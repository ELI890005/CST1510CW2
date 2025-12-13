import streamlit as st
import pandas as pd
import plotly.express as px
from database import db
from gemini_ai import gemini_reply

# AUTH CHECK
if "logged" not in st.session_state:
    st.error("Please login first.")
    st.stop()

st.title(" Cybersecurity Dashboard")

# LOAD DATA
rows = db.fetch_all("SELECT * FROM cyber_incidents")
df = pd.DataFrame(rows)

# SHOW TABLE
st.subheader(" Incidents Table")
if df.empty:
    st.info("No cybersecurity incidents yet.")
else:
    st.dataframe(df)

# ADD INCIDENT
st.subheader(" Create Cyber Incident")

threat = st.text_input("Threat Type (e.g. Phishing)")
severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
status = st.selectbox("Status", ["Open", "Investigating", "Resolved"])
opened_at = st.date_input("Opened At")

if st.button("Create Incident"):
    if threat:
        db.execute(
            """
            INSERT INTO cyber_incidents (threat_type, severity, status, opened_at)
            VALUES (?, ?, ?, ?)
            """,
            (threat, severity, status, str(opened_at)),
            commit=True,
        )
        st.success("Incident added! Refresh page.")
    else:
        st.warning("Threat type is required.")

# CHART
st.subheader("Threat Frequency")

if not df.empty and "threat_type" in df.columns:
    fig = px.histogram(
        df,
        x="threat_type",
        title="Threat Frequency",
        color="threat_type",
    )
    st.plotly_chart(fig)
else:
    st.info("Add incidents to see analytics.")

# GEMINI AI
st.subheader(" Gemini Security Assistant")

question = st.text_input("Ask Gemini about cybersecurity trends")

if st.button("Ask Gemini (Cyber)"):
    if question:
        answer = gemini_reply(
            question,
            context="cybersecurity incidents, phishing trends, SOC operations, incident response",
        )
        st.write(answer)
    else:
        st.warning("Enter a question first.")

