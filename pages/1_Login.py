import streamlit as st
import sqlite3

# Connect to your existing SQLite DB
conn = sqlite3.connect("multi_domain.db")
cursor = conn.cursor()

st.title("User Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not username or not password:
        st.error("Please enter both username and password.")
    else:
        query = "SELECT password_hash, role FROM users WHERE username = ?"
        row = cursor.execute(query, (username,)).fetchone()

        if row is None:
            st.error("Invalid username or password.")
        else:
            stored_hash, role = row
            # For coursework demo we just show success
            st.success(f" Logged in as **{username}** (role: {role})")
