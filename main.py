import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.database import Database
from modules.reminders import schedule_reminders
from modules.tips import get_daily_tip, get_educational_content
from modules.products import get_product_suggestions, get_self_care_tips
from modules.mood import add_mood
from modules.utils import calculate_next_period
from modules.ai_module import get_ai_advice
from modules.quiz import get_random_quiz
from modules.report import generate_weekly_report

API_TOKEN = "8418079716:AAGFB4SmVKq8DMzbNwz9Qlnr-Da4FAKv0sg"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.startup.register(lambda _: logging.info("Bot is starting..."))
dp.shutdown.register(lambda _: logging.info("Bot is stopping..."))

db = Database("users.db")

# Start command
@dp.message()
async def start_handler(message: types.Message):
    if message.text and message.text.lower() == "/start":
        user_id = message.from_user.id
        db.add_user(user_id)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Set Period", callback_data="set_period"),
             InlineKeyboardButton("Next Period", callback_data="next_period")],
            [InlineKeyboardButton("Symptoms / Tips", callback_data="symptoms"),
             InlineKeyboardButton("Mood Tracker", callback_data="mood")],
            [InlineKeyboardButton("Product Reminder", callback_data="product"),
             InlineKeyboardButton("Daily Tip", callback_data="daily_tip")],
            [InlineKeyboardButton("AI Advice", callback_data="ai_advice"),
             InlineKeyboardButton("Quiz", callback_data="quiz")],
            [InlineKeyboardButton("Weekly Report", callback_data="weekly_report")]
        ])
        await message.answer("👋 Welcome to LadyBuddy – your all-in-one menstrual health companion! Choose an option:", reply_markup=keyboard)

# Callback handler
@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data
    user = db.get_user(user_id)

    if data == "set_period":
        await callback_query.message.answer("Please send your last period date (DD-MM-YYYY)")
        db.set_state(user_id, "awaiting_period")

    elif data == "next_period":
        if user.get("last_period") and user.get("cycle_length"):
            next_period = calculate_next_period(user["last_period"], user["cycle_length"])
            await callback_query.message.answer(f"Your next period is expected on: {next_period}")
        else:
            await callback_query.message.answer("Please set your period first.")

    elif data == "symptoms":
        await callback_query.message.answer("Enter your symptoms today (e.g., cramps, headache):")
        db.set_state(user_id, "awaiting_symptoms")

    elif data == "mood":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(e, callback_data=f"mood_{e}") for e in ["😊","😐","😔","😡","😴"]]
        ])
        await callback_query.message.answer("How's your mood today?", reply_markup=keyboard)

    elif data == "product":
        products = get_product_suggestions()
        tips = get_self_care_tips()
        await callback_query.message.answer(f"🛒 Recommended products:\n{products}\n\nSelf-care tips:\n{tips}")

    elif data == "daily_tip":
        tip = get_daily_tip()
        edu = get_educational_content()
        await callback_query.message.answer(f"💡 Daily Tip:\n{tip}\n📚 Fact:\n{edu}")

    elif data == "ai_advice":
        advice = get_ai_advice()
        await callback_query.message.answer(f"🤖 AI Advice:\n{advice}")

    elif data == "quiz":
        quiz = get_random_quiz()
        options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(opt, callback_data=f"quiz_{opt}_{quiz['answer']}")] for opt in quiz["options"]
        ])
        await callback_query.message.answer(quiz["question"], reply_markup=options_keyboard)

    elif data.startswith("quiz_"):
        _, selected, answer = data.split("_")
        if selected == answer:
            await callback_query.message.answer("✅ Correct!")
        else:
            await callback_query.message.answer("❌ Wrong!")

    elif data == "weekly_report":
        report = generate_weekly_report(user_id)
        await callback_query.message.answer(f"📊 Your weekly report:\n{report}")

# Run bot as background worker
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
