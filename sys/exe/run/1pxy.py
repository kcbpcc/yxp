import telegram

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'
user_usernames = ('-4022487175',)

def send_message(bot, chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

def send_messages():
    # Initialize the Telegram bot
    bot_instance = telegram.Bot(token=bot_token)

    # Iterate through user IDs
    for chat_id in user_usernames:
        try:
            # Send a simple test message
            send_message(bot_instance, chat_id, "Test Message")
            print(f"Sent message to chat_id: {chat_id}")
        except Exception as e:
            print(f"Error sending message to chat_id {chat_id}: {e}")

if __name__ == "__main__":
    send_messages()
