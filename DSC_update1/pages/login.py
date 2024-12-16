import streamlit as st
from firebase_admin import auth, credentials, initialize_app
import firebase_admin

# Initialize Firebase app only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(r"pages/dscproject-f948b-8497a0ceddfe.json")
    initialize_app(cred)

# Set page configuration
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

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

st.title("Login Page")

if st.session_state.authenticated:
    st.success("You are already logged in!")
else:
    option = st.radio("Choose an option:", ["Log In", "Sign Up"])
    if option == "Log In":
        username = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        if st.button("Log In"):
            try:
                # Check if user exists
                user = auth.get_user_by_email(username)
                # Simulate password verification
                st.warning("Password verification is not handled by Firebase Admin SDK.")
                if password == "firebase_placeholder":
                    st.session_state.authenticated = True
                    st.success("Login successful!")
                else:
                    st.error("Invalid password")
            except Exception as e:
                st.error(f"Login failed: {e}")

    elif option == "Sign Up":
        new_email = st.text_input("Email", placeholder="Enter your email for signup")
        new_password = st.text_input("Password", placeholder="Enter a new password", type="password")

        if st.button("Sign Up"):
            try:
                user = auth.create_user(email=new_email, password=new_password)
                st.success("Sign up successful! You can now log in.")
            except Exception as e:
                st.error(f"Error during sign up: {e}")
