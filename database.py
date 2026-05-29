import sqlite3

DB_NAME = "sentinelshield.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        threat TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def insert_log(ip, threat):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (ip, threat) VALUES (?, ?)",
        (ip, threat)
    )

    conn.commit()
    conn.close()

def get_logs():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY time DESC")
    logs = cursor.fetchall()

    conn.close()
    return logs
