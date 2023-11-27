import os
import warnings
import telegram
import pandas as pd
import time  # Import the time module for adding delays

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'
user_usernames = ('-4022487175')

def send_message(bot, chat_id, text):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')

def send_messages():
    # Read CSV file
    csv_file_path = 'filePnL.csv'
    df = pd.read_csv(csv_file_path)

    # Read telblock.txt to keep track of sent messages
    try:
        with open('telblock.txt', 'r') as f:
            telblock = set(map(str.strip, f.readlines()))
    except FileNotFoundError:
        telblock = set()

    # Initialize the Telegram bot
    bot_instance = telegram.Bot(token=bot_token)

    # Iterate through rows in the DataFrame
    for _, row in df.iterrows():
        # Construct message from the row data
        message = "\n".join(f"{header}: {value}" for header, value in row.items())

        # Check if the message has been sent before
        if message in telblock:
            continue

        # Send the message to the specified user(s)
        for chat_id in user_usernames:
            print(f"Sending message to chat_id: {chat_id}")
            send_message(bot_instance, chat_id, message)
            time.sleep(1)  # Add a 1-second delay between messages

        # Record the sent message in telblock.txt to avoid double sending
        telblock.add(message)

    # Update telblock.txt with the new messages
    with open('telblock.txt', 'w') as f:
        f.write("\n".join(telblock))

if __name__ == "__main__":
    print("Start sending messages")
    send_messages()
    print("Finished sending messages")

