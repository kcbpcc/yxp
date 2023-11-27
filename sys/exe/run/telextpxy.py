import pandas as pd
import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'
user_usernames = ('-4022487175')

def send_message(chat_id, text):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    response = requests.post(api_url, params=params)

    if response.status_code != 200:
        print(f"Failed to send message to {chat_id}. Status code: {response.status_code}")
        print(response.text)

def send_messages():
    # Read CSV file
    csv_file_path = 'PnL.csv'
    df = pd.read_csv(csv_file_path)

    # Check for headers in the CSV file
    required_headers = ['qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'PnL%_H', 'dPnL%', 'product', 'source', 'key', 'pxy', 'yxp', 'PnL%']
    missing_headers = set(required_headers) - set(df.columns)

    # If there are missing headers, raise an exception or fix them programmatically
    if missing_headers:
        raise ValueError(f"Missing headers in CSV file: {missing_headers}")

    # Read telblock.txt to keep track of sent messages
    try:
        with open('telblock.txt', 'r') as f:
            telblock = set(map(str.strip, f.readlines()))
    except FileNotFoundError:
        telblock = set()

    # Iterate through rows in the DataFrame
    for _, row in df.iterrows():
        # Construct message from the row data
        message = "\n".join(f"{header}: {value}" for header, value in row.items())

        # Check if the message has been sent before
        if message in telblock:
            continue

        # Send the message to the specified user(s)
        for chat_id in user_usernames:
            send_message(chat_id, message)

        # Record the sent message in telblock.txt to avoid double sending
        telblock.add(message)

    # Update telblock.txt with the new messages
    with open('telblock.txt', 'w') as f:
        f.write("\n".join(telblock))

if __name__ == "__main__":
    send_messages()





