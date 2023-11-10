from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite, remove_token
import sys
from time import sleep
import traceback
import os
import subprocess
from cnstpxy import dir_path
from colorama import Fore, Style



SILVER = "\033[97m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
print(f'{SILVER}{UNDERLINE}"PXY® PreciseXceleratedYield Pvt Ltd™ All Rights Reserved."{RESET}')
logging = Logger(30, dir_path + "main.log")
try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
def order_place(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.1)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")
                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid format for 'index'")
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False

def mis_order_sell(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='MIS',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.1)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")
                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid format for 'index'")
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False

def mis_order_buy(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='BUY',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='MIS',
                variety='regular',
                price=round_to_paise(row['ltp'], +0.1)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")
                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid format for 'index'")
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False


def get_holdingsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        return None
def get_positionsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return None
try:
    import sys
    import traceback
    import pandas as pd
    import datetime
    import time
    from login_get_kite import get_kite, remove_token
    from cnstpxy import dir_path
    from toolkit.logger import Logger
    from toolkit.currency import round_to_paise
    import csv
    from cnstpxy import sellbuff, secs, perc_col_name
    from time import sleep
    import subprocess

    import random
    import os
    import numpy as np
    import mktpxy
    import importlib
    from daypxy import get_nse_action
    mktpxy = mktpxy.get_market_check('^NSEI')
    SILVER = "\033[97m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    logging.debug("are we having any holdings to check")
    holdings_response = broker.kite.holdings()
    positions_response = broker.kite.positions()['net']
    holdings_df = get_holdingsinfo(holdings_response, broker)
    positions_df = get_positionsinfo(positions_response, broker)
    # Add 'key' column to holdings_df and positions_df
    # Create 'key' column if holdings_df is not empty
    holdings_df['key'] = holdings_df['exchange'] + ":" + holdings_df['tradingsymbol'] if not holdings_df.empty else None
    # Create 'key' column if positions_df is not empty
    positions_df['key'] = positions_df['exchange'] + ":" + positions_df['tradingsymbol'] if not positions_df.empty else None
    combined_df = pd.concat([holdings_df, positions_df], ignore_index=True)
    # Get OHLC data for the 'key' column
    lst = combined_df['key'].tolist()
    resp = broker.kite.ohlc(lst)
    # Create a dictionary from the response for easier mapping
    dct = {
        k: {
            'ltp': v['ohlc'].get('ltp', v['last_price']),
            'open': v['ohlc']['open'],
            'high': v['ohlc']['high'],
            'low': v['ohlc']['low'],
            'close_price': v['ohlc']['close'],
        }
        for k, v in resp.items()
    }
    # Add 'ltp', 'open', 'high', and 'low' columns to the DataFrame
    combined_df['ltp'] = combined_df.apply(lambda row: dct.get(row['key'], {}).get('ltp', row['last_price']), axis=1)
    combined_df['open'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('open', 0))
    combined_df['high'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('high', 0))
    combined_df['low'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('low', 0))
    combined_df['close'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
    combined_df['qty'] = combined_df.apply(lambda row: int(row['quantity'] + row['t1_quantity']) if row['source'] == 'holdings' else int(row['quantity']), axis=1)
    # Calculate 'Invested' column
    combined_df['Invested'] = combined_df['qty'] * combined_df['average_price']
    # Calculate 'value' column as 'qty' * 'ltp'
    combined_df['value'] = combined_df['qty'] * combined_df['ltp']
    combined_df['value_H'] = combined_df['qty'] * combined_df['high']
    # Calculate 'PnL' column as 'value' - 'Invested'
    combined_df['PnL'] = combined_df['value'] - combined_df['Invested']
    combined_df['PnL_H'] = combined_df['value_H'] - combined_df['Invested']
    # Calculate 'PnL%' column as ('PnL' / 'Invested') * 100
    combined_df['PnL%'] = (combined_df['PnL'] / combined_df['Invested']) * 100
    combined_df['PnL%_H'] = (combined_df['PnL_H'] / combined_df['Invested']) * 100
    # Calculate 'Yvalue' column as 'qty' * 'close'
    combined_df['Yvalue'] = combined_df['qty'] * combined_df['close']
    # Calculate 'dPnL' column as 'close_price' - 'ltp'
    combined_df['dPnL'] = combined_df['value'] - combined_df['Yvalue']
    # Calculate 'dPnL%' column as ('dPnL' / 'Invested') * 100
    combined_df['dPnL%'] = (combined_df['dPnL'] / combined_df['Yvalue']) * 100
    # Round all numeric columns to 2 decimal places
    numeric_columns = ['qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PnL%','PnL%_H', 'dPnL', 'dPnL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(1)        # Filter combined_df
    filtered_df = combined_df[(combined_df['qty'] > 0) | ((combined_df['qty'] == 0) & (combined_df['product'] == 'MIS'))]
    # Filter combined_df for rows where 'qty' is greater than 0
    combined_df_positive_qty = combined_df[(combined_df['qty'] > 0) & (combined_df['source'] == 'holdings')]
    # Calculate and print the sum of 'PnL' values and its total 'PnL%' for rows where 'qty' is greater than 0
    total_PnL = combined_df_positive_qty['PnL'].sum()
    total_PnL_percentage = (total_PnL / combined_df_positive_qty['Invested'].sum()) * 100
    # Calculate and print the sum of 'dPnL' values and its total 'dPnL%' for rows where 'qty' is greater than 0
    total_dPnL = combined_df_positive_qty['dPnL'].sum()
    total_dPnL_percentage = (total_dPnL / combined_df_positive_qty['Invested'].sum()) * 100
    import pandas as pd
    # Assuming you have a list of instrument keys, e.g., ['NIFTY50', 'RELIANCE', ...]
    # Replace this with your actual list of keys
    instrument_keys = ['NSE:NIFTY 50']
    # Create an empty DataFrame named NIFTY
    NIFTY = pd.DataFrame()
    # Get OHLC data for the list of keys
    resp = broker.kite.ohlc("NSE:NIFTY 50")
    # Create a dictionary from the response for easier mapping
    dct = {
        k: {
            'ltp': v['ohlc'].get('ltp', v['last_price']),
            'open': v['ohlc']['open'],
            'high': v['ohlc']['high'],
            'low': v['ohlc']['low'],
            'close_price': v['ohlc']['close'],
        }
        for k, v in resp.items()
    }
    # Set the 'key' column to the instrument keys from your list
    NIFTY['key'] = instrument_keys
    # Populate other columns based on the dct dictionary
    NIFTY['ltp'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('ltp', 0))
    NIFTY['timestamp'] = pd.to_datetime('now').strftime('%H:%M:%S')
    NIFTY['open'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('open', 0))
    NIFTY['high'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('high', 0))
    NIFTY['low'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('low', 0))
    NIFTY['close_price'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
    NIFTY['Day_Change_%'] = round(((NIFTY['ltp'] - NIFTY['close_price']) / NIFTY['close_price']) * 100, 2)
    NIFTY['Open_Change_%'] = round(((NIFTY['ltp'] - NIFTY['open']) / NIFTY['open']) * 100, 2)
    NIFTYconditions = [
        (NIFTY['Day_Change_%'] > 0) & (NIFTY['Open_Change_%'] > 0),
        (NIFTY['Open_Change_%'] > 0) & (NIFTY['Day_Change_%'] < 0),
        (NIFTY['Day_Change_%'] < 0) & (NIFTY['Open_Change_%'] < 0),
        (NIFTY['Day_Change_%'] > 0) & (NIFTY['Open_Change_%'] < 0)
    ]
    choices = ['SuperBull', 'Bull', 'DangerBear', 'Bear']
    NIFTY['Day Status'] = np.select(NIFTYconditions, choices, default='Bear')
    status_factors = {
        'SuperBull': 2.8,
        'Bull': 1.4,
        'Bear': 0.7,
        'DangerBear': 0
    }
    # Calculate 'Score' for each row based on 'Day Status' and 'status_factors'
    NIFTY['Score'] = NIFTY['Day Status'].map(status_factors).fillna(0)
    score_value = NIFTY['Score'].values[0]
    # Assuming you have a DataFrame named "NIFTY" with columns 'ltp', 'low', 'high', 'close'
    # Calculate the metrics
    NIFTY['strength'] = NIFTY['strength'] = ((NIFTY['ltp'] - (NIFTY['close_price'] - 0.01)) / (abs(NIFTY['high'] + 0.01) - abs(NIFTY['close_price'] - 0.01))) * 1.4
    NIFTY['pricerange'] = (NIFTY['high'] + 0.01) - (NIFTY['close_price'] - 0.01)
    NIFTY['priceratio'] =  (NIFTY['ltp'] - NIFTY['close_price'])/NIFTY['pricerange']
    # Extract and print just the values without the column name and data type information
    strength_values = NIFTY['strength'].values
    pricerange_values = NIFTY['pricerange'].values
    priceratio_values = NIFTY['priceratio'].values
    # Assuming NIFTY is a dictionary-like object with pandas Series
    import pandas as pd
    # Assuming NIFTY['Day_Change_%'] is a Pandas Series
    Precise = max(1.4, (1 + (NIFTY['Day_Change_%'] * 2.4).round(1)).max())
    Xlratd = max(1.4, (2 + (NIFTY['Day_Change_%'] * 3.4).round(1)).max())
    Yield = max(1.4, (3 + (NIFTY['Day_Change_%'] * 4.4).round(1)).max())
    conditions_pxy = [(mktpxy == 'Bull') | (mktpxy == 'Buy'), (mktpxy == 'Sell'), (mktpxy == 'Bear')]
    choices_pxy = ['Yield', 'Xlratd', 'Precise']
    PXY = np.select(conditions_pxy, choices_pxy, default='Yield')
    # Define the file path for the CSV file
    lstchk_file = "fileHPdf.csv"
    # Dump the DataFrame to the CSV file, overwriting any existing file
    combined_df.to_csv(lstchk_file, index=False)
    print(f"DataFrame has been saved to {lstchk_file}")
    # Create a copy of 'filtered_df' and select specific columns
    pxy_df = filtered_df.copy()[['source','product', 'qty','average_price', 'close', 'ltp', 'open', 'high','low', 'key','dPnL%','PnL','PnL%_H', 'PnL%']]
    pxy_df['Pre'] = Precise
    pxy_df['Xlratd'] = Xlratd
    pxy_df['Yield'] = Yield
    pxy_df['PXY'] = np.where(mktpxy == 'Bear', Precise, np.where((mktpxy == 'Buy') | (mktpxy == 'Bull'), Yield, Xlratd))
    pxy_df['avg'] =filtered_df['average_price']
    # Create a copy for just printing 'filtered_df' and select specific columns
    EXE_df = pxy_df[['source','product', 'key', 'qty','avg','close', 'ltp', 'open', 'high','low','dPnL%','PXY','PnL%','PnL']]
    PRINT_df = pxy_df[['source','product', 'key', 'qty','avg','ltp','PXY','PnL%','PnL']]
    # Sort the DataFrame by 'PnL%' in ascending order
    # Assuming you have a DataFrame named PRINT_df
    PRINT_df_sorted = PRINT_df[(PRINT_df['product'] == 'MIS') | ((PRINT_df['product'] == 'CNC') & (PRINT_df['PnL%'] > 0))].sort_values(by='PnL%', ascending=True)
    SILVER = "\033[97m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    # ANSI escape codes for text coloring
    RESET = "\033[0m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    import pandas as pd
    # Always print "Market view" in bright yellow
    print(f"{BRIGHT_YELLOW}My Trades Overview & Market Dynamics {RESET}")
    # ANSI escape codes for text coloring
    RESET = "\033[0m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    # Print all three sets of values in a single line with rounding to 2 decimal places
    column_width = 47
    left_aligned_format = "{:<" + str(column_width) + "}"
    right_aligned_format = "{:>" + str(column_width) + "}"
    print(left_aligned_format.format(f"Day Change %: {BRIGHT_GREEN if NIFTY['Day_Change_%'][0] >= 0 else BRIGHT_RED}{round(NIFTY['Day_Change_%'][0], 2)}{RESET}"), end="")
    print(right_aligned_format.format(f"Total Day dPnL {BRIGHT_GREEN if total_dPnL > 0 else BRIGHT_RED}{round(total_dPnL, 2)}{RESET}"))
    print(left_aligned_format.format(f"Day Status: {BRIGHT_GREEN if NIFTY['Day Status'][0] in ('Bull', 'SuperBull') else BRIGHT_RED}{NIFTY['Day Status'][0]}, Score: {score_value}{RESET}"), end="")
    print(right_aligned_format.format(f"Total Day dPnL% {BRIGHT_GREEN if total_dPnL_percentage > 0 else BRIGHT_RED}{round(total_dPnL_percentage, 2)}{RESET}"))
    print(left_aligned_format.format(f"Open Change %: {BRIGHT_GREEN if NIFTY['Open_Change_%'][0] >= 0 else BRIGHT_RED}{round(NIFTY['Open_Change_%'][0], 2)}{RESET}"), end="")
    print(right_aligned_format.format(f"Precise Check (Precise): {BRIGHT_GREEN if Precise > 1.4 else BRIGHT_RED}{round(Precise, 2)}{RESET}"))
    print(left_aligned_format.format(f"Total PnL: {BRIGHT_GREEN if total_PnL >= 0 else BRIGHT_RED}{round(total_PnL, 2)}{RESET}"), end="")
    print(right_aligned_format.format(f"Xcelerated Check (Xlratd): {BRIGHT_GREEN if Xlratd > 2.4 else BRIGHT_RED}{round(Xlratd, 2)}{RESET}"))
    print(left_aligned_format.format(f"Total PnL%: {BRIGHT_GREEN if total_PnL_percentage >= 0 else BRIGHT_RED}{round(total_PnL_percentage, 2)}{RESET}"), end="")
    print(right_aligned_format.format(f"Yield Check (Yield): {BRIGHT_GREEN if Yield > 3.4 else BRIGHT_RED}{round(Yield, 2)}{RESET}"))
    # Always print "Table" in bright yellow
    print(f"{BRIGHT_YELLOW}Table– Above Precise and reaching Xcelerated{RESET}")
    # Print EXE_df_sorted without color
    print(PRINT_df_sorted)

    # Define the CSV file path
    csv_file_path = "filePnL.csv"
    # Create an empty list to store the rows that meet the condition
    selected_rows = []
    # Loop through the DataFrame and place orders based on conditions
    if any(item in mktpxy for item in ['Sell', 'Bear', 'Buy', 'Bull', 'None']):  # Check if mktpxy is one of the specified values
        try:
            for index, row in EXE_df.iterrows():
                key = row['key']  # Get the 'key' value
                # Check the common conditions first
                if (
                    (row['ltp'] > 0)
                ):
                    if (row['source'] == 'holdings' and row['product'] == 'CNC' and row['PnL%'] > 0 and row['PnL%'] > 0
                        
                    ):
                        # Print the row before placing the order
                        print(row)

                        try:
                            is_placed = order_place(key, row)
                            if is_placed:
                                # Write the row to the CSV file here
                                with open(csv_file_path, 'a', newline='') as csvfile:
                                    csvwriter = csv.writer(csvfile)
                                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
                    elif row['source'] == 'positions' and row['product'] == 'CNC' and row['PnL%'] > 0 and (row['PnL%'] > 0):
                        # Print the row before placing the order
                        print(row)
                        
                        try:
                            is_placed = order_place(key, row)
                            if is_placed:
                                # Write the row to the CSV file here
                                with open(csv_file_path, 'a', newline='') as csvfile:
                                    csvwriter = csv.writer(csvfile)
                                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
                    elif row['product'] == 'MIS' and row['source'] == 'positions' and row['PnL%'] < -1 and row['qty'] < 0:

                        # Print the row before placing the order
                        print(row)
                        try:
                            is_placed = mis_order_buy(key, row)
                            if is_placed:
                                # Write the row to the CSV file here
                                with open(csv_file_path, 'a', newline='') as csvfile:
                                    csvwriter = csv.writer(csvfile)
                                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")

                    elif row['product'] == 'MIS' and row['source'] == 'positions' and row['qty'] == 0 and row['PnL']==0:

                        # Print the row before placing the order
                        print(row)
                        try:
                            is_placed = mis_order_sell(key, row)
                            if is_placed:
                                # Write the row to the CSV file here
                                with open(csv_file_path, 'a', newline='') as csvfile:
                                    csvwriter = csv.writer(csvfile)
                                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
        except Exception as e:
            # Handle any other exceptions that may occur during the loop
            print(f"An unexpected error occurred: {e}")
        print(f'{SILVER}{UNDERLINE}"PXY® PreciseXceleratedYield Pvt Ltd™ All Rights Reserved."{RESET}')

       
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")



    
