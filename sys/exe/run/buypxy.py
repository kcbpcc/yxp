from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from byhopxy import get
from pluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from mktchksmbl import getsmktchk

logging = Logger(10)
holdings = dir_path + "holdings.csv"
black_file = dir_path + "blacklist.txt"

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
    if fileutils.is_file_not_2day(holdings):
        logging.debug("getting holdings for the day ...")
        resp = broker.kite.holdings()
        if resp and any(resp):
            df = get(resp)
            logging.debug(f"writing to csv ... {holdings}")
            df.to_csv(holdings, index=False)
        with open(black_file, 'w+') as bf:
            pass
except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

# Call the calculate_decision function to get the decision
decision = calculate_decision()

if decision == "YES":
    for symbol_to_check in lst_tlyne:
        # Append '.NS' to the symbol if it doesn't have it already
        symbol_to_check_ns = symbol_to_check if '.NS' in symbol_to_check else f"{symbol_to_check}.NS"

        # Get the market sentiment for each symbol
        symbol_sentiment = get_market_sentiment(symbol_to_check_ns)

        # Check if the market sentiment is 'Bull'
        if symbol_sentiment == 'Bull':
            try:
                lst = []
                file_size_in_bytes = os.path.getsize(holdings)
                logging.debug(f"holdings file size: {file_size_in_bytes} bytes")
                if file_size_in_bytes > 50:
                    logging.debug(f"reading from csv ...{holdings}")
                    df_holdings = pd.read_csv(holdings)
                    if not df_holdings.empty:
                        lst = df_holdings['tradingsymbol'].to_list()

                # get list from positions
                lst_dct = broker.positions
                if lst_dct and any(lst_dct):
                    lst = [dct['symbol'] for dct in lst_dct]
                    logging.info(f"filtered from positions ...{lst}")
            except Exception as e:
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to read positions")
                sys.exit(1)

            # Place a buy order for the symbol
            try:
                # Get the last traded price (LTP) for the symbol
                key = "NSE:" + symbol_to_check_ns
                resp = broker.kite.ltp(key)
                if resp and isinstance(resp, dict):
                    ltp = resp[key]['last_price']

                    # Place a buy order
                    order_id = broker.order_place(
                        tradingsymbol=symbol_to_check_ns,
                        exchange='NSE',
                        transaction_type='BUY',
                        quantity=your_quantity,  # Replace with the desired quantity
                        order_type='MARKET',
                        product='MIS',
                        variety='regular',
                        price=round_to_paise(ltp, +0.1)
                    )

                    if order_id:
                        logging.info(
                            f"BUY {order_id} placed for {symbol_to_check_ns} successfully")
                    else:
                        print(traceback.format_exc())
                        logging.error(
                            f"Unable to place order for {symbol_to_check_ns}")

            except Exception as e:
                print(traceback.format_exc())
                logging.error(
                    f"{str(e)} while processing symbol {symbol_to_check_ns}")
        else:
            # Perform actions when the market sentiment is not Bull
            print(
                f"\033[91mThe market sentiment for {symbol_to_check_ns} is not Bull\033[0m")

elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo Funds Available \033[0m")
