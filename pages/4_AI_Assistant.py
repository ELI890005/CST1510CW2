import streamlit as st
import sqlite3
import pandas as pd
import openai  # type: ignore

# ------------------------------
# SETUP
# ------------------------------

# If using a real OpenAI API key:
# openai.api_key = st.secrets["OPENAI_API_KEY"]
# Or hardcode for testing (not recommended in GitHub!)

st.title(" AI Assistant")

st.write("Ask questions about cybersecurity incidents or IT operations.")

# ------------------------------
# LOAD DATA FROM DB
# ------------------------------

conn = sqlite3.connect("multi_domain.db")

cyber_df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
it_df = pd.read_sql_query("SELECT * FROM it_tickets", conn)

# ------------------------------
# USER QUESTION
# ------------------------------
question = st.text_input("Ask the AI a question:")

if st.button("Ask"):
    if not question:
        st.warning("Enter a question first.")
    else:
        st.write("Thinking...")

        # Build context
        context_text = (
            "CYBER INCIDENTS:\n" +
            cyber_df.to_string() +
            "\n\nIT TICKETS:\n" +
            it_df.to_string()
        )

        prompt = f"""
        You are an AI assistant analyzing an enterprise security and IT operations system.

        Context data:
        {context_text}

        User question:
        {question}

        Provide a clear, short, analytical answer.
        """

        # ------------------------------
        # USE YOUR AI MODEL
        # ------------------------------

        # If OpenAI key available:
        # response = openai.ChatCompletion.create(
        #     model="gpt-4o-mini",
        #     messages=[{"role": "user", "content": prompt}]
        # )

        # For now, we simulate an AI response (safe for coursework)
        fake_answer = "Based on the available incidents and ticket data, here is an analytical summary:\n\n" \
                      "- Phishing is the most common category.\n" \
                      "- High severity incidents are increasing.\n" \
                      "- IT delays are mostly caused by 'Waiting for User' and 'Investigation' stages.\n" \
                      "- Staff with the longest average resolution time may need support or workload balancing."

        st.success(fake_answer)
