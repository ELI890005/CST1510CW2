import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, file="platform.db"):
        self.conn = sqlite3.connect(file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query, params=(), commit=False):
        cur = self.conn.cursor()
        cur.execute(query, params)
        if commit:
            self.conn.commit()
        return cur

    def fetch_all(self, query, params=()):
        return self.execute(query, params).fetchall()

    def fetch_one(self, query, params=()):
        return self.execute(query, params).fetchone()

    def init_schema(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash BLOB,
            role TEXT
        );
        """, commit=True)

        self.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            assigned_to TEXT,
            status TEXT,
            created_at TEXT,
            resolved_at TEXT
        );
        """, commit=True)

        self.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threat_type TEXT,
            severity TEXT,
            status TEXT,
            opened_at TEXT,
            closed_at TEXT
        );
        """, commit=True)

db = DatabaseManager()
db.init_schema()

