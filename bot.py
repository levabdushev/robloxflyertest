import json
import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==== Загрузка конфигурации ====
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

TOKEN = cfg["BOT_TOKEN"]
COMMANDS_FILE = "commands.json"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==== Создание файла команд, если его нет ====
if not os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)

def update_command(username, command):
    """Записывает команду для игрока"""
    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[username] = command
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ==== Стартовое сообщение ====
@dp.message(F.text.startswith("/start"))
async def start(msg: types.Message):
    await msg.answer("✅ Бот запущен!\nИспользуйте `/user <RobloxName>` для управления игроком.", parse_mode="Markdown")

# ==== Команда /user для управления игроком ====
@dp.message(F.text.startswith("/user"))
async def user_control(msg: types.Message):
    args = msg.text.split()
    if len(args) != 2:
        await msg.answer("Использование: `/user <RobloxName>`", parse_mode="Markdown")
        return

    username = args[1]

    # Кнопки троллинга
    buttons = [
        [InlineKeyboardButton(text="🟢 Jump", callback_data=f"jump:{username}")],
        [InlineKeyboardButton(text="💀 Kill", callback_data=f"kill:{username}")],
        [InlineKeyboardButton(text="⚡ Glitch Screen", callback_data=f"glitch:{username}")],
        [InlineKeyboardButton(text="🔒 Lock Screen", callback_data=f"lock:{username}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await msg.answer(f"🎮 Действия для **{username}**:", reply_markup=keyboard, parse_mode="Markdown")

# ==== Обработка нажатий кнопок ====
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    command, username = callback.data.split(":")
    update_command(username, command)
    await callback.answer(f"Команда '{command}' отправлена {username}!")

# ==== Главная функция запуска бота ====
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())