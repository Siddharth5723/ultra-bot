from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# -------------------- LOAD ENV VARIABLES --------------------
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyAvBNrlL-I2doeMJbutks4e1meenz26Ooo"))  # Store your API key in .env

# -------------------- MODEL SETUP --------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------- STREAMING FUNCTION --------------------
def stream_output(query):
    """Generate response in a streaming fashion."""
    full_response = ""
    for chunk in model.generate_content(query, stream=True):
        if chunk.text:
            full_response += chunk.text
            yield chunk.text
    return full_response

# -------------------- SESSION STATE --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- UI SETUP --------------------
st.set_page_config(page_title="David Chatbot", layout="wide")
st.title("🤖 David - Your AI Assistant")

# Personality selector
mode = st.selectbox("🧠 Choose Chat Mode", 
                    ["Default", "Formal", "Casual", "Motivational", "Sarcastic"])

# Input box
user_input = st.text_input("💬 Enter your query", key="input")

# File upload
uploaded_file = st.file_uploader("📂 Upload a file (txt, pdf, csv)", 
                                  type=["txt", "pdf", "csv"])

# Submit button
submit = st.button("Ask")

# -------------------- FILE READING --------------------
def read_file_content(uploaded_file):
    """Reads and returns the file content."""
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8", errors="ignore")
    elif file_type == "csv":
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        return df.to_string()
    elif file_type == "pdf":
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    return ""

# -------------------- CHAT PROCESS --------------------
if submit:
    # Personality-based prompt
    if mode != "Default":
        final_prompt = f"Respond in a {mode} tone. Question: {user_input}"
    else:
        final_prompt = user_input

    # If file uploaded, append file content
    if uploaded_file:
        file_content = read_file_content(uploaded_file)
        final_prompt = f"Based on this file content:\n{file_content}\n\nQuestion: {user_input}"

    # Store user input
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Stream response
    st.subheader("🤖 David's Response:")
    response_placeholder = st.empty()
    full_text = ""
    for token in stream_output(final_prompt):
        full_text += token
        response_placeholder.write(full_text)

    # Store assistant's reply
    st.session_state.chat_history.append({"role": "assistant", "content": full_text})

# -------------------- DISPLAY CHAT HISTORY --------------------
st.markdown("### 📜 Conversation History")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**🧑 You:** {chat['content']}")
    else:
        st.markdown(f"**🤖 David:** {chat['content']}")
