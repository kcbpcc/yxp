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
        return "Error"

    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    # Extract today's open and current price
    today_open = data['Open'].iloc[0]
    current_price = data['Close'].iloc[-1]

    # Determine the market condition based on the relationship between open and current price
    if current_price > today_open:
        nse_action = "NIFTYBULL"
    elif current_price < today_open:
        nse_action = "NIFTYBEAR"
    else:
        nse_action = "Neutral"

    return nse_action

# Call the get_nse_action function
nse_action = get_nse_action()
print(f"Today's Market is {nse_action}")
