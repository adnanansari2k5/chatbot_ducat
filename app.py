import os 
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Configure the Google Generative AI API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# select the model
model = genai.GenerativeModel("genai-2.5-flash")

# Streamlit page config 
st.set_page_config(page_title="ducat chatboat",page_icon="🤖")
st.title("🤖 ducat chatbot")

# initialize chat history in session state
if"messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# chating input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # genrate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(prompt)
                reply = response.text
                st.markdown(reply)
            except Exception as e:
                st.error(f"Error: {e}")
                reply = "Sorry, I encountered an error."

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": reply})