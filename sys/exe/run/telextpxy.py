import os
import telegram
import asyncio
import pandas as pd

# Constants
BOT_TOKEN = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
USER_USERNAMES = '-4022487175'  # Replace with your Telegram username or ID

def send_telegram_message(message_text, bot_token, user_usernames):
    try:
        # Function to send a message to Telegram
        async def send_message():
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=user_usernames, text=message_text)

        # Send the message to Telegram
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_message())
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

def process_new_rows(file_path, telblock_path, bot_token, user_usernames):
    # Read telblock file to get the list of already processed keys
    try:
        with open(telblock_path, 'r') as telblock_file:
            telblock = telblock_file.read().splitlines()
    except FileNotFoundError:
        telblock = []

    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Check if 'key' is in the DataFrame columns
    if 'key' not in df.columns:
        print("Error: 'key' not found in DataFrame columns.")
        return

    # Iterate over rows
    for index, row in df.iterrows():
        # Assuming 'key' is the column containing key information
        key_parts = row['key'].split(':')

        # Construct the message using provided headers as keys
        message_text = f"{' | '.join([f'{header}: {row[header]}' for header in ['qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'PnL%_H', 'dPnL%', 'product', 'source', 'key', 'pxy', 'yxp', 'PnL%', 'PnL']])} | https://www.tradingview.com/chart/?symbol={key_parts[0]}"

        if key_parts[0] not in telblock:
            send_telegram_message(message_text, bot_token, user_usernames)
            # Append the processed key to telblock
            with open(telblock_path, 'a') as telblock_file:
                telblock_file.write(key_parts[0] + '\n')

# File paths
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, 'filePnL.csv')
TELBLOCK_PATH = os.path.join(CURRENT_DIR, 'telblock.txt')

# Execute the functionality automatically
process_new_rows(FILE_PATH, TELBLOCK_PATH, BOT_TOKEN, USER_USERNAMES)





