import streamlit as st
from auth import verify_user

st.title(" Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    success, user = verify_user(username, password)
    
    if success:
        st.session_state["user"] = dict(user)
        st.session_state["logged"] = True
        st.success("Login successful! Navigate to dashboards.")
    else:
        st.error("Invalid username or password.")
