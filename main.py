# main.py
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from database import Database
from reminders import schedule_reminders
from tips import get_daily_tip
from products import get_product_suggestions
from mood import add_mood, get_mood_stats
from utils import calculate_next_period

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

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
        InlineKeyboardButton("Check Next Period", callback_data="next_period"),
        InlineKeyboardButton("Symptoms / Tips", callback_data="symptoms"),
        InlineKeyboardButton("Mood Tracker", callback_data="mood"),
        InlineKeyboardButton("Product Reminder", callback_data="product")
    )
    await message.answer("👋 Welcome to the All-in-One Period Bot! Choose an option:", reply_markup=keyboard)

# Callback query handler for inline buttons
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "set_period":
        await bot.send_message(user_id, "Please send your last period date in format DD-MM-YYYY")
        db.set_state(user_id, "awaiting_period")
    elif data == "next_period":
        user = db.get_user(user_id)
        if user.get('last_period') and user.get('cycle_length'):
            next_period = calculate_next_period(user['last_period'], user['cycle_length'])
            await bot.send_message(user_id, f"Your next period is expected on: {next_period}")
        else:
            await bot.send_message(user_id, "Please set your period first using 'Set Period'.")
    elif data == "symptoms":
        await bot.send_message(user_id, "Please enter your symptoms today (e.g., cramps, headache):")
        db.set_state(user_id, "awaiting_symptoms")
    elif data == "mood":
        keyboard = InlineKeyboardMarkup(row_width=5)
        for emoji in ["😊","😐","😔","😡","😴"]:
            keyboard.insert(InlineKeyboardButton(emoji, callback_data=f"mood_{emoji}"))
        await bot.send_message(user_id, "How's your mood today?", reply_markup=keyboard)
    elif data == "product":
        products = get_product_suggestions()
        await bot.send_message(user_id, f"🛒 Recommended products:\n{products}")

# Handle user text input
@dp.message_handler(lambda message: db.get_state(message.from_user.id) == "awaiting_period")
async def period_input(message: types.Message):
    user_id = message.from_user.id
    try:
        day, month, year = map(int, message.text.split('-'))
        db.set_period(user_id, message.text)
        await message.reply("✅ Last period date saved! Now set your cycle length using /setcycle command.")
        db.set_state(user_id, None)
    except:
        await message.reply("❌ Invalid format! Please use DD-MM-YYYY")

@dp.message_handler(lambda message: db.get_state(message.from_user.id) == "awaiting_symptoms")
async def symptom_input(message: types.Message):
    user_id = message.from_user.id
    symptoms = message.text
    tip = get_daily_tip(symptoms)
    await message.reply(f"💡 Advice for your symptoms:\n{tip}")
    db.set_state(user_id, None)

# Handle mood buttons
@dp.callback_query_handler(lambda c: c.data.startswith('mood_'))
async def mood_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    emoji = callback_query.data.split("_")[1]
    add_mood(user_id, emoji)
    await bot.send_message(user_id, f"Your mood {emoji} has been recorded!")

# Start reminders scheduler
schedule_reminders(bot, db)

# Run bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
