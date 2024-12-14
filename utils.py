# utils.py
from datetime import timedelta

# Function to delete the photo or any message
async def delete_message(context):
    message = context.job.context
    await context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    print(f"Deleted message {message.message_id}")  # Debug: Log the deletion

# Function to delete the reply message after 2 hours
async def delete_reply(context):
    message = context.job.context
    await context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    print(f"Deleted reply message {message.message_id}")  # Debug: Log the deletion
