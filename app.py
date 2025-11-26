import streamlit as st

st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    layout="wide"
)

st.title("Multi-Domain Intelligence Platform")
st.write("Use the menu on the left to navigate between pages.")

st.sidebar.title("Navigation")
st.sidebar.write("Choose a page from the menu:")
st.sidebar.write("- Login")
st.sidebar.write("- Cybersecurity Dashboard")
st.sidebar.write("- IT Operations Dashboard")
