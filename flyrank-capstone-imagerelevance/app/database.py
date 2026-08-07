# Simple SQLite database integration for persisting review decisions and image metadata
import sqlite3

DB_NAME = "imagerelevance.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table for image metadata
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            subject TEXT,
            category TEXT,
            confidence REAL
        )
    ''')
    
    # Table for review API decisions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS review_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_topic TEXT,
            image_subject TEXT,
            status TEXT,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()