import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file='users.db'):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            last_period TEXT,
            cycle_length INTEGER,
            state TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods(
            user_id INTEGER,
            date TEXT,
            mood TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptoms(
            user_id INTEGER,
            date TEXT,
            symptom TEXT
        )
        """)
        self.conn.commit()

    def add_user(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (user_id,))
        self.conn.commit()

    def set_period(self, user_id, last_period, cycle_length=None):
        self.cursor.execute("UPDATE users SET last_period=?, cycle_length=? WHERE user_id=?",
                            (last_period, cycle_length, user_id))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {'user_id': row[0], 'last_period': row[1], 'cycle_length': row[2], 'state': row[3]}
        return {}

    def set_state(self, user_id, state):
        self.cursor.execute("UPDATE users SET state=? WHERE user_id=?", (state, user_id))
        self.conn.commit()

    def get_state(self, user_id):
        user = self.get_user(user_id)
        return user.get('state', None)

    def add_mood(self, user_id, mood):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO moods(user_id, date, mood) VALUES (?,?,?)", (user_id, today, mood))
        self.conn.commit()

    def get_mood_stats(self, user_id):
        self.cursor.execute("SELECT date, mood FROM moods WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()

    def add_symptom(self, user_id, symptom):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO symptoms(user_id, date, symptom) VALUES (?,?,?)", (user_id, today, symptom))
        self.conn.commit()

    def get_symptoms(self, user_id):
        self.cursor.execute("SELECT date, symptom FROM symptoms WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()
