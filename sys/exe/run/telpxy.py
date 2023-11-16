import asyncio
from telegram import Bot
from telegram import ParseMode

# Move the token, usernames, and message_text definition here
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'
user_usernames = ('-4022487175')

async def create_message_text(row, key):
    return f"{str(row)} Symbol: {key} [TradingView Chart](https://www.tradingview.com/chart/?symbol={key})"

async def send_telegram_message(row, key):
    try:
        message_text = await create_message_text(row, key)
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=user_usernames, text=message_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

# Usage example
async def main():
    # Example data
    row_data = "Some data"
    key_data = "BTCUSD"

    # Call the asynchronous function
    await send_telegram_message(row_data, key_data)

# Run the event loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
