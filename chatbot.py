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

# Initialize models and APIs
client = InferenceClient(api_key="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")
genai.configure(api_key="AIzaSyDgl2r7EC09IWQR0ZepGw2V0Ny1Bd0w9tY")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
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
    video_frames = pipe(prompt, num_inference_steps=25).frames
    
    # Create a temporary directory to store frames
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save frames as images
    for i, frame in enumerate(video_frames[0]):
        frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
        frame = (frame * 255).astype(np.uint8)  # Ensure uint8 format
        imageio.imwrite(frame_path, frame)
    
    # FFmpeg command to compile frames into a video
    output_filename = "output.mp4"
    ffmpeg_command = [
        "ffmpeg",
        "-framerate", "24",
        "-i", os.path.join(temp_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-y",
        output_filename,
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
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }}
    [data-testid="stHeader"] {{
        background: none;
    }}
    [data-testid="stSidebar"] {{
        background: #222222;
        color: white;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Page Header
st.title("AI Assistant 🤖")
st.markdown("### A smart assistant for text, image, and video generation.")

# Sidebar with App Features
with st.sidebar:
    st.header("Features")
    feature = st.radio("Select a feature:", ["Chatbot", "Image Generation", "Text-to-Video"], index=0)

# Chatbot UI
if feature == "Chatbot":
    set_background("https://www.shutterstock.com/image-vector/3d-vector-robot-chatbot-ai-600nw-2301916351.jpg") 
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.subheader("Chat with AI 🤖")

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
    set_background("https://cdn.pixabay.com/photo/2023/06/06/16/38/ai-generated-8045101_1280.jpg")
    st.subheader("Generate Images 🎨")
    image_prompt = st.text_area("Enter a description for the image:", placeholder="Describe an image...")
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
elif feature == "Text-to-Video":
    set_background("https://example.com/video-background.jpg")  # Set appropriate background
    st.subheader("Generate Videos 🎬")
    video_prompt = st.text_area("Enter a description for the video:", placeholder="Describe the video...")
    if st.button("Generate Video"):
        if video_prompt.strip():
            generate_video(video_prompt.strip())
        else:
            st.warning("Please provide a video description.")