import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

def setup_db():
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # SMTP configuration table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS smtp_settings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        email TEXT,
        server TEXT,
        port INTEGER,
        app_password TEXT
    )
    """)

    # Sent mails table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sent_mails(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        receiver TEXT,
        subject TEXT,
        message TEXT,
        timestamp TEXT,
        status TEXT
    )
    """)
    conn.commit()
