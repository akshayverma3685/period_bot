# modules/quiz.py
import random

QUIZZES = [
    {
        "question": "What is the average menstrual cycle length?",
        "options": ["21-35 days", "10-20 days", "36-45 days"],
        "answer": "21-35 days"
    },
    {
        "question": "Which nutrient is important during periods?",
        "options": ["Iron", "Vitamin C", "Calcium"],
        "answer": "Iron"
    },
    {
        "question": "Cramping can be relieved by?",
        "options": ["Stretching", "Skipping meals", "Excess caffeine"],
        "answer": "Stretching"
    }
]

def get_random_quiz():
    return random.choice(QUIZZES)
