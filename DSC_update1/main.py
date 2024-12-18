import streamlit as st

# Custom CSS to center the image and style the app
st.markdown(
    """
    <style>
    .center-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        height: auto;
    }
    .stApp {
        background-color: #f4f4f4; /* Light neutral background */
    }
    /* Styling the welcome note */
    .welcome-note {
        text-align: center;
        font-size: 24px;
        color: #333333; /* Darker text for visibility */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Welcome Note
st.markdown('<p class="welcome-note">Welcome! DSC RIT core members are here to help you.</p>', unsafe_allow_html=True)

# Display the specified image in the center using HTML
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.postimg.cc/br3Rt14H/Untitled.png" 
             alt="Your AI Chatbot Companion" class="center-image">
    </div>
    """,
    unsafe_allow_html=True
)

# Add Button
if st.button("Get Started 🚀"):
    st.success("Welcome to the future of AI chatbots! 🎮")
    st.balloons()
