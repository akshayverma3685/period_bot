QUIZZES = [
    {"question": "What is a normal menstrual cycle length?", "options": ["21-35 days","10-20 days","40-50 days"], "answer": "21-35 days"},
    {"question": "Does exercise help relieve cramps?", "options": ["Yes","No"], "answer": "Yes"}
]

def get_random_quiz():
    import random
    return random.choice(QUIZZES)
