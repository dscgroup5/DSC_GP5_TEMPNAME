import pyrebase
import streamlit as st
from datetime import datetime



firebaseConfig = {
  'apiKey': "AIzaSyCbda_06n7nIWfF0QZ4vrGPn1EuiZGEW9s",
  'authDomain': "dscproject-f948b.firebaseapp.com",
  'projectId': "dscproject-f948b",
  'databaseURL': "https://dscproject-f948b-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "dscproject-f948b.firebasestorage.app",
  'messagingSenderId': "164203532070",
  'appId': "1:164203532070:web:2258c667c189af6b17bbe7",
  'measurementId': "G-4RW8BMLYJ1"
}

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Background styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: url('https://wallpaperaccess.com/full/3713231.jpg') no-repeat center center fixed;
    background-size: cover;
}

[data-testid="stAppViewContainer"] > div:first-child {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh;
}

.login-container {
    background: rgba(0, 0, 0, 0.7);
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    color: white;
    width: 350px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firebase.database()

st.markdown(
    """
    <style>
    .centered-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
        text-align: center;
    }
    .content-box {
        background-color: black; /* Black background */
        padding: 20px; /* Padding inside the box */
        border-radius: 10px; /* Rounded corners */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); /* Shadow effect */
        color: white; /* White text color */
        max-width: 600px; /* Limit width of the box */
    }
    .main-title {
        font-size: 2.5rem; /* Larger font size for title */
        margin-bottom: 10px; /* Space below the title */
    }
    .subtitle {
        font-size: 1.5rem; /* Smaller font size for subtitle */
        margin-top: 0;
    }
    </style>
    <div class="centered-content">
        <div class="content-box">
            <h1 class="main-title">SnapWrite</h1>
            <h2 class="subtitle">🤖 Your AI chatbot, 🖼️ image, and 🎥 gif generator</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.subheader("Login and Signup")

option = st.radio("Choose an option:", ["Login", "Sign Up"])
if option == "Sign Up":
    st.subheader("Create a New Account")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    if st.button("Signup"):
        try:
            user = auth.create_user_with_email_and_password(new_email, new_password)
            user = auth.sign_in_with_email_and_password(new_email,new_password)
            st.success('account created successfully',icon="✅")
            st.balloons()
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif option == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            db.child(user['localId']).child("Email").set(email)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.switch_page("pages/chatbot.py")
        except Exception as e:
            st.error(f"Error: {str(e)}")
