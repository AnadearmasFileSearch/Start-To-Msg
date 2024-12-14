import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# Load bot token from environment variable (for security)
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = os.getenv("PORT", 8080)  # Default to 8080 if no port is set

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    first_name = update.effective_user.first_name

    await context.bot.send_message(chat_id=chat_id, text="Welcome to the bot! 🚀")

# Command: /broadcast (Admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is an admin
    admin_id = os.getenv("ADMIN_ID")
    if update.effective_user.id != int(admin_id):
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <your message>")
        return

    message = " ".join(context.args)
    users = []  # Replace with your user list logic

    for user in users:
        try:
            await context.bot.send_message(chat_id=user['user_id'], text=message)
        except Exception as e:
            logger.warning(f"Failed to send to {user['user_id']}: {e}")

    await update.message.reply_text("Broadcast completed!")

# Command: /users (Admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is an admin
    admin_id = os.getenv("ADMIN_ID")
    if update.effective_user.id != int(admin_id):
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    count = 0  # Replace with your user count logic
    await update.message.reply_text(f"Total users: {count}")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))

    logger.info("Bot started...")
    app.run_polling()  # No need to specify the port here

if __name__ == "__main__":
    main()
