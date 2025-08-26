SYMPTOM_TIPS = {
    "cramps": "Use a hot water bottle on your lower abdomen and do light exercise.",
    "headache": "Drink plenty of water and try relaxation techniques.",
    "acne": "Maintain hygiene and drink lots of water. Avoid oily foods.",
    "mood swings": "Try meditation or short walks. Rest well."
}

DAILY_TIPS = [
    "Drink 8 glasses of water daily during your cycle.",
    "Include iron-rich foods like spinach and nuts.",
    "Gentle exercises reduce cramps and improve mood.",
    "Track your cycle to understand your body better."
]

import random

def get_daily_tip(symptom=None):
    if symptom and symptom.lower() in SYMPTOM_TIPS:
        return SYMPTOM_TIPS[symptom.lower()]
    return random.choice(DAILY_TIPS)
