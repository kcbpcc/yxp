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
        data = yf.download(stock_symbol, period="2d")  # Download 2 days of data for today and yesterday
    except Exception as e:
        print(f"Error: {e}")
        return "Error"

    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    # Extract today's open, close, high, low, and yesterday's close
    today_open = data['Open'].iloc[-1]
    today_close = data['Close'].iloc[-1]
    today_high = data['High'].iloc[-1]
    today_low = data['Low'].iloc[-1]
    yesterday_close = data['Close'].iloc[0]

    # Calculate candle body and wick lengths
    candle_body = abs(today_close - today_open)
    bull_wick = today_high - max(today_open, today_close)
    bear_wick = min(today_open, today_close) - today_low

    # Calculate percentage strength
    total_length = candle_body + bull_wick + bear_wick
    bull_strength_percent = (bull_wick / total_length) * 100
    bear_strength_percent = (bear_wick / total_length) * 100

    # Determine the market condition based on the relationship between open, current price, and yesterday's close
    if today_close > today_open and today_close > yesterday_close:
        nse_action = "SNIFTYBULL"
        strength = f"Bull Strength: {bull_strength_percent:.2f}%"
    elif today_close < today_open and today_close < yesterday_close:
        nse_action = "SNIFTYBEAR"
        strength = f"Bear Strength: {bear_strength_percent:.2f}%"
    elif today_close > today_open and today_close < yesterday_close:
        nse_action = "NIFTYBULL"
        strength = f"Bull Strength: {bull_strength_percent:.2f}%"
    elif today_close < today_open and today_close > yesterday_close:
        nse_action = "NIFTYBEAR"
        strength = f"Bear Strength: {bear_strength_percent:.2f}%"
    else:
        nse_action = "Neutral"
        strength = "Neutral"

    return nse_action, strength

# Call the get_nse_action function
nse_action, strength = get_nse_action()

# Set color based on the main condition (NIFTYBULL, NIFTYBEAR, or Neutral)
color = "\x1b[31m" if nse_action == "SNIFTYBEAR" else "\x1b[32m" if nse_action == "SNIFTYBULL" else "\x1b[0m"

print(f"Today's Market is {color}{nse_action}\x1b[0m")
print(strength)


color = "\x1b[31m" if nse_action == "NIFTYBEAR" else "\x1b[32m" if nse_action == "NIFTYBULL" else "\x1b[0m"

print(f"Today's Market is {color}{nse_action}\x1b[0m")

