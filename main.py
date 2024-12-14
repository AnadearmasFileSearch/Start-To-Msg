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
    print(f"Received /start command from chat {chat_id}")  # Debug: Print chat ID

    # Define the image URL or file path
    image_url = "https://i.ibb.co/SB9XZ6Z/photo-2024-12-14-08-27-56-7448181445471764512.jpg"  # Replace with your image URL

    # Create inline buttons
    keyboard = [
        [InlineKeyboardButton("⚡Movie Link Here", url="https://t.me/Pushpa_Part_2_The_Rule_Tamil/20")],
        [InlineKeyboardButton("🎯Join Our Main Channel", url="https://t.me/FilesUlagam1")],
        [InlineKeyboardButton("🤗Group Link", url="https://t.me/+xR-e38apt6AxMmY1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the image and buttons
    print(f"Sending welcome message and buttons to chat {chat_id}")  # Debug: Confirm sending message
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,  # You can also use an image file instead of a URL
        caption="Welcome to our Channel!🥳Here👇",
        reply_markup=reply_markup
    )

# Forward the user's message to the admin
async def forward_message_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.full_name
    user_id = update.message.from_user.id

    print(f"Forwarding message from {user_name} (ID: {user_id}): {user_message}")  # Debug: Log the message

    # Forward the message to the admin (you can customize the message you forward)
    forwarded_message = f"Message from {user_name} (ID: {user_id}):\n{user_message}"
    forwarded_msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=forwarded_message,
    )

    # Save the message ID for replying later
    context.user_data['forwarded_message_id'] = forwarded_msg.message_id
    context.user_data['user_chat_id'] = update.effective_chat.id

# Replying to the user's message from the admin
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        print(f"Unauthorized reply attempt by user {update.effective_user.id}")  # Debug: Unauthorized reply attempt
        return  # Only allow admin to reply

    # Check if the admin is replying to a forwarded message
    if 'forwarded_message_id' not in context.user_data:
        print("No forwarded message to reply to.")  # Debug: No forwarded message
        return  # No forwarded message to reply to

    reply_message = update.message.text
    user_chat_id = context.user_data['user_chat_id']

    # Send the admin's reply back to the user
    await context.bot.send_message(
        chat_id=user_chat_id,
        text=f"Reply from admin: {reply_message}"
    )

    print(f"Reply sent to user {user_chat_id}: {reply_message}")  # Debug: Log the reply action

# Command: /broadcast (Admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("Unauthorized! Admins only.")
        print(f"Unauthorized access attempt by user {update.effective_user.id}")  # Debug: Log unauthorized access
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <your message>")
        print("Broadcast command received without message")  # Debug: Log when no message is provided
        return

    message = " ".join(context.args)
    # Add your user list logic to get all users
    users = []  # Replace with your user list logic

    print(f"Broadcasting message to {len(users)} users")  # Debug: Log how many users will receive the message
    for user in users:
        try:
            await context.bot.send_message(chat_id=user['user_id'], text=message)
        except Exception as e:
            logger.warning(f"Failed to send to {user['user_id']}: {e}")

    await update.message.reply_text("Broadcast completed!")
    print("Broadcast completed!")  # Debug: Log when broadcast is completed

# Command: /users (Admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("Unauthorized! Admins only.")
        print(f"Unauthorized access attempt by user {update.effective_user.id}")  # Debug: Log unauthorized access
        return

    count = 0  # Replace with your user count logic
    print(f"Sending user count: {count}")  # Debug: Log the user count
    await update.message.reply_text(f"Total users: {count}")

# Main function
def main():
    print("Starting the bot...")  # Debug: Log when the bot starts

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    print("Application built successfully")  # Debug: Log when the application is built

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))  # Forward all text messages to the admin
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))  # Allow admin to reply to users
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))

    print("Handlers added successfully")  # Debug: Log after adding handlers

    # Start the bot and begin polling
    print("Bot is now polling...")  # Debug: Log when polling starts
    app.run_polling()

if __name__ == "__main__":
    main()
