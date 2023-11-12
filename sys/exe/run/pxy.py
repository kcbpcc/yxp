import time
from datetime import datetime

while True:
    now = datetime.now().time()
    market_open_time = datetime.strptime("09:00", "%H:%M").time()
    market_close_time = datetime.strptime("15:30", "%H:%M").time()

    if market_open_time <= now <= market_close_time:
        # Inside market hours - your existing code here
        print("Inside market hours")
      
    else:
        # Outside market hours - your additional action here
        print("Outside market hours")

        # Perform some action outside market hours here

        # Break out of the loop if needed
        break

    # Sleep for a while before the next iteration
    time.sleep(60)  # Sleep for 60 seconds (adjust as needed)
