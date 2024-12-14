from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from utils import delete_message, delete_reply
from datetime import timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    image_url = "https://i.ibb.co/SB9XZ6Z/photo-2024-12-14-08-27-56-7448181445471764512.jpg"

    keyboard = [
        [InlineKeyboardButton("⚡Movie Link Here", url="https://t.me/Pushpa_Part_2_The_Rule_Tamil/20")],
        [InlineKeyboardButton("🎯Join Our Main Channel", url="https://t.me/FilesUlagam1")],
        [InlineKeyboardButton("🤗Group Link", url="https://t.me/+xR-e38apt6AxMmY1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent_message = await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption="Welcome to our Channel!🥳Here👇",
        reply_markup=reply_markup
    )

    # Schedule the deletion of the photo message after 2 minutes
    context.job_queue.run_once(delete_message, timedelta(minutes=2), context=sent_message)

# Forward the user's message to the admin
async def forward_message_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.full_name
    user_id = update.message.from_user.id

    forwarded_message = f"Message from {user_name} (ID: {user_id}):\n{user_message}"
    forwarded_msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=forwarded_message,
    )

    # Save the forwarded message ID and user's chat ID to reply later
    context.user_data['forwarded_message_id'] = forwarded_msg.message_id
    context.user_data['user_chat_id'] = update.effective_chat.id

# Replying to the user's message from the admin
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        return  # Only allow admin to reply

    # Check if the admin is replying to a forwarded message
    if 'forwarded_message_id' not in context.user_data:
        return  # No forwarded message to reply to

    reply_message = update.message.text
    user_chat_id = context.user_data['user_chat_id']

    try:
        sent_reply = await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"Reply from admin: {reply_message}"
        )

        # Schedule the deletion of the reply message after 2 hours
        context.job_queue.run_once(delete_reply, timedelta(hours=2), context=sent_reply)
    except Exception as e:
        logger.error(f"Failed to send reply to {user_chat_id}: {e}")

# Command: /broadcast (Admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
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
            logger.error(f"Failed to send to {user['user_id']}: {e}")

    await update.message.reply_text("Broadcast completed!")

# Command: /users (Admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    count = 0  # Replace with your user count logic
    await update.message.reply_text(f"Total users: {count}")

# Notify admin if the user blocks or deletes the bot
async def handle_user_blocked_or_deleted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.my_chat_member.from_user.full_name
    user_id = update.my_chat_member.from_user.id
    status = update.my_chat_member.new_chat_member.status

    if status in ["kicked", "left"]:
        notification_message = f"User {user_name} (ID: {user_id}) has either blocked or deleted the bot."
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=notification_message
            )
        except Exception as e:
            logger.error(f"Error notifying admin about user blocking/deleting: {e}")
