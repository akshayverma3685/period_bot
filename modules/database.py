# modules/database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            last_period TEXT,
            cycle_length INTEGER,
            symptoms TEXT,
            mood TEXT
        )
        ''')
        self.conn.commit()

    def add_user(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "last_period": row[1],
                "cycle_length": row[2],
                "symptoms": row[3],
                "mood": row[4]
            }
        return {}

    def update_user(self, user_id, **kwargs):
        for key, value in kwargs.items():
            self.cursor.execute(f"UPDATE users SET {key}=? WHERE user_id=?", (value, user_id))
        self.conn.commit()

    def set_state(self, user_id, state):
        self.update_user(user_id, mood=state)  # temporary use mood field for state

    def get_state(self, user_id):
        user = self.get_user(user_id)
        return user.get("mood")
