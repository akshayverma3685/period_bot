import asyncio
from datetime import datetime, timedelta

async def send_reminder(bot, user_id, message):
    await bot.send_message(user_id, message)

def schedule_reminders(bot, db):
    async def scheduler():
        while True:
            users = [db.get_user(row[0]) for row in db.cursor.execute("SELECT user_id FROM users")]
            today = datetime.now().strftime("%d-%m-%Y")
            for user in users:
                if user['last_period']:
                    next_period = datetime.strptime(user['last_period'], "%d-%m-%Y") + timedelta(days=user['cycle_length'] or 28)
                    reminder_day = (next_period - timedelta(days=1)).strftime("%d-%m-%Y")
                    if today == reminder_day:
                        await send_reminder(bot, user['user_id'], "⏰ Reminder: Your period may start tomorrow!")
            await asyncio.sleep(86400)
    asyncio.create_task(scheduler())
