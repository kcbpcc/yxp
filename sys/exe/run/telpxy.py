bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
chat_id = '-4022487175'  # Replace with your Telegram chat ID

import telegram
import asyncio
import pandas as pd
import os

# Function to read the contents of the CSV file
def read_csv(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.to_string(index=False)
    else:
        return "File not found."

# Define the bot token and your Telegram chat ID
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
chat_id = '-4022487175'  # Replace with your Telegram chat ID



# Function to send a message to Telegram
async def send_telegram_message(message_text):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message_text)

# Function to check for updates and send messages
async def check_and_send_updates(file_path):
    previous_contents = None
    current_contents = read_csv(file_path)

    if current_contents != previous_contents:
        try:
            message_text = f"Updated Contents:\n{current_contents}"
            await send_telegram_message(message_text)
            print("Content updated and sent to Telegram.")
            previous_contents = current_contents
        except Exception as e:
            print(f"Error sending message to Telegram: {e}")

async def main(file_path):
    await check_and_send_updates(file_path)

if __name__ == '__main__':
    file_path = 'filePnL.csv'  # Update with the path to your CSV file
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(file_path))
    loop.close()
