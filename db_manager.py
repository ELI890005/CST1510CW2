import sqlite3
import pandas as pd
import bcrypt
import os

DB_FILE = "multi_domain.db"


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    # -------------------------------
    # Create all tables
    # -------------------------------
    def create_tables(self):

        # ----- USERS TABLE -----
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                username TEXT PRIMARY KEY,
                password_hash TEXT,
                role TEXT
            );
        """)

        # Create default admin user
        self.create_default_admin()

        # ----- CYBER INCIDENTS TABLE -----
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents(
                incident_id INTEGER PRIMARY KEY,
                timestamp TEXT,
                severity TEXT,
                category TEXT,
                status TEXT,
                description TEXT
            );
        """)

        # ----- IT TICKETS TABLE -----
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets(
                ticket_id INTEGER PRIMARY KEY,
                priority TEXT,
                description TEXT,
                status TEXT,
                assigned_to TEXT,
                created_at TEXT,
                resolved_at TEXT,
                resolution_time_hours REAL
            );
        """)

        self.conn.commit()

        # Load CSV data only if tables are empty
        self.load_csv_if_empty("DATA/cyber_incidents.csv", "cyber_incidents")
        self.load_csv_if_empty("DATA/it_tickets.csv", "it_tickets")

    # -------------------------------
    # Create default admin user
    # -------------------------------
    def create_default_admin(self):
        default_user = "admin"
        default_pass = "Admin123"
        default_role = "it_admin"

        self.cursor.execute("SELECT username FROM users WHERE username = ?", (default_user,))
        exists = self.cursor.fetchone()

        if not exists:
            hashed = bcrypt.hashpw(default_pass.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            self.cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (default_user, hashed, default_role))

            self.conn.commit()
            print("✔ Default admin created: admin / Admin123")

    # -------------------------------
    # Load CSV into a table if empty
    # -------------------------------
    def load_csv_if_empty(self, csv_path, table_name):
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]

            if count == 0:
                print(f"📥 Loading CSV into {table_name} ...")

                df = pd.read_csv(csv_path)

                df.to_sql(table_name, self.conn, if_exists="append", index=False)
                print(f"✔ Loaded {len(df)} records into {table_name}")

        except Exception as e:
            print(f" Error loading {csv_path}: {e}")

    # -------------------------------
    # Read entire table
    # -------------------------------
    def read(self, table_name):
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            return df
        except Exception as e:
            print(f"⚠ Error reading table {table_name}: {e}")
            return pd.DataFrame()

    # -------------------------------
    # Insert generic record
    # -------------------------------
    def insert(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    # -------------------------------
    # Query helper
    # -------------------------------
    def query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

