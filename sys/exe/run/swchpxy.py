import yfinance as yf
from datetime import datetime

def analyze_stock(symbol):
    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Fetch historical stock data for today
    stock_data = yf.download(symbol, start=today_date, end=today_date)

    # Check if the conditions are met
    below_open_high_above_open = (stock_data['Low'] < stock_data['Open']) & (stock_data['High'] > stock_data['Open'])
    above_open_low_below_open = (stock_data['High'] > stock_data['Open']) & (stock_data['Low'] < stock_data['Open'])

    if below_open_high_above_open.any() or above_open_low_below_open.any():
        return 'yes'
    else:
        return 'no'


