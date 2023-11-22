import csv
from rich import print
from rich.table import Table

def process_dataframe(EXE_df):
    # Set the overall table width
    table_width = 41

    # Create a table to display the selected columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)
    table.add_column("Product")
    table.add_column("Source")
    table.add_column("Key")
    table.add_column("Pxy")
    table.add_column("Yxp")
    table.add_column("PnL%")
    table.add_column("PnL")

    # Initialize the total profit variable
    total_profit = 0

    try:
        # Check if the DataFrame is not empty
        if not EXE_df.empty:
            # Iterate over each row in the DataFrame and add it to the table
            for _, row in EXE_df.iterrows():
                # Extract the last 7 columns
                product, source, key, pxy, yxp, pnl_percentage, pnl = row[-7:]

                # Convert numerical values to strings and round them to two decimal places
                pnl_percentage = str(round(float(pnl_percentage), 2))
                pnl = str(round(float(pnl), 2))

                # Accumulate the total profit
                total_profit += float(pnl)

                # Add the row to the table
                table.add_row(product, source, key, pxy, yxp, pnl_percentage, pnl)
        else:
            print("DataFrame is empty!")

    except FileNotFoundError:
        print("File not found!")

    # Print the table with the updated column names
    print(table)

    # Print the total profit in INR (₹) format rounded to two decimal places
    total_profit = round(total_profit, 2)
    print(f"Total Profit: ₹{total_profit:.2f}")

    # Return the total_profit value
    return total_profit

# Assuming you have a DataFrame named EXE_df
# EXE_df = pxy_df[['qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'PnL%_H', 'dPnL%', 'product', 'source', 'key', 'pxy', 'yxp', 'PnL%', 'PnL']]
# Call the function and get the total_profit value
total_profit_main = process_dataframe(EXE_df)

# Now you can use total_profit_main in your main code
# print("Total Profit in Main:", total_profit_main)





