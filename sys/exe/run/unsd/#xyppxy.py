import yfinance as yf
import numpy as np
import pandas as pd
from timpxy import calculate_timpxy
from mktpxy import get_market_check

mktpxy, pktpxy = get_market_check('^NSEI')

# Function to fetch NIFTY data for one-day candles
def fetch_nifty_data():
    nifty_ticker = yf.Ticker('^NSEI')  # NSE NIFTY 50 index symbol
    nifty_data = nifty_ticker.history(period='1d', interval='1d')
    return nifty_data

# Fetch NIFTY data for one-day candles
NIFTY = fetch_nifty_data()

# Ensure you have data for one-day candles
if not NIFTY.empty:
    # Extract relevant information for one-day candles
    day_open = NIFTY['Open'].values[0]
    day_high = NIFTY['High'].max()
    day_low = NIFTY['Low'].min()
    day_close = NIFTY['Close'].values[-1]

    # Print the results
    print("Day Open:", day_open)
    print("Day High:", day_high)
    print("Day Low:", day_low)
    print("Day Close:", day_close)

    # Calculate 'strength' and 'weakness'
    NIFTY['strength'] = ((NIFTY['Close'] - (NIFTY['Low'] - 0.01)) /
                         (np.abs(NIFTY['High'] + 0.01) - np.abs(NIFTY['Low'] - 0.01)))

    NIFTY['weakness'] = ((NIFTY['Close'] - (NIFTY['High'] - 0.01)) /
                          (np.abs(NIFTY['High'] + 0.01) - np.abs(NIFTY['Low'] - 0.01)))

    # Assuming other necessary variables are defined
    timpxy = calculate_timpxy()

    Precise = min(1.3, (1 + NIFTY['strength']).round(1).max())

    # Calculate Xlratd
    Xlratd = NIFTY['strength'] * timpxy

    # Calculate Yield
    Yield = timpxy * (-1)

    # Conditions and choices for PXY
    conditions_pxy = [
        (mktpxy == 'Bull') | (mktpxy == 'Buy'),
        (mktpxy == 'Sell'),
        (mktpxy == 'Bear'),
        (mktpxy == 'Bull')
    ]
    choices_pxy = ['Yield', 'Xlratd', 'Precise', 'Yield']
    PXY = np.select(conditions_pxy, choices_pxy)

    # Assuming NIFTY['Day_Change_%'] is a Pandas Series
    _Precise = min(1.3, (NIFTY['weakness']).round(1).max(), -1)
    _Xlratd = (NIFTY['weakness'] * timpxy).clip(None, -1)
    _Yield = timpxy * (-1)

    # Conditions and choices for _PXY
    _conditions_pxy = [
        (mktpxy == 'Bear') | (mktpxy == 'Buy'),
        (mktpxy == 'Sell'),
        (mktpxy == 'Bear'),
        (mktpxy == 'Bull')
    ]
    _choices_pxy = ['_Yield', '_Xlratd', '_Precise', '_Yield']
    _PXY = np.select(_conditions_pxy, _choices_pxy)

    # Print values with one decimal place
    print("Precise:", round(Precise, 1))
    print("Xlratd:", Xlratd.round(1))
    print("Yield:", round(Yield, 1))
    print("PXY:", np.where(np.isnan(PXY), 'NaN', PXY).round(1))

    print("_Precise:", round(_Precise, 1))
    print("_Xlratd:", _Xlratd.round(1))
    print("_Yield:", round(_Yield, 1))
    print("_PXY:", _PXY.astype(str).replace('nan', 'NaN').round(1))
else:
    print("No data available for one-day candles.")


