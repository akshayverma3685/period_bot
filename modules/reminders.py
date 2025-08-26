# modules/reminders.py
import asyncio
from datetime import datetime, timedelta

async def send_period_reminder(bot, user_id, message: str):
    """
    Sends a reminder message to the user.
    """
    try:
        await bot.send_message(user_id, f"⏰ Reminder: {message}")
    except Exception as e:
        print(f"Failed to send reminder to {user_id}: {e}")

def schedule_reminders(bot, db):
    """
    Schedule reminders for all users based on their cycle.
    This should be called once at bot startup.
    """
    async def reminder_loop():
        while True:
            users = db.cursor.execute("SELECT user_id, last_period, cycle_length FROM users").fetchall()
            for user in users:
                user_id, last_period, cycle_length = user
                if last_period and cycle_length:
                    try:
                        last_date = datetime.strptime(last_period, "%d-%m-%Y")
                        next_period = last_date + timedelta(days=cycle_length)
                        today = datetime.now()
                        # Send reminder 2 days before period
                        if 0 <= (next_period - today).days <= 2:
                            await send_period_reminder(bot, user_id, "Your period is coming soon! 🌸")
                    except:
                        continue
            await asyncio.sleep(60 * 60)  # Check every hour

    asyncio.create_task(reminder_loop())
