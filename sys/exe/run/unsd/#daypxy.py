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
        data = yf.download(stock_symbol, period="1d")
    except Exception as e:
        print(f"Error: {e}")
        return "Error", None

    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    # Extract today's open, yesterday's close, and current price
    today_open = data['Open'].iloc[0]
    today_high = data['high'].iloc[0]
    today_low = data['low'].iloc[0]
    yesterday_close = data['Close'].iloc[0]
    current_price = data['Close'].iloc[-1]
    

    # Initialize Day Action as an empty string
    nse_action = ""
    nse_factor = ""

    # Determine the candlestick condition for today
    if current_price > today_open and current_price > yesterday_close:
        nse_action = "SuperBull"
        nse_factor = "SuperBull"
    elif current_price < today_open and current_price < yesterday_close:
        nse_action = "DangerBear"
        nse_factor = "DangerBear"
    elif current_price > today_open:
        nse_action = "Bull"
        nse_factor = "Normal  
    elif current_price < yesterday_close:
        nse_action = "Bear"
        nse_factor = "Normal"
    else:
        nse_action = "Neutral"
        nse_factor = "Neutral"

    return nse_action, nse_factor

# Call the get_nse_action function
nse_action, nse_factor = get_nse_action()
#print(f"{nse_action}")
print(f"Today's Market is {nse_action} {nse_factor}")
