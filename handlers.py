# handlers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from utils import delete_message, delete_reply

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

    context.user_data['forwarded_message_id'] = forwarded_msg.message_id
    context.user_data['user_chat_id'] = update.effective_chat.id

# Replying to the user's message from the admin
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        return

    if 'forwarded_message_id' not in context.user_data:
        return

    reply_message = update.message.text
    user_chat_id = context.user_data['user_chat_id']

    sent_reply = await context.bot.send_message(
        chat_id=user_chat_id,
        text=f"Reply from admin: {reply_message}"
    )

    context.job_queue.run_once(delete_reply, timedelta(hours=2), context=sent_reply)
