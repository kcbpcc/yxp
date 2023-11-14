import datetime
import time

def calculate_Yi(current_time):
    # Calculate Yi value based on the given criteria
    start_time = datetime.datetime.strptime("09:00", "%H:%M")
    end_time = datetime.datetime.strptime("15:30", "%H:%M")

    if start_time <= current_time <= end_time:
        # Calculate Yi value based on the time difference
        time_difference = current_time - start_time
        minutes_difference = time_difference.total_seconds() / 60
        Yi_value = max(5, 15 - int(minutes_difference / 30))
        return Yi_value
    else:
        # Return 15 if outside the specified time range
        return 15

if __name__ == "__main__":
    while True:
        current_time = datetime.datetime.now().time()
        Yi = calculate_Yi(current_time)


