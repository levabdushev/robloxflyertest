import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# === Загружаем настройки ===
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

TOKEN = cfg["BOT_TOKEN"]
COMMANDS_FILE = "commands.json"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создаем файл команд, если его нет
if not os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)

def update_command(username, command):
    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[username] = command
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("✅ Бот запущен! Используйте /user <RobloxName> для управления игроком.")

@dp.message_handler(commands=['user'])
async def user_control(msg: types.Message):
    args = msg.get_args().split()
    if len(args) != 1:
        await msg.answer("Использование: /user <RobloxName>")
        return

    username = args[0]

    buttons = [
        [types.InlineKeyboardButton("🟢 Jump", callback_data=f"jump:{username}")],
        [types.InlineKeyboardButton("💀 Kill", callback_data=f"kill:{username}")],
        [types.InlineKeyboardButton("⚡ Glitch Screen", callback_data=f"glitch:{username}")],
        [types.InlineKeyboardButton("🔒 Lock Screen", callback_data=f"lock:{username}")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await msg.answer(f"🎮 Действия для **{username}**:", reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query_handler()
async def callbacks(callback: types.CallbackQuery):
    command, username = callback.data.split(":")
    update_command(username, command)
    await callback.answer(f"Команда '{command}' отправлена {username}!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)