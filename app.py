from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def my_output(query):
    response = model.generate_content(query)
    return response.text

### UI development using streamlit

st.set_page_config(page_title="David")
st.header("David")
input = st.text_input("input" , key = "input")
submit = st.button("Ask your query")

if submit :
    response = my_output(input)
    st.subheader("The response is = ")
    st.write(response)