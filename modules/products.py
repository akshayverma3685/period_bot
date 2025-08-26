# modules/products.py
import random

PRODUCTS = [
    "Heating pad 🌡️",
    "Herbal tea 🍵",
    "Menstrual cup 🩸",
    "Pain relief patch 💊",
    "Comfortable underwear 👙"
]

SELF_CARE_TIPS = [
    "Take warm baths 🛁",
    "Practice yoga stretches 🧘‍♀️",
    "Listen to calming music 🎶",
    "Rest when needed 😴",
    "Eat light and nutritious meals 🥗"
]

def get_product_suggestions():
    return '\n'.join(random.sample(PRODUCTS, 3))

def get_self_care_tips():
    return '\n'.join(random.sample(SELF_CARE_TIPS, 3))
