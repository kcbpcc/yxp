import csv
from rich import print
from rich.table import Table

def shorten_value(value, mapping):
    # Map the value to its shortened version
    return mapping.get(value, value)

def process_csv(csv_file_path):
    # Set the overall table width
    table_width = 41

    # Create a table to display the selected columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)
    table.add_column("CM", alias="C")
    table.add_column("PH", alias="P")
    table.add_column("Key")
    table.add_column("Pxy")
    table.add_column("Yxp")
    table.add_column("PnL%", alias="P%")
    table.add_column("PnL")

    # Initialize the total profit variable
    total_profit = 0

    # Mapping for shortening values in "CM" and "PH" columns
    cm_mapping = {"CNC": "C", "MIS": "M"}
    ph_mapping = {"Positions": "P", "Holdings": "H"}

    try:
        # Open the CSV file for reading
        with open(csv_file_path, newline='') as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile)

            # Skip the header row
            header_row = next(csvreader)

            # Iterate over each row in the CSV file and add it to the table
            for row in csvreader:
                # Adjust column names to match your DataFrame structure
                qty, avg, close, ltp, open_price, high, low, pnl_h, dpnl, CM, PH, key, cm, ph, pnl_percentage, pnl = row

                # Convert numerical values to strings and round them to two decimal places
                pnl_percentage = str(round(float(pnl_percentage), 2))
                pnl = str(round(float(pnl), 2))

                # Shorten the values in "CM" and "PH" columns
                cm_shortened = shorten_value(cm, cm_mapping)
                ph_shortened = shorten_value(ph, ph_mapping)

                # Accumulate the total profit
                total_profit += float(pnl)

                # Add the row to the table
                table.add_row(CM, PH, key, cm_shortened, ph_shortened, pnl_percentage, pnl)

    except FileNotFoundError:
        print("File not found!")

    # Print the table with the updated column names
    print(table)

    # Print the total profit in INR (₹) format rounded to two decimal places
    total_profit = round(total_profit, 2)
    print(f"Total Profit: ₹{total_profit:.2f}")

    # Return the total_profit value
    return total_profit

# Replace "filePnL.csv" with your actual CSV file path
csv_file_path = "filePnL.csv"
# Call the function and get the total_profit value
total_profit_main = process_csv(csv_file_path)

# Now you can use total_profit_main in your main code
# print("Total Profit in Main:", total_profit_main)






