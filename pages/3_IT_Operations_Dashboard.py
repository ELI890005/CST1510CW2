import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="IT Operations Dashboard",
    layout="wide"
)

DATA_PATH = "DATA/it_tickets.csv"

# ---------------- INIT CSV ----------------
if not os.path.exists("DATA"):
    os.makedirs("DATA")

if not os.path.exists(DATA_PATH):
    df_init = pd.DataFrame(columns=[
        "ticket_id",
        "category",
        "priority",
        "description",
        "status",
        "assigned_to",
        "created_at",
        "resolution_time_hours"
    ])
    df_init.to_csv(DATA_PATH, index=False)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

# ---------------- TITLE ----------------
st.title(" IT Operations Dashboard")
st.markdown("Manage IT support tickets and view operational analytics.")

# ---------------- CREATE TICKET ----------------
st.subheader(" Create New Ticket")

with st.form("create_ticket_form", clear_on_submit=True):
    category = st.selectbox(
        "Category",
        ["Network", "Hardware", "Software", "Security"]
    )

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High", "Critical"]
    )

    status = st.selectbox(
        "Status",
        ["Open", "In Progress", "Waiting for User", "Resolved"]
    )

    assigned_to = st.selectbox(
        "Assigned To",
        ["IT_Support_A", "IT_Support_B", "IT_Support_C", "Admin"]
    )

    description = st.text_area("Description")

    submitted = st.form_submit_button("Create Ticket")

    if submitted:
        new_ticket = {
            "ticket_id": int(df["ticket_id"].max() + 1) if not df.empty else 4001,
            "category": category,
            "priority": priority,
            "description": description if description else "No description provided",
            "status": status,
            "assigned_to": assigned_to,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resolution_time_hours": 0
        }

        df = pd.concat([df, pd.DataFrame([new_ticket])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)

        st.success(" Ticket created successfully")
        st.rerun()

# ---------------- TABLE ----------------
st.subheader(" All Tickets")
st.dataframe(df, use_container_width=True)

# ---------------- ANALYTICS ----------------
st.subheader(" Analytics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Tickets by Category")
    category_counts = df["category"].value_counts()
    if not category_counts.empty:
        st.bar_chart(category_counts)
    else:
        st.info("Add tickets to see analytics.")

with col2:
    st.markdown("### Tickets by Status")
    status_counts = df["status"].value_counts()
    if not status_counts.empty:
        st.bar_chart(status_counts)

# ---------------- PRIORITY CHART ----------------
st.markdown("### Tickets by Priority")
priority_counts = df["priority"].value_counts()
if not priority_counts.empty:
    st.bar_chart(priority_counts)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("IT Operations Dashboard | Coursework Ready | Streamlit")

