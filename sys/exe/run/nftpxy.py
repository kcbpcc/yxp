import yfinance as yf
import os
import sys

def get_nse_action():
    # Define the stock symbol (NSEI for Nifty 50)
    stock_symbol = "^NSEI"

    try:
        # Redirect standard output to os.devnull to suppress messages
        sys.stdout = open(os.devnull, 'w')

        # Download today's data
        data = yf.download(stock_symbol, period="5d")
    except Exception as e:
        print(f"Error during data download: {e}")
        return "Error", None
    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    # Extract today's open, yesterday's close, and current price
    today_open = data['Open'].iloc[0]
    today_high = data['High'].iloc[0]
    today_low = data['Low'].iloc[0]
    yesterday_close = data['Close'].iloc[0]
    current_price = data['Close'].iloc[-1]

    # Calculate nse_power
    nse_power = round((current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01)), 2)

    # Initialize Day Action as an empty string
    nse_action = ""

    # Determine the candlestick condition for today
    if current_price > today_open and current_price > yesterday_close:
        nse_action = "SuperBull"
    elif current_price < today_open and current_price < yesterday_close:
        nse_action = "DangerBear"
    elif current_price > today_open:
        nse_action = "Bull"
    elif current_price < yesterday_close:
        nse_action = "Bear"
    else:
        nse_action = "Neutral"

    return nse_action, nse_power

# Call the get_nse_action function
nse_action, nse_power = get_nse_action()
print(f"Today's Market is {nse_action} with nse_power {nse_power}")


