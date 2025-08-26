# modules/tips.py
import random

DAILY_TIPS = [
    "Stay hydrated 💧",
    "Do light exercises 🏃‍♀️",
    "Meditate for 10 minutes 🧘‍♀️",
    "Eat iron-rich food 🥦",
    "Maintain a sleep schedule 💤"
]

EDUCATIONAL_CONTENT = [
    "Menstrual cycles vary between 21-35 days.",
    "Tracking your period helps understand fertility.",
    "Mood swings are normal due to hormone changes.",
    "Cramping can be relieved with gentle stretching.",
    "Iron and protein intake is important during periods."
]

def get_daily_tip():
    return random.choice(DAILY_TIPS)

def get_educational_content():
    return random.choice(EDUCATIONAL_CONTENT)
