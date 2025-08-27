import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# --- Import your modules ---
from modules.database import Database
from modules.reminders import schedule_reminders
from modules.tips import get_daily_tip, get_educational_content
from modules.products import get_product_suggestions, get_self_care_tips
from modules.mood import add_mood
from modules.utils import calculate_next_period
from modules.ai_module import get_ai_advice
from modules.quiz import get_random_quiz
from modules.report import generate_weekly_report

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Telegram Bot token ---
API_TOKEN = "8247111109:AAFXtTZ9ChI2L4Dvvb7VwbwW9VUeyOX7XkY"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
db = Database("users.db")

# --- Start command ---
@dp.message()
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    db.add_user(user_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Set Period", callback_data="set_period"),
             InlineKeyboardButton("Next Period", callback_data="next_period")],
            [InlineKeyboardButton("Symptoms / Tips", callback_data="symptoms"),
             InlineKeyboardButton("Mood Tracker", callback_data="mood")],
            [InlineKeyboardButton("Product Reminder", callback_data="product"),
             InlineKeyboardButton("Daily Tip", callback_data="daily_tip")],
            [InlineKeyboardButton("AI Advice", callback_data="ai_advice"),
             InlineKeyboardButton("Quiz", callback_data="quiz")],
            [InlineKeyboardButton("Weekly Report", callback_data="weekly_report")]
        ]
    )

    await message.answer(
        "👋 Welcome to LadyBuddy – your all-in-one menstrual health companion! Choose an option:",
        reply_markup=keyboard
    )

# --- Callback handler ---
@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data
    user = db.get_user(user_id)

    try:
        if data == "set_period":
            await bot.send_message(user_id, "Please send your last period date (DD-MM-YYYY)")
            db.set_state(user_id, "awaiting_period")

        elif data == "next_period":
            if user.get("last_period") and user.get("cycle_length"):
                next_period = calculate_next_period(user["last_period"], user["cycle_length"])
                await bot.send_message(user_id, f"Your next period is expected on: {next_period}")
            else:
                await bot.send_message(user_id, "Please set your period first.")

        elif data == "symptoms":
            await bot.send_message(user_id, "Enter your symptoms today (e.g., cramps, headache):")
            db.set_state(user_id, "awaiting_symptoms")

        elif data == "mood":
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(emoji, callback_data=f"mood_{emoji}") 
                                  for emoji in ["😊","😐","😔","😡","😴"]]]
            )
            await bot.send_message(user_id, "How's your mood today?", reply_markup=keyboard)

        elif data == "product":
            products = get_product_suggestions()
            tips = get_self_care_tips()
            await bot.send_message(user_id, f"🛒 Recommended products:\n{products}\n\nSelf-care tips:\n{tips}")

        elif data == "daily_tip":
            tip = get_daily_tip()
            edu = get_educational_content()
            await bot.send_message(user_id, f"💡 Daily Tip:\n{tip}\n📚 Fact:\n{edu}")

        elif data == "ai_advice":
            advice = get_ai_advice()
            await bot.send_message(user_id, f"🤖 AI Advice:\n{advice}")

        elif data == "quiz":
            quiz = get_random_quiz()
            options_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}_{quiz['answer']}")] 
                                 for opt in quiz["options"]]
            )
            await bot.send_message(user_id, quiz["question"], reply_markup=options_keyboard)

        elif data.startswith("quiz_"):
            _, selected, answer = data.split("_")
            if selected == answer:
                await bot.send_message(user_id, "✅ Correct!")
            else:
                await bot.send_message(user_id, "❌ Wrong!")

        elif data == "weekly_report":
            report = generate_weekly_report(user_id)
            await bot.send_message(user_id, f"📊 Your weekly report:\n{report}")

    except Exception as e:
        await bot.send_message(user_id, f"Error: {str(e)}")

# --- Dummy web server for Render free plan ---
PORT = 10000

async def handle_root(request):
    return web.Response(text="Bot is running...")

app = web.Application()
app.router.add_get("/", handle_root)

async def start_web_app():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

# --- Start bot and dummy server ---
async def main():
    await start_web_app()
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    print("Bot is running... ✅")
    asyncio.run(main())
