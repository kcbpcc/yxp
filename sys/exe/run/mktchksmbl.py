import yfinance as yf
import warnings
from rich.console import Console
import sys
import csv

# Set the PYTHONIOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Specify the intervals in minutes
intervals = [5]

# Suffix to be added to each symbol
suffix = ".NS"

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last two closed candles
def calculate_last_two_heikin_ashi_colors(symbol, interval):
    try:
        data = yf.Ticker(symbol).history(period='5d', interval=f'{interval}m')
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        return current_color, last_closed_color
    except Exception as e:
        console.print(f"{symbol}: No data found, symbol may be delisted. Skipping to the next one.")
        return None, None

# Function to determine the market check based on candle colors
def get_market_check(symbol):
    current_color, last_closed_color = calculate_last_two_heikin_ashi_colors(symbol, intervals[0])
    return current_color

# Example usage:
def check_market_sentiment_for_symbol(symbol):
    market_sentiment = get_market_check(symbol)
    if market_sentiment is not None:
        console.print(f"{symbol}: {market_sentiment}")

# Call the function with a specific symbol
check_market_sentiment_for_symbol("AAPL.NS")  # Replace with the desired symbol
