# modules/database.py
import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                last_period TEXT,
                cycle_length INTEGER,
                state TEXT
            )
        ''')

        # Moods table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                mood TEXT
            )
        ''')

        # Symptoms table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                symptom TEXT
            )
        ''')

        self.conn.commit()

    # User methods
    def add_user(self, user_id):
        self.cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {'user_id': row[0], 'last_period': row[1], 'cycle_length': row[2], 'state': row[3]}
        return None

    def set_state(self, user_id, state):
        self.cursor.execute('UPDATE users SET state=? WHERE user_id=?', (state, user_id))
        self.conn.commit()

    def update_period(self, user_id, last_period, cycle_length):
        self.cursor.execute('UPDATE users SET last_period=?, cycle_length=? WHERE user_id=?',
                            (last_period, cycle_length, user_id))
        self.conn.commit()

    # Mood methods
    def save_mood(self, user_id, date, mood):
        self.cursor.execute('INSERT INTO moods (user_id, date, mood) VALUES (?, ?, ?)',
                            (user_id, date, mood))
        self.conn.commit()

    def get_last_week_moods(self, user_id):
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.cursor.execute('SELECT mood FROM moods WHERE user_id=? AND date>=?', (user_id, one_week_ago))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    # Symptom methods
    def save_symptom(self, user_id, date, symptom):
        self.cursor.execute('INSERT INTO symptoms (user_id, date, symptom) VALUES (?, ?, ?)',
                            (user_id, date, symptom))
        self.conn.commit()

    def get_last_week_symptoms(self, user_id):
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.cursor.execute('SELECT symptom FROM symptoms WHERE user_id=? AND date>=?', (user_id, one_week_ago))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
