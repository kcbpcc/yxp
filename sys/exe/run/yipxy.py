import datetime
import pytz

def calculate_Yi():
    # Define the time zone (Indian Standard Time)
    ist_timezone = pytz.timezone('Asia/Kolkata')

    # Get the current date and time in IST
    current_datetime_ist = datetime.datetime.now(ist_timezone)

    # Convert the current IST time to UTC
    current_datetime_utc = current_datetime_ist.astimezone(pytz.utc)

    # Convert start time to UTC
    start_time_utc = ist_timezone.localize(datetime.datetime.strptime("09:00", "%H:%M")).astimezone(pytz.utc).time()
    end_time_utc = ist_timezone.localize(datetime.datetime.strptime("15:30", "%H:%M")).astimezone(pytz.utc).time()

    # Extract the time from the UTC datetime object
    current_time_utc = current_datetime_utc.time()

    if start_time_utc <= current_time_utc <= end_time_utc:
        # Calculate Yi value based on the time difference
        time_difference = current_datetime_utc - datetime.datetime.combine(current_datetime_utc.date(), datetime.datetime.min.time())
        minutes_difference = time_difference.total_seconds() / 60
        Yi = max(5, round(15 - minutes_difference / 30, 1))
        return Yi
    else:
        # Return 15 if outside the specified time range
        return 15

# Example usage:
result = calculate_Yi()
#print(f"Yi value: {result}")





