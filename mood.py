from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from database import Database
from reminders import schedule_reminders
from tips import get_daily_tip, get_educational_content
from products import get_product_suggestions, get_self_care_tips
from mood import add_mood
from utils import calculate_next_period
from ai_module import get_ai_advice
from quiz import get_random_quiz
from report import generate_weekly_report

API_TOKEN = '8418079716:AAGFB4SmVKq8DMzbNwz9Qlnr-Da4FAKv0sg'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = Database('users.db')

# Start command
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    db.add_user(user_id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Set Period", callback_data="set_period"),
        InlineKeyboardButton("Next Period", callback_data="next_period"),
        InlineKeyboardButton("Symptoms / Tips", callback_data="symptoms"),
        InlineKeyboardButton("Mood Tracker", callback_data="mood"),
        InlineKeyboardButton("Product Reminder", callback_data="product"),
        InlineKeyboardButton("Daily Tip", callback_data="daily_tip"),
        InlineKeyboardButton("Quiz", callback_data="quiz"),
        InlineKeyboardButton("Weekly Report", callback_data="weekly_report")
    )
    await message.answer("👋 Welcome to LadyBuddy – your all-in-one menstrual health companion! Choose an option:", reply_markup=keyboard)

# Callback query handler
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data
    user = db.get_user(user_id)

    if data == "set_period":
        await bot.send_message(user_id, "Please send your last period date (DD-MM-YYYY)")
        db.set_state(user_id, "awaiting_period")

    elif data == "next_period":
        if user.get('last_period') and user.get('cycle_length'):
            next_period = calculate_next_period(user['last_period'], user['cycle_length'])
            await bot.send_message(user_id, f"Your next period is expected on: {next_period}")
        else:
            await bot.send_message(user_id, "Please set your period first.")

    elif data == "symptoms":
        await bot.send_message(user_id, "Enter your symptoms today (e.g., cramps, headache):")
        db.set_state(user_id, "awaiting_symptoms")

    elif data == "mood":
        keyboard = InlineKeyboardMarkup(row_width=5)
        for emoji in ["😊","😐","😔","😡","😴"]:
            keyboard.insert(InlineKeyboardButton(emoji, callback_data=f"mood_{emoji}"))
        await bot.send_message(user_id, "How's your mood today?", reply_markup=keyboard)

    elif data == "product":
        products = get_product_suggestions()
        tips = get_self_care_tips()
        await bot.send_message(user_id, f"🛒 Recommended products:\n{products}\n\nSelf-care tips:\n{tips}")

    elif data == "daily_tip":
        tip = get_daily_tip()
        edu = get_educational_content()
        await bot.send_message(user_id, f"💡 Daily Tip:\n{tip}\n📚 Fact:\n{edu}")

    elif data == "quiz":
        quiz = get_random_quiz()
        options_keyboard = InlineKeyboardMarkup(row_width=1)
        for opt in quiz['options']:
            options_keyboard.insert(InlineKeyboardButton(opt, callback_data=f"quiz_{opt}_{quiz['answer']}"))
        await bot.send_message(user_id, quiz['question'], reply_markup=options_keyboard)

    elif data.startswith("quiz_"):
        _, selected, answer = data.split("_")
        if selected == answer:
            await bot.send_message(user_id, "✅ Correct!")
        else:
            await bot.send_message(user_id, "❌ Wrong!")

    elif data == "weekly_report":
        report = generate_weekly_report(user_id)
        await bot.send_message(user_id, f"📊 Your weekly report:\n{report}")

# Start polling (aiogram v3.22+ compatible)
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling())
