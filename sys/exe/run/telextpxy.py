import pandas as pd
from telegram import Bot, ParseMode
from telegram.error import Unauthorized

def send_messages(bot_token, user_usernames, csv_file_path='PnL.csv', telblock_file='telblock.txt'):
    # Read CSV file
    df = pd.read_csv(csv_file_path)

    # Check for headers in the CSV file
    required_headers = ['qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'PnL%_H', 'dPnL%', 'product', 'source', 'key', 'pxy', 'yxp', 'PnL%']
    missing_headers = set(required_headers) - set(df.columns)

    # If there are missing headers, raise an exception or fix them programmatically
    if missing_headers:
        raise ValueError(f"Missing headers in CSV file: {missing_headers}")

    # Read telblock.txt to keep track of sent messages
    try:
        with open(telblock_file, 'r') as f:
            telblock = set(map(str.strip, f.readlines()))
    except FileNotFoundError:
        telblock = set()

    # Initialize the Telegram bot
    bot = Bot(token=bot_token)

    # Iterate through rows in the DataFrame
    for _, row in df.iterrows():
        # Construct message from the row data
        message = "\n".join(f"{header}: {value}" for header, value in row.items())

        # Check if the message has been sent before
        if message in telblock:
            continue

        # Send the message to the specified user(s)
        for username in user_usernames:
            try:
                bot.send_message(chat_id=username, text=message, parse_mode=ParseMode.MARKDOWN)
            except Unauthorized:
                print(f"Unauthorized: Could not send message to user {username}")

        # Record the sent message in telblock.txt to avoid double sending
        telblock.add(message)

    # Update telblock.txt with the new messages
    with open(telblock_file, 'w') as f:
        f.write("\n".join(telblock))

if __name__ == "__main__":
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    send_messages('6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo', ('-4022487175'))




