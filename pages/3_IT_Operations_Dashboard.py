import streamlit as st
import pandas as pd
import plotly.express as px
from database import db
from gemini_ai import gemini_reply

# AUTH CHECK
if "logged" not in st.session_state:
    st.error("Please login first.")
    st.stop()

st.title(" IT Operations Dashboard")

# LOAD DATA
rows = db.fetch_all("SELECT * FROM it_tickets")
df = pd.DataFrame(rows)

# SHOW TABLE
st.subheader(" Tickets Table")
if df.empty:
    st.info("No IT tickets yet.")
else:
    st.dataframe(df)

# ADD TICKET
st.subheader(" Create IT Ticket")

category = st.text_input("Category")
assigned = st.text_input("Assigned To")
status = st.selectbox(
    "Status", ["Open", "In Progress", "Waiting for User", "Resolved"]
)
created_at = st.date_input("Created At")

if st.button("Create Ticket"):
    if category and assigned:
        db.execute(
            """
            INSERT INTO it_tickets (category, assigned_to, status, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (category, assigned, status, str(created_at)),
            commit=True,
        )
        st.success("Ticket added! Refresh page.")
    else:
        st.warning("Category and Assigned To are required.")

# CHART
st.subheader(" Tickets by Category")

if not df.empty and "category" in df.columns:
    fig = px.bar(
        df,
        x="category",
        title="Ticket Distribution by Category",
        color="category",
    )
    st.plotly_chart(fig)
else:
    st.info("Add tickets to see analytics.")

# GEMINI AI
st.subheader(" Gemini IT Assistant")

question = st.text_input("Ask Gemini about IT ticket performance")

if st.button("Ask Gemini (IT)"):
    if question:
        answer = gemini_reply(
            question,
            context="IT operations, ticket resolution delays, staff performance, service desk analysis",
        )
        st.write(answer)
    else:
        st.warning("Enter a question first.")
