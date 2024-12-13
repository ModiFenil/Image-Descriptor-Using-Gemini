import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
import streamlit as st
from io import BytesIO
import os
import time

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_gemini_content(input_text, image):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([input_text, image])
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

st.title("Image Descriptor Application")

image_input = st.file_uploader("Choose an image",type=["'jpg","jpeg","png"])

if image_input:
    st.image(image_input)
    user_input = st.text_input("ask anything related to uploaded image")

    if st.button("Click Here"):
        try:
            # Convert UploadedFile to PIL Image
            image = PIL.Image.open(BytesIO(image_input.read()))

            # Create a progress bar
            progress_bar = st.progress(0)
            progress_status = st.empty()

            # Update the progress bar incrementally
            for i in range(1, 101):
                time.sleep(0.03)  # Simulate a delay
                progress_bar.progress(i)
                progress_status.text(f"Processing... {i}%")
            
            # Generate content
            response_text = generate_gemini_content(user_input, image)

            if response_text:
                st.write(response_text)
            else:
                st.write("Failed to generate content.")

            # Remove the progress bar after completion
            progress_status.empty()
            progress_bar.empty()

        except Exception as e:
            st.error(f"Error processing the image: {e}")
else:
    st.write("Please upload an image.")
