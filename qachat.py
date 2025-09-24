from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import base64

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("AIzaSyCq97jvXiBCsaRrjWmVKPBifYuFP0_Gk_E"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-2.5-pro")

chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)  # streaming response
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")


# Function to convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Generate base64 string
image_base64 = get_base64_image("photo.png")  # make sure photo.png is in the same folder

# Inject CSS using f-string
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: lightblue; /* fallback */
        background-image: url("data:image/png;base64,{image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Test content
st.title("THINKBOT with Local Background")
st.write("Your chat app goes here…")
# Header for the application
st.header("THINKBOT")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input and button to submit
input_text = st.text_input("How Can I Help You: ", key="input")
submit = st.button("Ask the question")

# Handle user input and model response
if submit and input_text:
    response = get_gemini_response(input_text)

    # Add user query to chat history
    st.session_state["chat_history"].append(("You", input_text))

    st.subheader("The Response is")
    bot_reply = ""  # collect full response

    for chunk in response:
        if hasattr(chunk, "text") and chunk.text:  # safe check
            st.write(chunk.text)
            bot_reply += chunk.text

    # Store bot reply in chat history
    if bot_reply:
        st.session_state["chat_history"].append(("Bot", bot_reply))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")
