# modules/mood.py
from modules.database import Database

db = Database()

def add_mood(user_id: int, mood_emoji: str) -> str:
    """
    Save user's mood and return an acknowledgment message.
    """
    # Get existing moods
    user = db.get_user(user_id)
    previous_mood = user.get("mood", "")
    
    # Update mood in database
    db.update_user(user_id, mood=mood_emoji)
    
    # Return response
    mood_messages = {
        "😊": "Great to see you happy! Keep smiling 😄",
        "😐": "Feeling neutral today? Take some time for yourself!",
        "😔": "Feeling down? Try some relaxation or talk to a friend.",
        "😡": "Frustrated? Take deep breaths and relax your mind.",
        "😴": "Feeling tired? Ensure you get proper rest!"
    }
    return mood_messages.get(mood_emoji, "Mood recorded! Stay healthy 💖")
