import csv
from rich import print
from rich.table import Table

# Replace this with your CSV file path
csv_file_path = "filePnL.csv"

# Create a table to display the selected columns with custom headers
table = Table(show_header=True, header_style="bold cyan", min_width=60)
table.add_column("Source")
table.add_column("Type")
table.add_column("Key")
table.add_column("PXY")
table.add_column("PnL%")
table.add_column("PnL")

# Initialize the total profit variable
total_profit = 0

try:
    # Open the CSV file for reading
    with open(csv_file_path, newline='') as csvfile:
        # Create a CSV reader
        csvreader = csv.reader(csvfile)

        # Skip the header row
        header_row = next(csvreader)

        # Iterate over each row in the CSV file and add it to the table
        for row in csvreader:
            # Adjust column indices to match your CSV file structure
            source, product, key, qty, avg, close, ltp, open, high, low, dpnl_percentage, pxy, pnl_percentage, pnl = row

            # Convert numerical values to strings and round them to two decimal places
            pxy = str(round(float(pxy), 1))
            pnl_percentage = str(round(float(pnl_percentage), 1))
            pnl = str(round(float(pnl), 1))

            # Accumulate the total profit
            total_profit += float(pnl)

            # Add the row to the table, excluding the excluded columns
            table.add_row(source, product, key, pxy, pnl_percentage, pnl)

    # Print the table
    print(table)

    # Print the total profit in INR (₹) format rounded to two decimal places
    total_profit = round(total_profit, 2)
    print(f"Total Profit: ₹{total_profit:.2f}")

except FileNotFoundError:
    print("File not found!")
