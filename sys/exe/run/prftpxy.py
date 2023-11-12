import csv
from rich import print
from rich.table import Table

# Replace this with your CSV file path
csv_file_path = "filePnL.csv"

# Set the overall table width
table_width = 35

# Create a table to display the selected columns with custom headers
table = Table(show_header=True, header_style="bold cyan", min_width=table_width)
table.add_column("PH")
table.add_column("CM")
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

        # Rename the columns in the table
        table.field_names = ["P/H" if col.lower() == "PH" else ("C/M" if col.lower() == "CM" else col) for col in header_row]

        # Iterate over each row in the CSV file and add it to the table
        for row in csvreader:
            # Adjust column indices to match your CSV file structure
            PH, CM, key, qty, avg, close, ltp, open, high, low, dpnl_percentage, pxy, pnl_percentage, pnl = row

            # Remove "NSE:" or "BSE:" prefix from the "Key" column
            key = key.replace("NSE:", "").replace("BSE:", "")

            # Convert numerical values to strings and round them to two decimal places
            pxy = str(round(float(pxy), 1))
            pnl_percentage = str(round(float(pnl_percentage), 1))
            pnl = str(round(float(pnl)))

            # Map product values
            product_mapping = {"CNC": "C", "MIS": "M"}
            mapped_product = product_mapping.get(product.upper(), product)

            # Map PH values
            PH_mapping = {"positions": "P", "holdings": "H"}
            mapped_PH = PH_mapping.get(PH.lower(), PH)

            # Accumulate the total profit
            total_profit += float(pnl)

            # Add the row to the table
            table.add_row(mapped_PH, mapped_product, key, pxy, pnl_percentage, pnl)

    # Print the table with the updated column names
    print(table)

    # Print the total profit in INR (₹) format rounded to two decimal places
    total_profit = round(total_profit, 2)
    print(f"Total Profit: ₹{total_profit:.2f}")

except FileNotFoundError:
    print("File not found!")
