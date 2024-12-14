import streamlit as st

# Set page configuration
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Background styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: url('https://t3.ftcdn.net/jpg/04/71/00/20/360_F_471002062_tCBbTqeeMhHgMfCW86mQhdgpETooy3ID.jpg') no-repeat center center fixed;
    background-size: cover;
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
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if st.button("Log In"):
        if username and password == "12345":  # Replace with your authentication logic
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")
