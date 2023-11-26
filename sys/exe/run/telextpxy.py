import telegram
import asyncio

def send_telegram_notification(row, key):
    try:
        message_text = f"{str(row)} Symbol: {key} https://www.tradingview.com/chart/?symbol={key}"
        
        # Define the bot token and your Telegram username or ID
        bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
        user_usernames = ('-4022487175')  # Replace with your Telegram username or ID
        
        # Function to send a message to Telegram
        async def send_telegram_notification(message_text):
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=user_usernames, text=message_text)
        
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

    # Send the 'row' content as a message to Telegram immediately after printing the row
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_notification(message_text))

# Example of calling the function
if __name__ == "__main__":
    row_data = "Your Row Data"  # Replace with your actual row data
    key_data = "Your Key Data"  # Replace with your actual key data
    send_telegram_notification(row_data, key_data)
