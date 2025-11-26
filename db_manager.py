import sqlite3

DB_NAME = "multi_domain.db"


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        """Execute INSERT/UPDATE/DELETE"""
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        """Return multiple rows"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        """Return one row"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def create_tables(self):
        """Create all required tables for the coursework."""
        # USERS TABLE
        self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                role TEXT
            );
        """)

        # CYBER INCIDENTS TABLE
        self.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                category TEXT,
                severity TEXT,
                status TEXT,
                created_at TEXT,
                resolved_at TEXT,
                assigned_to TEXT
            );
        """)

        # DATASETS TABLE (for Data Science domain)
        self.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT,
                size_mb REAL,
                last_updated TEXT,
                num_rows INTEGER,
                description TEXT
            );
        """)

        # IT TICKETS TABLE
        self.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                status TEXT,
                priority TEXT,
                opened_at TEXT,
                closed_at TEXT,
                assigned_staff TEXT,
                stage TEXT
            );
        """)

        print(" All tables created successfully.")


if __name__ == "__main__":
    db = DatabaseManager()
    db.create_tables()
