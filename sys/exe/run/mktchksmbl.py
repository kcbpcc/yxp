import yfinance as yf
import warnings
import sys

# Set the PYTHONIOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Specify the intervals in minutes
intervals = [5]

# Function to calculate the Heikin-Ashi candle colors for the last two closed candles
def smktchk(symbol, interval):
    try:
        data = yf.Ticker(symbol).history(period='1mo', interval=f'{interval}m')
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'
        
        # Conditions to check and return the corresponding string
        if current_color == 'Bull' and last_closed_color == 'Bull' and second_last_closed_color == 'Bull':
            return 'Bullish'
        elif current_color == 'Bear' and last_closed_color == 'Bear' and second_last_closed_color == 'Bear':
            return 'Bearish'
        elif current_color == 'Bull' and last_closed_color == 'Bear':
            return 'Buy'
        elif current_color == 'Bear' and last_closed_color == 'Bull':
            return 'Sell'
        else:
            return 'Neutral'
    except Exception as e:
        return 'No Data'

# Example usage:
def check_market_sentiment_for_symbol(symbol):
    market_sentiment = smktchk(symbol, intervals[0])
    return market_sentiment

# Usage example
symbol_to_check = "TCS.NS"  # Replace with the desired stock symbol
result = check_market_sentiment_for_symbol(symbol_to_check)
print(result)

