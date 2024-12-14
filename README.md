# Start-To-Msg
A simple Telegram bot with broadcasting, user management, and MongoDB support.

# Telegram Bot with MongoDB

A simple Telegram bot that allows admin-only broadcasting to users, stores messages in MongoDB, and provides user management features.

---

## Features
- **Admin-only commands**: `/broadcast`, `/status`, `/users`.
- **User functionality**: `/start` command to register users.
- **Broadcasting**: Admin can send messages to all users.
- **Database**: MongoDB for storing user data and messages.

---

## Prerequisites
1. [Create a bot](https://core.telegram.org/bots#6-botfather) on Telegram via BotFather and get your bot token.
2. Set up MongoDB:
   - Use a [local MongoDB server](https://www.mongodb.com/docs/manual/installation/) or a [MongoDB Atlas cluster](https://www.mongodb.com/atlas/database).
3. Python 3.7 or higher installed locally or on your hosting environment.

---

## Deployment Options

### 1. Local Deployment
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
