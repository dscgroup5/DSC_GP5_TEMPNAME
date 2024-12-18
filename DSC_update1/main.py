import streamlit as st

# Custom CSS to enhance the UI for generating GIFs and images
st.markdown(
    """
    <style>
    /* General App Styles */
    .stApp {
        background-color: #111111; /* Dark background */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Header without background color */
    .header {
        color: white;
        padding: 20px 0;
        text-align: center;
        font-size: 56px; /* Reduced size */
        font-weight: bold;
        letter-spacing: 1px; /* Slight letter spacing for modern look */
        border-bottom: 2px solid #444444; /* Subtle border */
        font-family: 'Poppins', sans-serif; /* Modern font */
        animation: fadeIn 1.5s ease-in-out; /* Smooth fade-in effect */
    }

    /* Welcome note styling */
    .welcome-note {
        font-size: 28px;
        font-weight: 500;
        color: white;
        text-align: left;
        margin-top: 20px;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
        padding-right: 20px;
    }

    /* Image/GIF Section */
    .image-gif-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-direction: row; /* Ensure layout is row */
        margin-top: 40px;
        gap: 40px; /* Space between title and image */
    }

    /* Styling the image/GIF preview */
    .preview-image {
        width: 80%;
        max-width: 500px;
        margin: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Button Styles */
    .stButton button {
        background-color: #2575fc;
        color: white;
        padding: 12px 40px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
        margin-top: 20px;
    }

    .stButton button:hover {
        background-color: #6a11cb;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .welcome-note {
            font-size: 22px;
        }
        .preview-image {
            width: 90%;
        }
    }

    /* Keyframe for smooth fade-in animation */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Header Section with modern design, no background color, and reduced size
st.markdown('<div class="header">SNAP.</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-note">Create your own amazing GIFs and images easily with just a click!</div>', unsafe_allow_html=True)

# Image/GIF Display Section with Title on the Left and Image on the Right
st.markdown('<div class="image-gif-container">', unsafe_allow_html=True)

# Display sample image/GIF on the right side
st.image("https://cdn.prod.website-files.com/624ac40503a527cf47af4192/65313084ff0fb3453089947e_giphy.gif", use_column_width=True, output_format="PNG")

# Title with catchy line on the left

st.markdown('</div>', unsafe_allow_html=True)
