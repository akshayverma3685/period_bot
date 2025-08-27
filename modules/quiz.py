import random

QUIZZES = [
    {
        "question": "Which nutrient is important to include during your period?",
        "options": ["Iron", "Sugar", "Salt", "Caffeine"],
        "answer": "Iron"
    },
    {
        "question": "What can help relieve menstrual cramps?",
        "options": ["Exercise", "Skipping meals", "Excess caffeine", "Smoking"],
        "answer": "Exercise"
    },
    {
        "question": "Average menstrual cycle length is usually:",
        "options": ["21-35 days", "10-15 days", "40-50 days", "60 days"],
        "answer": "21-35 days"
    },
    {
        "question": "Which of the following is eco-friendly?",
        "options": ["Menstrual cup", "Disposable pads", "Plastic tampons", "Paper towels"],
        "answer": "Menstrual cup"
    }
]

def get_random_quiz() -> dict:
    """
    Return a random quiz from the pool.
    """
    return random.choice(QUIZZES)
