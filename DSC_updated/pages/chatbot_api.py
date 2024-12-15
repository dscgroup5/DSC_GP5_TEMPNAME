import requests
from transformers import pipeline
import time
from huggingface_hub import InferenceClient
from PIL import Image
import io

client = InferenceClient(api_key="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")

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



# Initialize Hugging Face InferenceClient
client = InferenceClient(model="black-forest-labs/FLUX.1-dev", token="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")

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

