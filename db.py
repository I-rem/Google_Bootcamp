import sqlite3

def connect_db():
    conn = sqlite3.connect("beni_teshis_et.db", check_same_thread=False)
    return conn

def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS case_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        complaint TEXT,
        user_diagnosis TEXT,
        correct_diagnosis TEXT,
        is_correct BOOLEAN,
        score INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
