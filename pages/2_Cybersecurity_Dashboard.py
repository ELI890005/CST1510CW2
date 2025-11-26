import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to the same DB the rest of the app uses
conn = sqlite3.connect("multi_domain.db", check_same_thread=False)
cursor = conn.cursor()

st.title("Cybersecurity Dashboard")

st.write("This dashboard shows security incidents and basic analytics.")


# --------- Helper: load incidents into a DataFrame ---------
@st.cache_data
def load_incidents():
    query = """
        SELECT id, incident_id, category, severity, status,
               created_at, resolved_at, assigned_to
        FROM cyber_incidents
        ORDER BY created_at DESC
    """
    return pd.read_sql_query(query, conn)


# --------- Section 1: Add a new incident ---------
st.subheader("Add New Incident")

with st.form("new_incident_form"):
    col1, col2 = st.columns(2)

    with col1:
        incident_id = st.text_input("Incident ID (e.g. INC1001)")
        category = st.selectbox(
            "Category",
            ["Phishing", "Malware", "Ransomware", "Data Breach", "Other"]
        )
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])

    with col2:
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        created_at = st.text_input("Created At (YYYY-MM-DD)", value="2025-01-01")
        resolved_at = st.text_input(
            "Resolved At (YYYY-MM-DD or empty if not resolved)",
            value=""
        )
        assigned_to = st.text_input("Assigned To (Analyst name)", value="Analyst1")

    submitted = st.form_submit_button("Add Incident")

    if submitted:
        cursor.execute(
            """
            INSERT INTO cyber_incidents
            (incident_id, category, severity, status,
             created_at, resolved_at, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                incident_id,
                category,
                severity,
                status,
                created_at,
                resolved_at if resolved_at.strip() != "" else None,
                assigned_to,
            ),
        )
        conn.commit()
        st.success(f"Incident {incident_id} added successfully!")
        # Clear cache so table & charts refresh
        load_incidents.clear()


st.divider()

# --------- Section 2: Incidents table ---------
st.subheader("All Incidents")

df = load_incidents()

if df.empty:
    st.info("No incidents in the database yet. Add some using the form above.")
else:
    st.dataframe(df, use_container_width=True)

    st.divider()

    # --------- Section 3: Quick metrics ---------
    st.subheader("Key Metrics")

    total_incidents = len(df)
    open_incidents = (df["status"] != "Resolved").sum()
    high_or_critical = df["severity"].isin(["High", "Critical"]).sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Incidents", total_incidents)
    c2.metric("Open / In Progress", open_incidents)
    c3.metric("High & Critical", high_or_critical)

    st.divider()

    # --------- Section 4: Visualisations ---------
    st.subheader("Visualisations")

    # Incidents by category
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["category", "count"]

    fig_cat = px.bar(
        cat_counts,
        x="category",
        y="count",
        title="Incidents by Category",
        labels={"category": "Category", "count": "Number of Incidents"},
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # Incidents by severity
    sev_counts = df["severity"].value_counts().reset_index()
    sev_counts.columns = ["severity", "count"]

    fig_sev = px.pie(
        sev_counts,
        names="severity",
        values="count",
        title="Incidents by Severity",
    )
    st.plotly_chart(fig_sev, use_container_width=True)

    st.divider()

    # --------- Section 5: Update status for an incident ---------
    st.subheader("Update Incident Status")

    incident_options = df["incident_id"].tolist()
    selected_incident = st.selectbox(
        "Choose incident to update",
        incident_options,
    )

    new_status = st.selectbox(
        "New status",
        ["Open", "In Progress", "Resolved"],
    )

    if st.button("Update Status"):
        cursor.execute(
            "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
            (new_status, selected_incident),
        )
        conn.commit()
        st.success(f"Status for {selected_incident} updated to {new_status}.")
        load_incidents.clear()
