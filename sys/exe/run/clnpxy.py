import csv
from datetime import datetime, timedelta

# Specify the path to your CSV file
file_path = 'filePnL.csv'

# Function to check if the current time is between 7:00 AM and 9:14 AM IST
def is_time_between(start_time, end_time):
    current_time = datetime.now() + timedelta(hours=5, minutes=30)  # Convert to IST
    return start_time <= current_time <= end_time

# Specify the time range during which you want to delete contents (7:00 AM to 9:14 AM IST)
start_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(hours=5, minutes=30)
end_time = datetime.now().replace(hour=9, minute=14, second=0, microsecond=0) + timedelta(hours=5, minutes=30)

# Check if the current time is within the specified range
if is_time_between(start_time, end_time):
    # Open the file in write mode to truncate its contents
    with open(file_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write an empty row to clear the contents
        csv_writer.writerow([])

    print(f"Contents of {file_path} deleted successfully at {datetime.now()}.")
else:
    print(f"Current time is not within the specified range. No deletion performed at {datetime.now()}.")

