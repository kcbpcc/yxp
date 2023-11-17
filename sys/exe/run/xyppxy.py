import yfinance as yf
import numpy as np
import pandas as pd
from timpxy import calculate_timpxy
from mktpxy import get_market_check
import math

mktpxy, pktpxy = get_market_check('^NSEI')
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
print("Xlratd:", Xlratd.round(1).values)  # Use .values to remove the Datetime index
print("Yield:", round(Yield, 1))
print("PXY:")
print(pd.Series(PXY).astype(str).replace('nan', 'NaN').round(1).values)  # Convert to Pandas Series to remove the Datetime index

print("_Precise:", round(_Precise, 1))
print("_Xlratd:", _Xlratd.round(1).values)  # Use .values to remove the Datetime index
print("_Yield:", round(_Yield, 1))
print("_PXY:")
print(pd.Series(_PXY).astype(str).replace('nan', 'NaN').round(1).values)  # Convert to Pandas Series to remove the Datetime index
