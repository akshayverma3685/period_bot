from datetime import datetime, timedelta

def generate_weekly_report(user_id, db=None):
    """
    Generates a simple weekly report of moods and symptoms.
    """
    if not db:
        return "Database not provided."
    
    try:
        rows = db.cursor.execute(
            "SELECT mood, symptoms FROM users WHERE user_id=?", (user_id,)
        ).fetchall()

        moods = []
        symptoms_list = []
        for row in rows:
            mood, symptoms = row[0], row[1]
            if mood:
                moods.append(mood)
            if symptoms:
                symptoms_list.append(symptoms)

        report_text = f"📝 Weekly Report for User {user_id}\n"
        report_text += f"- Mood entries: {', '.join(moods) if moods else 'No data'}\n"
        report_text += f"- Symptoms recorded: {', '.join(symptoms_list) if symptoms_list else 'No data'}\n"

        return report_text

    except Exception as e:
        return f"Error generating report: {e}"
