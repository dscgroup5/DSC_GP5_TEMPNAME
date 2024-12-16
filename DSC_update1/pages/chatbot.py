import streamlit as st
from PIL import Image
import requests
import os
import google.generativeai as genai
import re
from huggingface_hub import InferenceClient

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

# Image Generation Function
def generate_image(prompt):
    try:
        # Use the text-to-image function
        image = client.text_to_image(prompt)
        # Ensure the image is in PIL format, and then return it
        if isinstance(image, Image.Image):
            return image
        else:
            return f"Error: Unexpected output format. Expected a PIL Image."
    except Exception as e:
        return f"Error generating image: {str(e)}"

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Streamlit UI
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

# Background Styling
import streamlit as st

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
st.markdown("### A smart assistant for text and image generation.")

# Sidebar with App Features
with st.sidebar:
    st.header("Features")
    feature = st.radio("Select a feature:", ["Chatbot", "Image Generation"], index=0)

# Chatbot UI
if feature == "Chatbot":
    set_background("https://www.shutterstock.com/image-vector/3d-vector-robot-chatbot-ai-600nw-2301916351.jpg") 
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.subheader("Chat with AI 🤖")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
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
