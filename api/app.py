import streamlit as st
import re
import random
import string
import os
from pathlib import Path


# Common passwords blacklist
COMMON_PASSWORDS = {'password', 'password123', '123456', 'qwerty', 'admin'}

def calculate_password_strength(password):
    """Calculate password strength score based on weighted criteria"""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 2
    elif len(password) >= 6:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Add at least one number")

    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Add a special character (!@#$%^&*)")

    if password.lower() in COMMON_PASSWORDS:
        score = min(score, 2)
        feedback.append("This is a common password - choose something more unique")

    return score, feedback

def get_strength_label(score):
    """Convert score to strength label with colors"""
    if score <= 2:
        return "Weak", "#FF4444"  # Vibrant Red
    elif score <= 4:
        return "Moderate", "#FFA500"  # Bright Orange
    else:
        return "Strong", "#00CC00"  # Vivid Green

def generate_strong_password():
    """Generate a strong random password"""
    characters = (string.ascii_lowercase + string.ascii_uppercase + 
                 string.digits + "!@#$%^&*")
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]
    password += random.choices(characters, k=8)
    random.shuffle(password)
    return ''.join(password)

def main():
    # Streamlit app configuration
    st.set_page_config(
    page_title="Password Strength Meter",  # Title of the page
    page_icon="../static/favicon.ico",      # Path to the favicon image
    )
    
    # Updated CSS with improved logo centering
    st.markdown("""
        <style>
        .stApp {
            background: none;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .center-text {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
       }
        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(40deg, #1E3A8A, #93C5FD);
            z-index: -1;
        }
        .title {
            color: white;
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 5vmin;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: fadeIn 1s ease-in;
        }
        .stButton>button {
            background-color: #0A1A33;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 12px 24px;
            font-weight: bold;
            transition: transform 0.3s;
            display: block;
            margin: 10px auto;
            width: 300px;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            background-color: #142952;
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #0A1A33;
            padding: 0px;
            font-size: 20px;
            color: #fff;
            text-align: center;
            background: #142952;
            text-align: middle;
        }
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
            animation: slideUp 0.5s ease-in;
        }
        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 80vh;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
            height: 100vh; /* Full screen height for centering */
            flex-direction: column;
        }
        .centered-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            max-width: 100%;
            height: auto;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
        <div class="background"></div>
    """, unsafe_allow_html=True)

    # Main container for vertical distribution
    with st.container():
        # Logo using st.image with improved centering
        try:
            with st.container():
                # Create a column layout and center the image in the middle column
               col1, col2, col3 = st.columns([1.2, 1, 0.8])
               with col2:
                st.image("../static/logo.png", width=130)
                # Ensure the image is centered in the container
                st.markdown(
                    '<style>.stImage { display: block; margin-left: auto; margin-right: auto; }</style>',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"Error loading logo: {str(e)}")
            st.warning("Please ensure 'logo.png' exists in the 'static' folder")
            # Fallback to placeholder, centered
            with st.container():
                st.image("https://via.placeholder.com/120", width=120, caption="Placeholder Logo")
                st.markdown(
                    '<style>.stImage { display: block; margin-left: auto; margin-right: auto; }</style>',
                    unsafe_allow_html=True
                )

        # App header
        st.markdown('<div class="title">🔒 Password Strength Meter</div>', unsafe_allow_html=True)
        st.markdown('<p style="color: white; text-align: center; margin-top: -1.5vmin; font-size: 2vmin;">FOR GIAIC Q3 - ROLL # 00037391 BY MERCHANTSONS</p>', 
                    unsafe_allow_html=True)

        # Main content in a card
        with st.container():   
            st.markdown('<div class="center-text">', unsafe_allow_html=True)
            password = st.text_input("Enter your password", type="password", placeholder="Type your password here")
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("Check Strength"):
                if password:
                    score, feedback = calculate_password_strength(password)
                    strength, color = get_strength_label(score)

                    st.markdown(f"""
                        <div style='text-align: center; padding: 15px;'>
                            <h2 style='color: {color}; margin: 0;'>{strength}</h2>
                            <p style='color: #0A1A33; margin: 5px 0;'>Score: {score}/6</p>
                        </div>
                    """, unsafe_allow_html=True)

                    st.progress(score / 6)

                    if feedback:
                        st.markdown("### 💡 Improvement Tips:")
                        for item in feedback:
                            st.markdown(f'<p style="color: #0A1A33;">⚠️ {item}</p>', 
                                      unsafe_allow_html=True)
                    else:
                        st.markdown('<p style="color: #00CC00; text-align: center;">🎉 Perfect Password!</p>', 
                                  unsafe_allow_html=True)

        # Generator section
        with st.container():
            st.markdown('<h3 style="color: #0A1A33; text-align: center;">Auto Generate Strong Password!</h3>', 
                       unsafe_allow_html=True)
            if st.button("Generate Strong Password"):
                new_password = generate_strong_password()
                st.markdown(f"""
                    <div style='text-align: center; padding: 10px;'>
                        <p style='background: #f9c23c; color: #000; font-size: 18px; font-weight: bold; width: 250px; margin: 0 auto;'>
                            {new_password}
                        </p>
                        <p style='color: #000;'>Copy and test it above!</p>
                    </div>
                """, unsafe_allow_html=True)

    # Footer at bottom
    st.markdown("""
        <p style='color: white; text-align: center; margin-top: 20px;'>
            © Copyright 2025 Merchantsons. All rights reserved.
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
