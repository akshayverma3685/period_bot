# modules/mood.py
from modules.database import Database
from modules.utils import get_today_date

def add_mood(user_id, mood):
    db = Database('users.db')
    user = db.get_user(user_id)
    if not user:
        return False

    today = get_today_date()
    db.save_mood(user_id, today, mood)

    moods = db.get_last_week_moods(user_id)
    if moods.count('😔') >= 3 or moods.count('😡') >= 2:
        return "We noticed you've been down lately. Try some self-care or relaxation activities! 💖"

    return True
