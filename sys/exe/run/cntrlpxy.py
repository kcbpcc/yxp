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
print(f'{SILVER}{UNDERLINE}"PXY® PreciseXceleratedYield Pvt Ltd™"{RESET}')
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
                quantity=int(-1*row['qty']),
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
    from prftpxy import process_csv
    import random
    import os
    import numpy as np
    from mktpxy import get_market_check
    import importlib
    from nftpxy import get_nse_action
    from timpxy import calculate_timpxy
    import math
    #from telpxy import send_telegram_message
    timpxy = calculate_timpxy()
    csv_file_path = "filePnL.csv"
    total_profit_main = process_csv(csv_file_path)
    mktpxy, pktpxy = get_market_check('^NSEI')
    SILVER = "\033[97m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    logging.debug("Are we having any holdings to check")
    holdings_response = broker.kite.holdings()
    positions_response = broker.kite.positions()['net']
    holdings_df = get_holdingsinfo(holdings_response, broker)
    positions_df = get_positionsinfo(positions_response, broker)
    response = broker.kite.margins()
    available_cash = response["equity"]["available"]["live_balance"]  
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
    #combined_df['PnL%'] = ((combined_df['PnL'] / combined_df['Invested']) * 100) * np.where(combined_df['qty'] < 0, -1, 1)
    combined_df['PnL%_H'] = (combined_df['PnL_H'] / combined_df['Invested']) * 100
    #combined_df['PnL%_H'] = ((combined_df['PnL_H'] / combined_df['Invested']) * 100) * np.where(combined_df['qty'] < 0, -1, 1)
    # Calculate 'Yvalue' column as 'qty' * 'close'
    combined_df['Yvalue'] = combined_df['qty'] * combined_df['close']
    # Calculate 'dPnL' column as 'close_price' - 'ltp'
    combined_df['dPnL'] = combined_df['value'] - combined_df['Yvalue']
    # Calculate 'dPnL%' column as ('dPnL' / 'Invested') * 100
    combined_df['dPnL%'] = (combined_df['dPnL'] / combined_df['Yvalue']) * 100
    # Round all numeric columns to 2 decimal places
    numeric_columns = ['qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PnL%','PnL%_H', 'dPnL', 'dPnL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(1)        # Filter combined_df
    filtered_df = combined_df[(combined_df['qty'] > 0) | ((combined_df['qty'] < 0) & (combined_df['product'] == 'MIS'))]
    # Filter combined_df for rows where 'qty' is greater than 0
    combined_df_positive_qty = combined_df[(combined_df['qty'] > 0) & (combined_df['source'] == 'holdings')]
    # Calculate and print the sum of 'PnL' values and its total 'PnL%' for rows where 'qty' is greater than 0
    total_PnL = round(combined_df_positive_qty['PnL'].sum())
    total_PnL_percentage = (total_PnL / combined_df_positive_qty['Invested'].sum()) * 100
    # Calculate and print the sum of 'dPnL' values and its total 'dPnL%' for rows where 'qty' is greater than 0
    #total_dPnL = combined_df_positive_qty['dPnL'].sum()
    total_dPnL = round(combined_df_positive_qty['dPnL'].sum())
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
    choices = ['Super Bull', 'Bull', 'Danger Bear', 'Bear']
    NIFTY['Day Status'] = np.select(NIFTYconditions, choices, default='Bear')
    status_factors = {
        'Super Bull': 2.8,
        'Bull': 1.4,
        'Bear': 0.7,
        'Danger Bear': 0
    }
    # Calculate 'Score' for each row based on 'Day Status' and 'status_factors'
    NIFTY['Score'] = NIFTY['Day Status'].map(status_factors).fillna(0)
    score_value = NIFTY['Score'].values[0]
    # Assuming you have a DataFrame named "NIFTY" with columns 'ltp', 'low', 'high', 'close'
    # Calculate the metrics
    NIFTY['strength'] = ((NIFTY['ltp'] - (NIFTY['low'] - 0.01)) / (abs(NIFTY['high'] + 0.01) - abs(NIFTY['low'] - 0.01)))    
    NIFTY['weakness'] = ((NIFTY['ltp'] - (NIFTY['high'] - 0.01)) / (abs(NIFTY['high'] + 0.01) - abs(NIFTY['low'] - 0.01)))

    Pr = max(1.0, 3.0 + max(0.2, round((0.0 + (NIFTY['strength'] * 1.0)).max(), 2)))
    Xl = round(max(3.0, timpxy * 0.5 * max(0.1, round((0.0 + NIFTY['strength']).round(1).max(), 2))), 1)
    Yi = max(float(timpxy), float(Xl))  # Use max instead of np.maximum for scalar values
    
    PXY = Yi if mktpxy in ["Buy", "Bull"] else (Xl if mktpxy == "Sell" else Pr)
    
    _Pr = max(-1.3, 1.0 - max(-0.2, round((0.0 + (NIFTY['weakness'] * 1.0)).min(), 2)))
    _Xl = round(max(-3.0, timpxy * 0.5 * max(0.1, round((0.0 + NIFTY['weakness']).round(1).min(), 2))), 1)
    _Yi = min(float(timpxy), float(_Xl))  # Use min instead of np.minimum for scalar values
    
    YXP = _Yi if mktpxy in ["Sell", "Bear"] else (_Xl if mktpxy == "Buy" else _Pr)

    
    # Define the file path for the CSV file
    lstchk_file = "fileHPdf.csv"
    # Dump the DataFrame to the CSV file, overwriting any existing file
    combined_df.to_csv(lstchk_file, index=False)
    print(f"DataFrame has been saved to {lstchk_file}")
    # Create a copy of 'filtered_df' and select specific columns
    pxy_df = filtered_df.copy()[['source','product', 'qty','average_price', 'close', 'ltp', 'open', 'high','low','key','dPnL%','PnL','PnL%_H', 'PnL%']]
    
    pxy_df['Pr'] = Pr
    pxy_df['Xl'] = Xl
    pxy_df['Yi'] = Yi
    pxy_df['_Pr'] = _Pr
    pxy_df['_Xl'] = _Xl
    pxy_df['_Yi'] = _Yi
    
    pxy_df['PXY'] = PXY
    pxy_df['YXP'] = YXP 
    
    pxy_df['avg'] =filtered_df['average_price']
    # Create a copy for just printing 'filtered_df' and select specific columns
    EXE_df = pxy_df[['product','source', 'key', 'qty','avg','ltp','PnL%_H','dPnL%','PXY','YXP','PnL%','PnL']]
    PRINT_df = pxy_df[['source','product','qty','key','YXP','PXY','PnL%','PnL']]
    # Rename columns for display
    PRINT_df = PRINT_df.rename(columns={'source': 'HP', 'product': 'CM'})
    # Conditionally replace values in the 'HP' column
    PRINT_df['HP'] = PRINT_df['HP'].replace({'holdings': 'H', 'positions': 'P'})
    # Conditionally replace values in the 'CM' column
    PRINT_df['CM'] = PRINT_df['CM'].replace({'CNC': 'C', 'MIS': 'M'})
    # Convert the 'PnL' column to integers
    # Remove 'BSE:' or 'NSE:' from the 'key' column
    PRINT_df['key'] = PRINT_df['key'].str.replace(r'(BSE:|NSE:)', '', regex=True)    
    # Sort the DataFrame by 'PnL%' in ascending order
    # Assuming you have a DataFrame named PRINT_df
    PRINT_df_sorted = PRINT_df[
        (PRINT_df['qty'] != 0) & (
            ((PRINT_df['qty'] > 0) & (PRINT_df['PnL%'] > pxy_df['Pr'])) |
            ((PRINT_df['qty'] < 0) & (PRINT_df['PnL%'] < pxy_df['_Pr']))
        )
    ]
    PRINT_df_sorted['PnL'] = PRINT_df_sorted['PnL'].astype(int)

    SILVER = "\033[97m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    # ANSI escape codes for text coloring
    RESET = "\033[0m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    import pandas as pd

 
    # Always print "Table" in bright yellow
    print(f"{BRIGHT_YELLOW}Table– Stocks above @Pr and might reach @Yi {RESET}")

    # Print EXE_df_sorted without color
    print(PRINT_df_sorted.to_string(index=False))

    # Define the CSV file path
    csv_file_path = "filePnL.csv"
    # Create an empty list to store the rows that meet the condition
    selected_rows = []# Loop through the DataFrame and place orders based on conditions    
    if any(item in mktpxy for item in ['Sell', 'Bear', 'Buy', 'Bull', 'None']):  # Check if mktpxy is one of the specified values
        try:
            for index, row in EXE_df.iterrows():
                key = row['key']  # Get the 'key' value
                # Check the common conditions first
                if (
                    (row['ltp'] > 0 and
                     row['avg'] > 0) 
                ):
                    if (
                        row['qty'] > 0 and
                        row['source'] == 'holdings' and
                        row['PnL%'] > 1.4 and 
                        (row['PnL%'] < row['PXY'] and row['PnL%_H'] > row['PXY'])
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

                    elif (
                        row['qty'] > 0 and
                        row['source'] == 'positions' and
                        row['product'] == 'MIS' and
                        row['PnL%'] > row['PXY']
                    ):
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

                    elif (
                        row['qty'] < 0 and
                        row['source'] == 'positions' and
                        row['product'] == 'MIS' and
                        row['PnL%'] < row['YXP']
                    ):
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

        
        except Exception as e:
            # Handle any other exceptions that may occur during the loop
            print(f"An unexpected error occurred: {e}")


        
        print(f"{BRIGHT_YELLOW}📉🔀Trades Overview & Market Dynamics 📈🔄 {RESET}")
        # ANSI escape codes for text coloring
        RESET = "\033[0m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"
        # Print all three sets of values in a single line with rounding to 2 decimal places
        column_width = 30
        left_aligned_format = "{:<" + str(column_width) + "}"
        right_aligned_format = "{:>" + str(column_width) + "}"
        
        print(left_aligned_format.format(f"YXP:{BRIGHT_GREEN if (NIFTY['Open_Change_%'] < 0).any() else BRIGHT_RED}{round(YXP, 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"PXY:{BRIGHT_GREEN if (NIFTY['Open_Change_%'] > 0).any() else BRIGHT_RED}{round(PXY, 2)}{RESET}"))
        print(left_aligned_format.format(f"Day Change%:{BRIGHT_GREEN if NIFTY['Day_Change_%'][0] >= 0 else BRIGHT_RED}{round(NIFTY['Day_Change_%'][0], 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"dPnL {BRIGHT_GREEN if total_dPnL > 0 else BRIGHT_RED}{round(total_dPnL, 2)}{RESET}"))
        print(left_aligned_format.format(f"Day Status:{BRIGHT_GREEN if NIFTY['Day Status'][0] in ('Bull', 'Super Bull') else BRIGHT_RED}{NIFTY['Day Status'][0]}{RESET}"), end="")
        print(right_aligned_format.format(f"dPnL%:{BRIGHT_GREEN if total_dPnL_percentage > 0 else BRIGHT_RED}{round(total_dPnL_percentage, 2)}{RESET}"))
        print(left_aligned_format.format(f"Day Open%:{BRIGHT_GREEN if NIFTY['Open_Change_%'][0] >= 0 else BRIGHT_RED}{round(NIFTY['Open_Change_%'][0], 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"mktpxy:{(BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED)}{mktpxy}{RESET}"))
        print(left_aligned_format.format(f"tPnL:{BRIGHT_GREEN if total_PnL >= 0 else BRIGHT_RED}{round(total_PnL, 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"Funds:{BRIGHT_GREEN if available_cash > 12000 else BRIGHT_YELLOW}{available_cash:.0f}{RESET}"))
        print(left_aligned_format.format(f"tPnL%:{BRIGHT_GREEN if total_PnL_percentage >= 0 else BRIGHT_RED}{round(total_PnL_percentage, 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"Booked:{BRIGHT_GREEN if total_profit_main > 0 else BRIGHT_RED}{round(total_profit_main)}{RESET}"))

        
        subprocess.run(['python3', 'mktpxy.py'])


        print(f'{SILVER}{UNDERLINE}🏛🏛🏛PXY® PreciseXceleratedYield Pvt Ltd™🏛🏛🏛{RESET}')

except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")



