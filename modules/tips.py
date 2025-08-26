import random

SYMPTOM_TIPS = {
    "cramps": "Use a hot water bottle and gentle stretches.",
    "headache": "Drink water and try meditation.",
    "acne": "Maintain hygiene and drink lots of water.",
    "mood swings": "Try deep breathing and relaxation."
}

DAILY_TIPS = [
    "Drink 8 glasses of water daily.",
    "Include iron-rich foods like spinach, nuts.",
    "Gentle exercises reduce cramps and improve mood.",
    "Track your cycle to understand your body better."
]

EDUCATIONAL_CONTENT = [
    "Did you know? A normal cycle length is 21-35 days.",
    "Exercise during periods can relieve cramps.",
    "Balanced diet helps regulate your cycle.",
]

def get_daily_tip(symptom=None):
    if symptom and symptom.lower() in SYMPTOM_TIPS:
        return SYMPTOM_TIPS[symptom.lower()]
    return random.choice(DAILY_TIPS)

def get_educational_content():
    return random.choice(EDUCATIONAL_CONTENT)
