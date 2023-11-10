from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
import pandas as pd
import traceback
import sys
import os
import ynfndpxy
from ynfndpxy import calculate_decision
from mktpxy import mktpxy
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from byhopxy import get

# Set up Chrome options for running in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU for headless mode

# Create a WebDriver instance with the specified Chrome options
driver = webdriver.Chrome(options=chrome_options)

# Rest of your code remains the same
url = 'https://scanners.streak.tech/scanner/minuspxy'
driver.get(url)

# Wait for the "Run Scan >>" button to be clickable (increased timeout to 20 seconds)
wait = WebDriverWait(driver, 5)
scan_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Run Scan')]")))
scan_button.click()



# Wait for the table to load (you may need to adjust this wait time)
time.sleep(2)

# Capture the page source after clicking the button
page_source = driver.page_source

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Locate the table containing stock information
table = soup.find('table')

if table:
    with open('../minuspxy.txt', 'w') as file:  # Use '../' to refer to the parent directory
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if columns:
                first_column = columns[0].text.strip()  # Extract data from the first column
                file.write(first_column + '\n')

### Print the contents of the file
##with open('../minuspxy.txt', 'r') as file:  # Use '../' to refer to the parent directory
##    file_contents = file.read()
##    print("File Contents:")
##    print(file_contents)

        
# Close the browser window
driver.quit()


# Initialize the Logger
logging = Logger(10)
holdings = dir_path + "holdings.csv"
black_file = dir_path + "blacklist.txt"

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)

    if fileutils.is_file_not_2day(holdings):
        logging.debug("Getting holdings for the day...")
        resp = broker.kite.holdings()
        if resp and any(resp):
            df = get(resp)
            logging.debug(f"Writing to CSV... {holdings}")
            df.to_csv(holdings, index=False)
        with open(black_file, 'w+'):
            pass
except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} Unable to get holdings")
    sys.exit(1)

# Call the calculate_decision function to get the decision
decision = calculate_decision()

if decision == "YES" and mktpxy in ['Buy','Bull','Sell','Bear']:
    try:
        lst = []
        file_size_in_bytes = os.path.getsize(holdings)
        logging.debug(f"Holdings file size: {file_size_in_bytes} bytes")
        if file_size_in_bytes > 10:
            logging.debug(f"Reading from CSV... {holdings}")
            df_holdings = pd.read_csv(holdings)
            if not df_holdings.empty:
                lst = df_holdings['tradingsymbol'].to_list()

        # Read symbols from the "minuspxy.txt" file
        with open('../minuspxy.txt', 'r') as file:
            lst_tlyne = [line.strip().replace('NSE', '') for line in file]
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} Unable to read holdings or Trendlyne calls")
        sys.exit(1)

    try:
        if any(lst_tlyne):
            logging.info(f"Reading symbols from the website... {lst_tlyne}")
            lst_tlyne = [x for x in lst_tlyne if x not in lst]
            logging.info(f"Filtered from holdings: {lst}")

            # Get list from positions
            lst_dct = broker.positions
            if lst_dct and any(lst_dct):
                lst = [dct['symbol'] for dct in lst_dct]
                lst_tlyne = [x for x in lst_tlyne if x not in lst]
                logging.info(f"Filtered from positions: {lst}")
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} Unable to read positions")
        sys.exit(1)


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
            logging.info(f"LTP for {dct['tradingsymbol']} is {ltp}")
            if ltp <= 0:
                return dct['tradingsymbol']

            # Define calculated as 10000 divided by ltp, rounded to 0 decimal places
            calculated = round(50000 / ltp, 0)

            order_id = broker.order_place(
                tradingsymbol=dct['tradingsymbol'],
                exchange='NSE',
                transaction_type='SELL',
                quantity=int(float(calculated)),  # Use calculated instead of dct['calculated']
                order_type='LIMIT',
                product='MIS',
                variety='regular',
                price=round_to_paise(ltp, -0.2)
            )
            if order_id:
                logging.info(
                    f"SELL {order_id} placed for {dct['tradingsymbol']} successfully")
            else:
                print(traceback.format_exc())
                logging.error(f"Unable to place an order for {dct['tradingsymbol']}")
                return dct['tradingsymbol']
        except Exception as e:
            print(traceback.format_exc())
            logging.error(f"{str(e)} while placing an order")
            return dct['tradingsymbol']


    if any(lst_tlyne):
        new_list = []
        # Filter the original list based on the subset of 'tradingsymbol' values
        lst_all_orders = [{'tradingsymbol': symbol} for symbol in lst_tlyne]
        # Read the list of previously failed symbols from the file
        with open(black_file, 'r') as file:
            lst_failed_symbols = [line.strip() for line in file.readlines()]
        logging.info(f"Ignored symbols: {lst_failed_symbols}")
        lst_orders = [d for d in lst_all_orders if d['tradingsymbol']
                      not in lst_failed_symbols]
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
