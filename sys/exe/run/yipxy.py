import datetime
import pytz

def calculate_Yi():
    # Define the time zone (UTC)
    utc_timezone = pytz.timezone('UTC')

    # Get the current date and time in UTC
    current_datetime_utc = datetime.datetime.now(utc_timezone)

    # Set the start and end times in UTC
    start_time_utc = datetime.datetime(current_datetime_utc.year, current_datetime_utc.month, current_datetime_utc.day, 3, 30, tzinfo=utc_timezone)
    end_time_utc = datetime.datetime(current_datetime_utc.year, current_datetime_utc.month, current_datetime_utc.day, 10, 0, tzinfo=utc_timezone)

    if start_time_utc <= current_datetime_utc <= end_time_utc:
        # Calculate Yi value based on the time difference
        time_difference = current_datetime_utc - datetime.datetime.combine(current_datetime_utc.date(), datetime.datetime.min.time().replace(tzinfo=utc_timezone))
        minutes_difference = time_difference.total_seconds() / 60
        Yi = max(5, round(15 - minutes_difference / 30, 1))
        return Yi
    else:
        # Return 15 if outside the specified time range
        return 15

# Example usage:
result = calculate_Yi()
print(f"Yi value: {result}")








