import yfinance as yf
import warnings
from rich import print
from rich.console import Console
from rich.style import Style
import sys
import csv

# Set the PYTHONIOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Specify the intervals in minutes
intervals = [5]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, interval):
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period='5d', interval=f'{interval}m')

    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Calculate the colors of the last three closed candles
    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_last_closed_color

# Function to determine the market check based on candle colors
def get_market_check(symbol):
    # Check the colors of the last two closed candles and the currently running candle
    current_color, last_closed_color, second_last_closed_color = calculate_last_three_heikin_ashi_colors(symbol, intervals[0])

    # Initialize messages
    title = ""

    # Define styles for rich.print
    bear_style = Style(color="red")
    bull_style = Style(color="green")
    buy_style = Style(color="green")
    sell_style = Style(color="red")

    # Determine the market check based on the candle colors and use rich.print to format output
    if current_color == 'Bear' and last_closed_color == 'Bear':
        mktpxy = 'Bear'
        console.print(f"{symbol} 🐻🔴🔴🔴 [bold]Bearish sentiment![/bold]🍯💰", style=bear_style)
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        mktpxy = 'Bull'
        console.print(f"{symbol} 🐂🟢🟢🟢 [bold]Bullish sentiment![/bold]💪💰", style=bull_style)
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        mktpxy = 'Sell'
        console.print(f"{symbol} 🛒🔴🛬⤵️ [bold]Time to sell![/bold]📉💰", style=sell_style) 
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        mktpxy = 'Buy'
        console.print(f"{symbol} 🚀🟢🛫⤴️ [bold]Time to buy![/bold]🌠💰", style=buy_style)
    else:
        mktpxy = 'None'
        console.print(f"{symbol} 🌟 [bold]Market on standby![/bold]🍿💰📊")

    return mktpxy

# Read symbols from the CSV file and list them first
symbols_list = []

with open('mktsmbl500pxy.txt', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if len(row) > 1:  # Check if there is at least one symbol in the second column
            symbol = row[1].strip('"')  # Assuming symbols are in the second column
            symbols_list.append(symbol)

# Print the list of symbols
console.print(f"Symbols to Check: {', '.join(symbols_list)}")

# Perform the market check for each symbol
for symbol in symbols_list:
    get_market_check(symbol)

