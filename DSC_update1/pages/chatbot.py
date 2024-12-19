import streamlit as st
import os
import subprocess
import numpy as np
import imageio
from PIL import Image
import google.generativeai as genai
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch
from huggingface_hub import InferenceClient
import dotenv

dotenv.load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")  
hf_api_key = os.getenv("HF_API_KEY")         
client = InferenceClient(api_key=hf_api_key)
genai.configure(api_key=gemini_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Load Text-to-Video Pipeline
pipe = DiffusionPipeline.from_pretrained(
    "damo-vilab/text-to-video-ms-1.7b",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

# Function for generating an image
def generate_image(prompt):
    try:
        # Use the text-to-image function
        image = client.text_to_image(prompt)
        if isinstance(image, Image.Image):
            return image
        else:
            return f"Error: Unexpected output format. Expected a PIL Image."
    except Exception as e:
        return f"Error generating image: {str(e)}"

# Function to generate video frames
def generate_video(prompt):
    st.info("Generating video... Please wait.")
    
    # Generate video frames
    video_frames = pipe(prompt, num_inference_steps=25, num_frames=100).frames
    
    # Create a temporary directory to store frames
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    # Frame rate and target duration
    frame_rate = 24
    target_duration = 5  # in seconds
    target_frame_count = frame_rate * target_duration

    # Get the total number of available frames in the batch
    available_frames = len(video_frames[0])  # Assuming batch size of 1

    # Calculate how many times to repeat the frames to reach the target
    repeat_factor = target_frame_count // available_frames
    extra_frames = target_frame_count % available_frames

    # Repeat and extend the frames
    extended_frames = np.concatenate(
        [video_frames[0]] * repeat_factor + [video_frames[0][:extra_frames]]
    )

    # Save each frame as an image file
    for i, frame in enumerate(extended_frames):
        frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")

        # Convert frame to uint8 before saving
        frame = (frame * 255).astype(np.uint8)

        imageio.imwrite(frame_path, frame)

    # Construct FFmpeg command
    output_filename = "output.mp4"
    ffmpeg_command = [
        "ffmpeg",
        "-framerate", str(frame_rate),  # Set frame rate
        "-i", os.path.join(temp_dir, "frame_%04d.png"),  # Input pattern
        "-c:v", "libx264",  # Video codec
        "-pix_fmt", "yuv420p",  # Pixel format
        "-crf", "18",  # Constant Rate Factor (adjust for quality/size)
        "-y",  # Overwrite output file if it exists
        output_filename,  # Output filename
    ]

    # Run FFmpeg command
    process = subprocess.run(ffmpeg_command, capture_output=True, text=True)
    
    # Handle success or failure
    if process.returncode == 0:
        st.success(f"Video successfully generated! You can download it below:")
        st.video(output_filename)
    else:
        st.error("Error generating video.")
        st.error(process.stderr)
    
    # Clean up temporary frames
    import shutil
    shutil.rmtree(temp_dir)
    
    # Free GPU memory
    torch.cuda.empty_cache()

# Streamlit UI
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

# Background Styling
def set_background(image_url):
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("{image_url}");
        background-size : cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0, 0, 0, 0.5); /* Semi-transparent header */
    }}
    [data-testid="stSidebar"] {{
        background: rgba(34, 34, 34, 0.8); /* Dark sidebar with transparency */
        color: white;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Page Header
st.title("SNAP.")
st.markdown("### A smart assistant for text, image, and video generation.")

# Sidebar with App Features
with st.sidebar:
    st.header("Features")
    feature = st.radio("Select a feature:", ["Chatbot", "Image Generation", "Generate-GIFs"], index=0)

# Chatbot UI
if feature == "Chatbot":
    set_background("https://wallpapers.com/images/hd/mac-dark-3840-x-2160-u5bxti3gf7fke6yo.jpg") 
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])


    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message("assistant" if message.role == "model" else "user"):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Chatbot...")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image Generation UI
elif feature == "Image Generation":
    set_background("https://wallpapers.com/images/hd/mac-dark-3840-x-2160-u5bxti3gf7fke6yo.jpg") 
    st.subheader("Generate Images 🎨")
    image_prompt = st.text_area("Enter a description for the image:", placeholder="Baby Yoda in Darth Vadar's Lap?")
    if st.button("Generate"):
        if image_prompt.strip():
            st.info("Generating your image...")
            image = generate_image(image_prompt.strip())
            if isinstance(image, Image.Image):
                st.image(image, caption="Generated Image", use_column_width=True)
            else:
                st.error(image)
        else:
            st.warning("Please provide an image description.")

# Text-to-Video Generation UI
elif feature == "Generate-GIFs":
    set_background("https://wallpapers.com/images/hd/mac-dark-3840-x-2160-u5bxti3gf7fke6yo.jpg") 
    st.subheader("Generate GIFs")
    video_prompt = st.text_area("Enter a description for the GIF:", placeholder="A cycle race?")
    if st.button("Generate Video"):
        if video_prompt.strip():
            generate_video(video_prompt.strip())
        else:
            st.warning("Please provide a video description.")