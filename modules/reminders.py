# modules/reminders.py
import asyncio

async def schedule_reminders(bot, user_id, message, delay_seconds):
    """
    Schedule a reminder after delay_seconds
    """
    await asyncio.sleep(delay_seconds)
    await bot.send_message(user_id, message)
