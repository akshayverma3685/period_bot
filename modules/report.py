# modules/report.py
from modules.database import Database

def generate_weekly_report(user_id):
    db = Database('users.db')
    moods = db.get_last_week_moods(user_id)
    symptoms = db.get_last_week_symptoms(user_id)

    report = f"Moods last week: {', '.join(moods) if moods else 'No data'}\n"
    report += f"Symptoms last week: {', '.join(symptoms) if symptoms else 'No data'}"
    return report
