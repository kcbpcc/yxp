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

    # Get the current UTC time
    current_datetime_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    
    print(f"Current IST Time: {current_datetime_ist}")
    print(f"Current UTC Time: {current_datetime_utc}")
    print(f"Start Time IST: {start_time_ist}")
    print(f"End Time IST: {end_time_ist}")

    if start_time_ist <= current_datetime_ist <= end_time_ist:
        # Calculate Yi value based on the time difference
        time_difference = current_datetime_ist - datetime.datetime.combine(current_datetime_ist.date(), datetime.datetime.min.time().replace(tzinfo=ist_timezone))
        minutes_difference = time_difference.total_seconds() / 60
        print(f"Minutes Difference: {minutes_difference}")
        Yi = max(5, round(15 - minutes_difference / 30, 1))
        return Yi
    else:
        # Return 15 if outside the specified time range
        return 15

# Example usage:
result = calculate_Yi()
print(f"Yi value: {result}")
print(f"Current IST Time: {current_datetime_ist}")
print(f"Current UTC Time: {current_datetime_utc}")
print(f"Start Time IST: {start_time_ist}")
print(f"End Time IST: {end_time_ist}")






