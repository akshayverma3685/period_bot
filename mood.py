from database import Database
db = Database()

def add_mood(user_id, emoji):
    db.add_mood(user_id, emoji)

def get_mood_stats(user_id):
    data = db.get_mood_stats(user_id)
    stats = {}
    for date, mood in data:
        stats[date] = mood
    return stats
