import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to existing database
conn = sqlite3.connect("multi_domain.db")
cursor = conn.cursor()

st.title("🛠️ IT Operations Dashboard")
st.write("Track IT tickets, performance, delays, and staff workload.")

# ================================
# LOAD TICKETS
# ================================
def load_tickets():
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    return df

df = load_tickets()

# ================================
# DISPLAY TABLE
# ================================
st.subheader("📋 All Tickets")
st.dataframe(df, use_container_width=True)

# ================================
# ADD NEW TICKET
# ================================
st.subheader("Add New Ticket")

col1, col2, col3 = st.columns(3)

with col1:
    ticket_id = st.text_input("Ticket ID")
    status = st.selectbox("Status", ["Open", "In Progress", "Waiting for User", "Closed"])

with col2:
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    opened_at = st.date_input("Opened At")

with col3:
    closed_at = st.text_input("Closed At (YYYY-MM-DD or empty)")
    assigned_staff = st.text_input("Assigned Staff")
    stage = st.selectbox("Stage", ["Assigned", "Investigation", "Waiting for User", "Resolved"])

if st.button("Add Ticket"):
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, status, priority, opened_at, closed_at, assigned_staff, stage)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, status, priority, str(opened_at), closed_at, assigned_staff, stage))
    
    conn.commit()
    st.success("Ticket added successfully!")
    st.experimental_rerun()

# ================================
# VISUALIZATIONS
# ================================
st.subheader(" IT Operations Insights")

# Tickets by priority
priority_counts = df["priority"].value_counts().reset_index()
priority_counts.columns = ["Priority", "Count"]

fig1 = px.bar(priority_counts, x="Priority", y="Count", title="Tickets by Priority", color="Priority")
st.plotly_chart(fig1, use_container_width=True)

# Tickets by status
status_counts = df["status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig2 = px.pie(status_counts, names="Status", values="Count", title="Ticket Status Breakdown")
st.plotly_chart(fig2, use_container_width=True)

# Avg resolution time (for closed tickets)
if "closed_at" in df.columns and "opened_at" in df.columns:
    df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce")
    df["closed_at"] = pd.to_datetime(df["closed_at"], errors="coerce")

    df["resolution_days"] = (df["closed_at"] - df["opened_at"]).dt.days

    # Filter valid records
    resolved_df = df.dropna(subset=["resolution_days"])

    if not resolved_df.empty:
        avg_by_staff = resolved_df.groupby("assigned_staff")["resolution_days"].mean().reset_index()

        fig3 = px.bar(avg_by_staff, x="assigned_staff", y="resolution_days",
                      title="Average Resolution Time by Staff (days)")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No closed tickets to calculate resolution times yet.")
