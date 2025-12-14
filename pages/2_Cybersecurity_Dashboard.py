import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Cybersecurity Dashboard",
    layout="wide"
)

DATA_PATH = "DATA/cyber_incidents.csv"

# ---------------- INIT CSV ----------------
if not os.path.exists("DATA"):
    os.makedirs("DATA")

if not os.path.exists(DATA_PATH):
    df_init = pd.DataFrame(columns=[
        "incident_id",
        "timestamp",
        "severity",
        "category",
        "status",
        "description"
    ])
    df_init.to_csv(DATA_PATH, index=False)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

# ---------------- TITLE ----------------
st.title(" Cybersecurity Operations Dashboard")
st.markdown("Monitor, record, and analyse cybersecurity incidents.")

# ---------------- CREATE INCIDENT ----------------
st.subheader(" Log New Security Incident")

with st.form("create_incident_form", clear_on_submit=True):

    category = st.selectbox(
        "Incident Type",
        ["Phishing", "Malware", "Intrusion", "DDoS", "Policy Violation"]
    )

    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High", "Critical"]
    )

    status = st.selectbox(
        "Status",
        ["Open", "In Progress", "Resolved"]
    )

    description = st.text_area("Incident Description")

    submitted = st.form_submit_button("Log Incident")

    if submitted:
        new_incident = {
            "incident_id": int(df["incident_id"].max() + 1) if not df.empty else 6001,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": severity,
            "category": category,
            "status": status,
            "description": description if description else "No description provided"
        }

        df = pd.concat([df, pd.DataFrame([new_incident])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)

        st.success(" Incident logged successfully")
        st.rerun()

# ---------------- INCIDENT TABLE ----------------
st.subheader(" Logged Incidents")
st.dataframe(df, use_container_width=True)

# ---------------- ANALYTICS ----------------
st.subheader(" Security Analytics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Incidents by Type")
    category_counts = df["category"].value_counts()
    if not category_counts.empty:
        st.bar_chart(category_counts)
    else:
        st.info("Add incidents to see analytics.")

with col2:
    st.markdown("### Incidents by Severity")
    severity_counts = df["severity"].value_counts()
    if not severity_counts.empty:
        st.bar_chart(severity_counts)

# ---------------- STATUS CHART ----------------
st.markdown("### Incident Status Distribution")
status_counts = df["status"].value_counts()
if not status_counts.empty:
    st.bar_chart(status_counts)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Cybersecurity Operations Dashboard | SOC Analytics | Streamlit")


