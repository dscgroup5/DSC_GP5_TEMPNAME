import streamlit as st
from PIL import Image
import requests
from huggingface_hub import InferenceClient

# Initialize the Hugging Face API Client
client = InferenceClient(api_key="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")

# Chatbot Function
def generate_chatbot_response(prompt):
    messages = [
        {
            "role": "user",  # The message comes from the user
            "content": prompt
        }
    ]
    try:
        # Call the API for text generation
        completion = client.chat.completions.create(
            model="microsoft/DialoGPT-medium", 
            messages=messages, 
            max_tokens=500  # Adjust the number of tokens as needed
        )
        # Return the chatbot's response
        return completion.choices[0].message['content']
    except Exception as e:
        return f"Error generating response: {str(e)}"

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

# Streamlit UI
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

# Background Styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: white;
}
[data-testid="stHeader"] {
    background: none;
}
[data-testid="stSidebar"] {
    background: #222222;
    color: white;
}
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
    st.subheader("Chat with AI 🤖")
    user_prompt = st.text_area("Enter your message:", placeholder="Type something...")
    if st.button("Send"):
        if user_prompt.strip():
            st.info("Processing your message...")
            response = generate_chatbot_response(user_prompt.strip())
            if response:
                st.success(f"AI Response: {response}")
            else:
                st.warning("No response generated. Please try again.")
        else:
            st.warning("Please provide a message.")

# Image Generation UI
elif feature == "Image Generation":
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
