from database import Database
db = Database()

def generate_weekly_report(user_id):
    moods = db.get_mood_stats(user_id)
    symptoms = db.get_symptoms(user_id)
    report = "📊 Weekly Report:\n\nMoods:\n"
    for date, mood in moods[-7:]:
        report += f"{date}: {mood}\n"
    report += "\nSymptoms:\n"
    for date, symptom in symptoms[-7:]:
        report += f"{date}: {symptom}\n"
    return report
