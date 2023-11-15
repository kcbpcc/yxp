import datetime
import pytz

def calculate_Yi():
    # Define the time zone (Indian Standard Time)
    ist_timezone = pytz.timezone('Asia/Kolkata')

    # Get the current date and time in IST
    current_datetime_ist = datetime.datetime.now(ist_timezone)

    # Define the start and end times in IST
    start_time_ist = datetime.datetime.combine(current_datetime_ist.date(), datetime.time(9, 0)).astimezone(ist_timezone)
    end_time_ist = datetime.datetime.combine(current_datetime_ist.date(), datetime.time(15, 30)).astimezone(ist_timezone)

    # Calculate Yi value based on the time difference
    if start_time_ist <= current_datetime_ist <= end_time_ist:
        total_minutes = (current_datetime_ist - start_time_ist).total_seconds() / 60
        Yi = max(5, round(15 - total_minutes / 30, 1))
        return Yi
    else:
        # Return 15 if outside the specified time range
        return 15

# Example usage:
result = calculate_Yi()
#print(f"Yi value: {result}")
