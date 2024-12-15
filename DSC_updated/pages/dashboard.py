import streamlit as st
import whisper
from streamlit_mic_recorder import mic_recorder
import os
from pages.chatbot_api import generate_chatbot_response, generate_image


# Set Page Configuration (must be the first Streamlit command)
st.set_page_config(page_title="AI Chatbot Dashboard", page_icon="🎤", layout="centered")

# Background styling for the dashboard (excluding sidebar)
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: url('https://img.freepik.com/free-vector/geometric-style-futuristic-web-data-mesh-background-technology-research_1017-49432.jpg?semt=ais_hybrid');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background: none;  /* Transparent header */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Load Whisper Model (Cached)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")  # Model size options: "tiny", "small", "base"

model = load_whisper_model()

# Function to Transcribe Recorded Audio
def transcribe_audio(audio_bytes):
    temp_audio_path = "temp_audio.wav"
    with open(temp_audio_path, "wb") as f:
        f.write(audio_bytes)  # Write byte data to a temporary file
    result = model.transcribe(temp_audio_path)
    os.remove(temp_audio_path)
    return result["text"]

# Session State for Voice Command Input
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""  # Initialize user input

# Greeting Section
username = st.session_state.get("username", "PlayerOne")  # Replace with actual session username
st.markdown(f"<h2 style='text-align: center;'>Hey!!, how can I make your game interesting?</h2>", unsafe_allow_html=True)

# Voice Recorder Section (Populates Text Input)
st.write("Let's start a converstation..")
audio_bytes = mic_recorder(start_prompt="🎙️", stop_prompt="Stop Recording")

# Process Voice Input
if audio_bytes:  # Check if mic_recorder returned audio data
    st.info("Processing your voice input...")
    try:
        audio_data = audio_bytes['bytes']
        transcription = transcribe_audio(audio_data)
        st.session_state["user_input"] = transcription  # Populate session state
    except Exception as e:
        st.error(f"Error during transcription: {e}")

# Text Input Section (Populated by Voice Command)
user_input = st.text_input(
    "Enter your message:",
    value=st.session_state["user_input"],
    placeholder="Speak or type your message...",
    key="text_input",
)

# Send Button (Inside Input Section)
col1, col2 = st.columns([8, 2])
with col1:
    pass  # Keeps layout clean
with col2:
    send_button = st.button("↩ Send")


if send_button:
    if user_input.strip():  # Ensure input is not empty
        cleaned_input = user_input.strip()
        st.info(f"Processing your input: {cleaned_input}")
        chatbot_response = generate_chatbot_response(user_input.strip())
        
        # Check if the user asks for an image
        if "image" in user_input.lower():  # Example condition for image request
            image_url = generate_image(user_input.strip())
            st.image(image_url, caption="Generated Image", use_container_width=True)


        # Display chatbot response
        st.success(f"Chatbot Response: {chatbot_response}")
    else:
        st.warning("Please provide a message.")

# Features Section
st.markdown(
    """
    <h3 style='text-align: center;'>Explore Features 🚀</h3>
    """,
    unsafe_allow_html=True
)
feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.button("Story Creation 📚", use_container_width=True)
with feature_col2:
    st.button("Image Generation 🎨", use_container_width=True)
with feature_col3:
    st.button("Video Generation 🎥", use_container_width=True)