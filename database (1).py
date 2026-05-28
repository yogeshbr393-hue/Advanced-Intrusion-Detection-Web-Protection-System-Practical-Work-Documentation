import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "database")

# ✅ ENSURE FOLDER EXISTS BEFORE ANYTHING ELSE
os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, "sentinel.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attack_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attack_type TEXT,
        payload TEXT,
        ip_address TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_attack(attack_type, payload, ip_address):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO attack_logs (attack_type, payload, ip_address, timestamp)
    VALUES (?, ?, ?, ?)
    """, (attack_type, payload, ip_address, datetime.now()))

    conn.commit()
    conn.close()