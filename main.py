from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ChatMemberHandler
from config import BOT_TOKEN
from handlers import start, forward_message_to_admin, reply_to_user
from handlers import broadcast, users, handle_user_blocked_or_deleted

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))  # Allows admin to reply to users
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users))

    # Handle user blocking or deleting the bot
    app.add_handler(ChatMemberHandler(handle_user_blocked_or_deleted, ChatMemberHandler.MY_CHAT_MEMBER))

    app.run_polling()

if __name__ == "__main__":
    main()
