# telegram_notification.py

import asyncio
from telegram import Bot
from telegram import ParseMode

# Move the token, usernames, and message_text definition here
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'
user_usernames = '-4022487175'

async def send_telegram_notification(row, key):
    async def create_message_text(row, key):
        return f"{str(row)} Symbol: {key} [TradingView Chart](https://www.tradingview.com/chart/?symbol={key})"

    try:
        message_text = await create_message_text(row, key)
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=user_usernames, text=message_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")
