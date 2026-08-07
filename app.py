import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# Page settings
st.set_page_config(
    page_title="School AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 School AI Chatbot")
st.write("Ask me anything about the school!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I'm your School AI Assistant. How can I help you today?"
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def predict_response(user_text):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""
You are a helpful School AI Assistant.

Answer politely and clearly.
Help students with admissions, exams, fees, library,
courses, teachers, and campus facilities.

User Question:
{user_text}
"""
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {e}"


# Chat input
prompt = st.chat_input("Type your question...")

if prompt:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = predict_response(prompt)
            st.markdown(answer)

    # Save response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )