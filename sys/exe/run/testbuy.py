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
from ynfndpxy import calculate_decision
from mktpxy import mktpxy
from mktchksmbl import check_market_sentiment_for_symbol  # Import the function

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

        with open(black_file, 'w+'):
            pass

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

# Call the calculate_decision function to get the decision
decision = calculate_decision()

# Check if the decision is "YES" and market sentiment is 'Buy' or 'Bull'
if decision == "YES" and check_market_sentiment_for_symbol(mktpxy) in ['Buy', 'Bull']:
    try:
        lst = []
        file_size_in_bytes = os.path.getsize(holdings)
        logging.debug(f"holdings file size: {file_size_in_bytes} bytes")

        if file_size_in_bytes > 50:
            logging.debug(f"reading from csv ...{holdings}")
            df_holdings = pd.read_csv(holdings)

            if not df_holdings.empty:
                lst = df_holdings['tradingsymbol'].to_list()

        # get list from Trendlyne
        lst_tlyne = []
        lst_dct_tlyne = Trendlyne().entry()

        if lst_dct_tlyne and any(lst_dct_tlyne):
            print(pd.DataFrame(lst_dct_tlyne).set_index('tradingsymbol').rename_axis('Trendlyne'), "\n")
            lst_tlyne = [dct['tradingsymbol'] for dct in lst_dct_tlyne]

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read holdings or Trendlyne calls")
        sys.exit(1)

    try:
        if any(lst_tlyne):
            logging.info(f"reading trendlyne ...{lst_tlyne}")
            lst_tlyne = [x for x in lst_tlyne if x not in lst]

            logging.info(f"filtered from holdings: {lst}")

            # get list from positions
            lst_dct = broker.positions

            if lst_dct and any(lst_dct):
                lst = [dct['symbol'] for dct in lst_dct]
                lst_tlyne = [x for x in lst_tlyne if x not in lst]

                logging.info(f"filtered from positions ...{lst}")

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read positions")
        sys.exit(1)

    def calc_target(ltp, perc):
        resistance = round_to_paise(ltp, perc)
        target = round_to_paise(ltp, max_target)
        return max(resistance, target)

    def transact(dct):
        try:
            def get_ltp():
                ltp = -1
                key = "NSE:" + dct['tradingsymbol']
                resp = broker.kite.ltp(key)

                if resp and isinstance(resp, dict):
                    ltp = resp[key]['last_price']

                return ltp

            ltp = get_ltp()
            logging.info(f"ltp for {dct['tradingsymbol']} is {ltp}")

            if ltp <= 0:
                return dct['tradingsymbol']

            order_id = broker.order_place(
                tradingsymbol=dct['tradingsymbol'],
                exchange='NSE',
                transaction_type='BUY',
                quantity=int(float(dct['QTY'].replace(',', ''))),
                order_type='MARKET',
                product='MIS',
                variety='regular',
                price=round_to_paise(ltp, +0.1)
            )

            if order_id:
                logging.info(f"BUY {order_id} placed for {dct['tradingsymbol']} successfully")

            else:
                print(traceback.format_exc())
                logging.error(f"unable to place order for {dct['tradingsymbol']}")
                return dct['tradingsymbol']

        except Exception as e:
            print(traceback.format_exc())
            logging.error(f"{str(e)} while placing order for {dct['tradingsymbol']}")
            return dct['tradingsymbol']

    if any(lst_tlyne):
        new_list = []

        # Filter the original list based on the subset of 'tradingsymbol' values
        lst_all_orders = [d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]

        # Read the list of previously failed symbols from the file
        with open(black_file, 'r') as file:
            lst_failed_symbols = [line.strip() for line in file.readlines()]

        logging.info(f"ignored symbols: {lst_failed_symbols}")

        lst_orders = [d for d in lst_all_orders if d['tradingsymbol'] not in lst_failed_symbols]

        for d in lst_orders:
            failed_symbol = transact(d)

            if failed_symbol:
                new_list.append(failed_symbol)

            Utilities().slp_til_nxt_sec()

        if any(new_list):
            with open(black_file, 'w') as file:
                for symbol in new_list:
                    file.write(symbol + '\n')

elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo Funds Available \033[0m")
