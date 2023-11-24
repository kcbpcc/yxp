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
import ynfndpxy
from ynfndpxy import calculate_decision
from mktpxy import mktpxy
from mktchksmbl import getsmktchk


logging = Logger(10)
holdings = dir_path + "holdings.csv"
black_file = dir_path + "blacklist.txt"
try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
##    sys.stdout.close()
##    sys.stdout = sys.__stdout__
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

if decision == "YES" and mktpxy in ['Buy', 'Bull']:


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
            print(pd.DataFrame(
                lst_dct_tlyne).set_index('tradingsymbol').rename_axis('Trendlyne'), "\n")
            lst_tlyne = [dct['tradingsymbol'] for dct in lst_dct_tlyne]
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read holdings or Trendlyne calls")
        sys.exit(1)

    try:
        if any(lst_tlyne):
            logging.info(f"reading trendlyne ...{lst_tlyne}")
            lst_tlyne = [
                x for x in lst_tlyne if x not in lst]
            logging.info(f"filtered from holdings: {lst}")

            # Get lists from positions, orders, and holdings
            lst_dct_positions = broker.kite.positions()
            lst_dct_orders = broker.kite.orders
            lst_dct_holdings = broker.kite.holdings  # Replace with the actual way to get holdings
            
            # Extract symbols from positions
            if lst_dct_positions and any(lst_dct_positions):
                lst_positions = [position['symbol'] for position in lst_dct_positions]
            else:
                lst_positions = []
            
            # Extract symbols from orders
            if lst_dct_orders and any(lst_dct_orders):
                lst_orders = [order['symbol'] for order in lst_dct_orders]
            else:
                lst_orders = []
            
            # Extract symbols from holdings
            if lst_dct_holdings and any(lst_dct_holdings):
                lst_holdings = [holding['symbol'] for holding in lst_dct_holdings]
            else:
                lst_holdings = []
            
            # Combine symbols from positions, orders, and holdings
            combined_symbols = set(lst_positions + lst_orders + lst_holdings)
            
            # Filter lst_tlyne based on combined symbols
            lst_tlyne = [x for x in lst_tlyne if x not in combined_symbols]
            
            # Log information
            logging.info(f"filtered from positions: {lst_positions}")
            logging.info(f"filtered from orders: {lst_orders}")
            logging.info(f"filtered from holdings: {lst_holdings}")

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read positions")
        sys.exit(1)

    def calc_target(ltp, perc):
        resistance = round_to_paise(ltp, perc)
        target = round_to_paise(ltp, max_target)
        return max(resistance, target)

    def transact(dct, broker,):
        
        tradingsymbol = dct['tradingsymbol']
        symbol = tradingsymbol + ".NS"  # Append ".NS" to the tradingsymbol
        smktchk = getsmktchk(symbol,'5')
    
        try:
            def get_ltp():
                ltp = -1
                key = "NSE:" + tradingsymbol
                resp = broker.kite.ltp(key)
                if resp and isinstance(resp, dict):
                    ltp = resp[key]['last_price']
                return ltp
    
            ltp = get_ltp()
            logging.info(f"ltp for {tradingsymbol} is {ltp}")
    
            if ltp <= 0:
                return tradingsymbol
    
            # Check if the market condition is "Buy" or "Bull"
            if smktchk not in ["Buy", "Bull"]:
                logging.info(f"Not placing order for {tradingsymbol} because market condition is {smktchk}")
                return tradingsymbol
    
            order_id = broker.order_place(
                tradingsymbol=tradingsymbol,
                exchange='NSE',
                transaction_type='BUY',
                quantity=int(float(dct['QTY'].replace(',', ''))),
                order_type='MARKET',
                product='MIS',
                variety='regular',
                price=round_to_paise(ltp, +0.1)
            )
    
            if order_id:
                logging.info(f"BUY {order_id} placed for {tradingsymbol} successfully")
            else:
                print(traceback.format_exc())
                logging.error(f"Unable to place order for {tradingsymbol}")
                return tradingsymbol
    
        except Exception as e:
            print(traceback.format_exc())
            logging.error(f"{str(e)} while placing order")
            return tradingsymbol

    if any(lst_tlyne):
        new_list = []
        # Filter the original list based on the subset of 'tradingsymbol' values
        lst_all_orders = [
            d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]
        # Read the list of previously failed symbols from the file
        with open(black_file, 'r') as file:
            lst_failed_symbols = [line.strip() for line in file.readlines()]
        logging.info(f"ignored symbols: {lst_failed_symbols}")
        lst_orders = [d for d in lst_all_orders if d['tradingsymbol']
                    not in lst_failed_symbols]
        for d in lst_orders:
            failed_symbol = transact(d, broker)  # Pass the broker instance
            if failed_symbol:
                new_list.append(failed_symbol)
            Utilities().slp_til_nxt_sec()
        if any(new_list):
            with open(black_file, 'w') as file:
                for symbol in new_list:
                    file.write(symbol + '\n')
elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo Funds Avalable \033[0m") 

