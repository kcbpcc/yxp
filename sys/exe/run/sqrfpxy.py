from kiteconnect import KiteConnect
from login_get_kite import get_kite, remove_token
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
import traceback
import logging
import pandas as pd
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target

def place_mis_orders(positions_df, broker):
    try:
        # Place orders for MIS positions
        for position in positions_df:
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
        logging.error(f"{str(e)} while placing orders")
        return False

    return True

try:
    # Get KiteConnect instance
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} Unable to get KiteConnect instance")

# Get open MIS positions
mis_positions = [pos for pos in broker.positions()['day'] if pos['product'] == 'MIS']

# Call the function with the appropriate arguments
result = place_mis_orders(mis_positions, broker)

# Do something with the result if needed
if result:
    print("Orders placed successfully.")
else:
    print("Failed to place orders.")

# Get open MIS positions again for conversion
mis_positions = [pos for pos in broker.positions()['net'] if pos['product'] == 'MIS' and pos['quantity'] > 0]

# Convert MIS to CNC
for position in mis_positions:
    print(f"Symbol: {position['trading_symbol']}, Quantity: {position['quantity']}, Product: {position['product']}")
    broker.place_order(
        tradingsymbol=position['trading_symbol'],
        exchange=position['exchange'],
        quantity=position['quantity'],
        transaction_type='CONVERT',
        order_type='MARKET',
        product='CNC'
    )

print("Conversion complete.")

