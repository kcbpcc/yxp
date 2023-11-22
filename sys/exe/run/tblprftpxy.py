import csv
from rich import print
from rich.table import Table

def process_dataframe(exe_df):
    # Set the overall table width
    table_width = 80

    # Create a table to display the selected columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)
    table.add_column("CM", width=10)  # Set a fixed width for 'CM'
    table.add_column("PH", width=10)  # Set a fixed width for 'PH'
    table.add_column("Key")
    table.add_column("PnL%")
    table.add_column("PnL")

    # Initialize the total profit variable
    total_profit = 0

    try:
        # Iterate over each row in the data frame and add it to the table
        for index, row in exe_df.iterrows():
            # Adjust column names to match your data frame structure
            qty = row.get('qty', '')
            avg = row.get('avg', '')
            close = row.get('close', '')
            ltp = row.get('ltp', '')
            open_price = row.get('open', '')
            high = row.get('high', '')
            low = row.get('low', '')
            pnl_h = row.get('PnL%_H', '')
            dpnl = row.get('dPnL%', '')
            
            # Take only the first letter of 'product' to represent 'CM'
            cm = row.get('product', '')[0]
            
            # Take only the first letter of 'source' to represent 'PH'
            ph = row.get('source', '')[0]
            
            key = row.get('key', '')
            pnl_percentage = row.get('PnL%', '')
            pnl = row.get('PnL', '')

            # Remove "NSE:" or "BSE:" prefix from the "Key" column
            key = key.replace("NSE:", "").replace("BSE:", "")

            # Convert numerical values to strings and round them to two decimal places
            pnl_percentage = str(round(float(pnl_percentage), 2))
            pnl = str(round(float(pnl), 2))

            # Accumulate the total profit
            total_profit += float(pnl)

            # Add the row to the table
            table.add_row(cm, ph, key, pnl_percentage, pnl)

    except Exception as e:
        print(f"Error: {e}")

    # Print the table with the updated column names
    print(table)

    # Print the total profit in INR (₹) format rounded to two decimal places
    total_profit = round(total_profit, 2)
    print(f"Total Profit: ₹{total_profit:.2f}")

    # Return the total_profit value
    return total_profit

# Assuming EXE_df is your data frame
# Call the function and get the total_profit value
total_profit_main = process_dataframe(EXE_df)

# Now you can use total_profit_main in your main code
# print("Total Profit in Main:", total_profit_main)








