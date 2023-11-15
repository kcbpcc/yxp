import csv
from datetime import datetime, timedelta
import pytz

# Specify the path to your CSV file
file_path = 'filePnL.csv'

# Function to check if the current time is between 7:00 AM and 9:14 AM IST
def is_time_between(start_time, end_time):
    current_time = datetime.now(ist_timezone)
    return start_time <= current_time <= end_time

# Define the time zone (Indian Standard Time)
ist_timezone = pytz.timezone('Asia/Kolkata')

# Specify the time range during which you want to delete contents (7:00 AM to 9:14 AM IST)
start_time = ist_timezone.localize(datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=7))
end_time = ist_timezone.localize(datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=9, minutes=14))

# Check if the current time is within the specified range
if is_time_between(start_time, end_time):
    # Open the file in write mode to truncate its contents
    with open(file_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write an empty row to clear the contents
        csv_writer.writerow([])
