import yfinance as yf
import numpy as np
import pandas as pd
from timpxy import calculate_timpxy
import math


# Function to fetch NIFTY data using yfinance
def fetch_nifty_data():
    nifty_ticker = yf.Ticker('^NSEI')  # NSE NIFTY 50 index symbol
    nifty_data = nifty_ticker.history(period='1d', interval='1m')
    return nifty_data

# Fetch NIFTY data
NIFTY = fetch_nifty_data()

# Calculate 'strength' and 'weakness'
NIFTY['strength'] = ((NIFTY['Close'] - (NIFTY['Low'] - 0.01)) /
                     (np.abs(NIFTY['High'] + 0.01) - np.abs(NIFTY['Low'] - 0.01)))

NIFTY['weakness'] = ((NIFTY['Close'] - (NIFTY['High'] - 0.01)) /
                      (np.abs(NIFTY['High'] + 0.01) - np.abs(NIFTY['Low'] - 0.01)))

# Assuming other necessary variables are defined
timpxy = calculate_timpxy()

# Calculate Precise
Precise = min(1.3, (1 + NIFTY['strength']).round(1).max())

# Calculate Xlratd
Xlratd = NIFTY['strength'] * timpxy

# Calculate Yield
Yield = timpxy * (-1)

# Conditions for PXY
conditions_pxy = [
    (mktpxy.isin(['Bull', 'Buy'])),
    (mktpxy == 'Sell'),
    (mktpxy == 'Bear'),
    (mktpxy == 'Bull')
]

# Choices for PXY
choices_pxy = ['Yield', 'Xlratd', 'Precise', 'Yield']

# Calculate PXY
PXY = np.select(conditions_pxy, choices_pxy)

# Assuming NIFTY['Day_Change_%'] is a Pandas Series
# Calculate _Precise, _Xlratd, _Yield, and _PXY
_Precise = min(1.3, (NIFTY['weakness']).round(1).max(), -1)
_Xlratd = (NIFTY['weakness'] * timpxy).clip(None, -1)
_Yield = timpxy * (-1)

# Conditions for _PXY
_conditions_pxy = [
    (mktpxy == 'Bear') | (mktpxy == 'Buy'),
    (mktpxy == 'Sell'),
    (mktpxy == 'Bear'),
    (mktpxy == 'Bull')
]

# Choices for _PXY
_choices_pxy = ['_Yield', '_Xlratd', '_Precise', '_Yield']

# Calculate _PXY
_PXY = np.select(_conditions_pxy, _choices_pxy)

# Print values
print(NIFTY)
print("Precise:", Precise)
print("Xlratd:", Xlratd)
print("Yield:", Yield)
print("PXY:", PXY)

print("_Precise:", _Precise)
print("_Xlratd:", _Xlratd)
print("_Yield:", _Yield)
print("_PXY:", _PXY)
