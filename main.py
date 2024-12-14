import os
import logging
from pymongo import MongoClient
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load bot token, MongoDB URL, and admin ID from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the environment variables are loaded
if not BOT_TOKEN or not MONGO_URL or not ADMIN_ID:
    logger.error("Missing required environment variables: BOT_TOKEN, MONGO_URL, or ADMIN_ID.")
    exit(1)

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URL)
    db = client['telegram_bot']
    users_collection = db['users']
    logger.info("MongoDB connection established.")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    exit(1)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    first_name = update.effective_user.first_name

    # Check if user exists in DB, if not, save user
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id, "first_name": first_name})
        logger.info(f"New user added: {user_id}")

    await context.bot.send_message(chat_id=chat_id, text="Welcome to the bot! 🚀")

# Command: /broadcast (Admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <your message>")
        return

    message = " ".join(context.args)
    users = users_collection.find()

    for user in users:
        try:
            await context.bot.send_message(chat_id=user['user_id'], text=message)
        except Exception as e:
            logger.warning(f"Failed to send to {user['user_id']}: {e}")

    await update.message.reply_text("Broadcast completed!")

# Command: /users (Admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    count = users_collection.count_documents({})
    await update.message.reply_text(f"Total users: {count}")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))

    logger.info("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
