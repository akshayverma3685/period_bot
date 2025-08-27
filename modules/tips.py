import random

DAILY_TIPS = [
    "💧 Stay hydrated to ease cramps and bloating.",
    "🥗 Include iron-rich foods like spinach and nuts in your diet.",
    "🛌 Ensure at least 7-8 hours of sleep every night.",
    "🏃 Gentle exercises like yoga or walking help relieve discomfort.",
    "🧘‍♀️ Practice deep breathing or meditation for stress relief."
]

EDUCATIONAL_CONTENT = [
    "📚 Menstrual cycles are usually 28 days but can vary between 21-35 days.",
    "📚 PMS symptoms are normal and can include mood swings, cramps, and fatigue.",
    "📚 Tracking your period helps in identifying irregularities early.",
    "📚 Using menstrual cups is eco-friendly and can save money over time.",
    "📚 Pain during periods can be reduced with heat therapy and light exercise."
]

def get_daily_tip() -> str:
    """Return a random daily tip."""
    return random.choice(DAILY_TIPS)

def get_educational_content() -> str:
    """Return a random educational fact."""
    return random.choice(EDUCATIONAL_CONTENT)
