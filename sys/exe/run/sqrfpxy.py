from kiteconnect import KiteConnect
from login_get_kite import get_kite
import pandas as pd
import traceback
import logging  # Add this import statement for logging
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite, remove_token
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
import sys
from time import sleep
import traceback
import os
import subprocess
from cnstpxy import dir_path
from colorama import Fore, Style

def place_mis_orders(positions_df):
    try:
        # Get KiteConnect instance
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} Unable to get KiteConnect instance")
        return False

    # Place orders for MIS positions
    for position in positions_df:  # Use the passed positions_df argument
        try:
            logging.info(f"Placing order for {position['tradingsymbol']}")
            order_id = broker.order_place(
                tradingsymbol=position['tradingsymbol'],
                exchange=position['exchange'],
                transaction_type='BUY',
                quantity=int(-1 * position['quantity']),  # Selling the existing position
                order_type='MARKET',
                product='MIS',
                variety='regular'
            )
            if order_id:
                logging.info(f"Order {order_id} placed successfully for {position['tradingsymbol']}")
            else:
                logging.error("Order placement failed")
        except Exception as e:
            print(traceback.format_exc())
            logging.error(f"{str(e)} while placing order for {position['tradingsymbol']}")
            return False

    return True

# Get open MIS positions
mis_positions = [pos for pos in get_kite().positions()['day'] if pos['product'] == 'MIS']

# Call the function with the appropriate arguments
result = place_mis_orders(mis_positions)

# Do something with the result if needed
if result:
    print("Orders placed successfully.")
else:
    print("Failed to place orders.")
