from kiteconnect import KiteConnect
from login_get_kite import get_kite, remove_token
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
import traceback
import logging
import pandas as pd
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target

def place_mis_orders(positions_df, broker):
    try:
        # Place orders for MIS positions where quantity is less than 0
        for index, position in positions_df.iterrows():
            logging.info(f"Placing order for {position['tradingsymbol']}")
            order_id = broker.order_place(
                tradingsymbol=position['tradingsymbol'],
                exchange=position['exchange'],
                transaction_type='BUY',  # Change to BUY for buying positions
                quantity=int(-1 * position['quantity']),  # Buying the existing position
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
        logging.error(f"{str(e)} while placing orders")
        return False

    return True

try:
    # Get KiteConnect instance
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} Unable to get KiteConnect instance")

# Get open MIS positions with quantity < 0
positions_response = broker.kite.positions()['net']
mis_positions = pd.DataFrame([pos for pos in positions_response if pos['product'] == 'MIS' and pos['quantity'] < 0])

# Call the function with the appropriate arguments
result = place_mis_orders(mis_positions, broker)

# Do something with the result if needed
if result:
    print("Buy orders placed successfully for MIS positions with quantity < 0.")
else:
    print("Failed to place buy orders for MIS positions with quantity < 0.")



