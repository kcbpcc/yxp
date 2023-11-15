import datetime
import pytz

def calculate_Yi():
    # Define the time zone (Indian Standard Time)
    ist_timezone = pytz.timezone('Asia/Kolkata')

    # Get the current date and time in IST
    current_datetime_ist = datetime.datetime.now(ist_timezone)

    # Convert the current IST time to UTC
    current_datetime_utc = current_datetime_ist.astimezone(pytz.utc)

    # Extract the time from the UTC datetime object
    current_time_utc = current_datetime_utc.time()

    # Convert start and end times to UTC
    start_time_utc = datetime.datetime.combine(current_datetime_utc.date(), datetime.datetime.strptime("09:00", "%H:%M").time()).astimezone(pytz.utc)
    end_time_utc = datetime.datetime.combine(current_datetime_utc.date(), datetime.datetime.strptime("15:30", "%H:%M").time()).astimezone(pytz.utc)

    if start_time_utc <= current_datetime_utc <= end_time_utc:
        # Calculate Yi value based on the time difference
        time_difference = current_datetime_utc - datetime.datetime.combine(current_datetime_utc.date(), datetime.datetime.min.time().replace(tzinfo=pytz.utc))
        minutes_difference = time_difference.total_seconds() / 60
        Yi = max(5, round(15 - minutes_difference / 30, 1))
        return Yi
    else:
        # Return 15 if outside the specified time range
        return 15

# Example usage:
result = calculate_Yi()
print(f"Yi value: {result}")







