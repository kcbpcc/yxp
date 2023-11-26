import os
import telegram
import asyncio
import pandas as pd

# Constants
BOT_TOKEN = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
USER_USERNAMES = '-4022487175'  # Replace with your Telegram username or ID


HEADER_LIST = ['qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'PnL%_H', 'dPnL%', 'product', 'source', 'key', 'pxy', 'yxp', 'PnL%', 'PnL%']
FILE_PATH = 'filePnL.csv'
BLOCK_FILE_PATH = 'telblock.txt'

def send_telegram_message(message_text, bot_token, user_usernames):
    try:
        # Function to send a message to Telegram
        async def send_message():
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=user_usernames, text=message_text)

        # Run the asyncio event loop directly with asyncio.run
        asyncio.run(send_message())
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

def process_new_rows(file_path, block_file_path, bot_token, user_usernames, header_list):
    # Read block file to get the list of already processed keys
    try:
        with open(block_file_path, 'r') as block_file:
            block_list = block_file.read().splitlines()
    except FileNotFoundError:
        block_list = []

    # Read the CSV file
    try:
        df = pd.read_csv(file_path, header=None, names=header_list)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Iterate over rows
    for index, row in df.iterrows():
        key = row['key']
        # Extract stock code from the 'key' column (removing 'NSE:' or 'BSE:')
        stock_code = key.split(':')[-1]

        if stock_code not in block_list:
            # Construct message text with row data and headers
            message_text = f"{', '.join([f'{header}: {value}' for header, value in zip(header_list, row.values)])} https://www.tradingview.com/chart/?symbol={stock_code}"
            
            # Send message to Telegram
            send_telegram_message(message_text, bot_token, user_usernames)

            # Append the processed stock code to block list
            with open(block_file_path, 'a') as block_file:
                block_file.write(stock_code + '\n')

# Execute the functionality
if __name__ == "__main__":
    process_new_rows(FILE_PATH, BLOCK_FILE_PATH, BOT_TOKEN, USER_USERNAMES, HEADER_LIST)



