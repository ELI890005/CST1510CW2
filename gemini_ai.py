import google.generativeai as genai
import streamlit as st

def gemini_reply(question, context=""):
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    full_prompt = f"Context: {context}\n\nUser Question: {question}"

    response = model.generate_content(full_prompt)
    return response.text
