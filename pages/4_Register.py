import streamlit as st
from auth import register_user

st.title("Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
role = st.selectbox("Role", ["admin", "analyst", "it", "cyber"])

if st.button("Register"):
    try:
        register_user(username, password, role)
        st.success("User registered successfully!")
    except:
        st.error("Username already exists.")
