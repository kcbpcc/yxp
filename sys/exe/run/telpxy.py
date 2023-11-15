# telpxy.py

import telegram

# Move the token, usernames, and message_text definition here
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'
user_usernames = ('-4022487175')

def create_message_text(row, key):
    return f"{str(row)} Symbol: {key} https://www.tradingview.com/chart/?symbol={key}"

def send_telegram_message(row, key):
    try:
        message_text = create_message_text(row, key)
        bot = telegram.Bot(token=bot_token)
        bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")
