import sqlite3

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tutor_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            experience INTEGER,
            price_per_hour INTEGER
        )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_slot TEXT UNIQUE
        )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        tutor_id INTEGER,
        subject TEXT,
        slot_id INTEGER,
        status TEXT
        )
    """)



    conn.commit()
    conn.close()

def seed_slots():
    conn = get_db_connection()

    slots = [
        "09:00-10:00",
        "10:00-11:00",
        "11:00-12:00",
        "14:00-15:00",
        "15:00-16:00"
    ]

    for s in slots:
        conn.execute(
            "INSERT OR IGNORE INTO slots (time_slot) VALUES (?)",
            (s,)
        )

    conn.commit()
    conn.close()





