import csv

# Specify the path to your CSV file
file_path = 'filePnL.csv'

# Open the file in write mode to truncate its contents
with open(file_path, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write an empty row to clear the contents
    csv_writer.writerow([])
