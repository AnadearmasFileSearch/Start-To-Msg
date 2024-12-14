# Start-To-Msg Bot

A simple Telegram bot for broadcasting messages and managing users. Built with Python, MongoDB, and `python-telegram-bot`.

## Features:
- `/start`: Start the bot and receive a welcome message.
- `/broadcast <message>`: Admin-only command to send a message to all users.
- `/users`: Admin-only command to view the total number of users.

## Setup and Deployment

### Prerequisites
- Python 3.10+
- MongoDB Database
- Telegram Bot Token (from [BotFather](https://t.me/BotFather))

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Start-To-Msg.git
   cd Start-To-Msg

2. Install dependencies:

pip install -r requirements.txt


3. Add your bot token and MongoDB URL in config.py.


4. Run the bot:

python main.py



Deployment

You can deploy this bot using:

Heroku

Render

Koyeb

VPS or other hosting platforms.
