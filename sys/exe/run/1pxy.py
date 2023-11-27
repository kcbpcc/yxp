import telegram

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'
user_usernames = ('-4022487175')

def send_message(bot, chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

def send_hello():
    # Initialize the Telegram bot
    bot_instance = telegram.Bot(token=bot_token)

    # Send the message to the specified user(s)
    for chat_id in user_usernames:
        send_message(bot_instance, chat_id, "Hello")

if __name__ == "__main__":
    send_hello()
