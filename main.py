import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load bot token from environment variable (for security)
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # Store your admin ID for forwarding messages

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Define the image URL or file path
    image_url = "https://i.ibb.co/BZkwHP7/photo-2024-12-13-08-36-29-7448177433972310020.jpg"  # Replace with your image URL

    # Create inline buttons
    keyboard = [
        [InlineKeyboardButton("Join Our Main Channel", url="https://t.me/FilesUlagam1")],
        [InlineKeyboardButton("Join Our Group", url="https://t.me/+xR-e38apt6AxMmY1")],
        [InlineKeyboardButton("Movie Link", url="https://t.me/FilesUlagam1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the image and buttons
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,  # You can also use an image file instead of a URL
        caption="Welcome to our bot! Choose an option below:",
        reply_markup=reply_markup
    )

# Forward the user's message to the admin
async def forward_message_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.full_name
    user_id = update.message.from_user.id

    # Forward the message to the admin (you can customize the message you forward)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Message from {user_name} (ID: {user_id}):\n{user_message}",
    )

# Command: /broadcast (Admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <your message>")
        return

    message = " ".join(context.args)
    # Add your user list logic to get all users
    users = []  # Replace with your user list logic

    for user in users:
        try:
            await context.bot.send_message(chat_id=user['user_id'], text=message)
        except Exception as e:
            logger.warning(f"Failed to send to {user['user_id']}: {e}")

    await update.message.reply_text("Broadcast completed!")

# Command: /users (Admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    count = 0  # Replace with your user count logic
    await update.message.reply_text(f"Total users: {count}")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))  # Forward all text messages to the admin
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))

    logger.info("Bot started...")
    app.run_polling()  # Keep polling for messages without the need for a public endpoint

if __name__ == "__main__":
    main()
