# Yipxy.py

import datetime

def calculate_Yi():
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Extract the time from the datetime object
    current_time = current_datetime.time()

    # Calculate Yi value based on the given criteria
    start_time = datetime.datetime.strptime("09:00", "%H:%M").time()
    end_time = datetime.datetime.strptime("15:30", "%H:%M").time()

    if start_time <= current_time <= end_time:
        # Calculate Yi value based on the time difference
        time_difference = current_datetime - datetime.datetime.combine(current_datetime.date(), start_time)
        minutes_difference = time_difference.total_seconds() / 60
        Yi_value = max(5, 15 - int(minutes_difference / 30))
        return Yi_value
    else:
        # Return 15 if outside the specified time range
        return 15



