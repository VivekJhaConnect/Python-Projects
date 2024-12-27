import schedule
import time
import logging

# Setup logging
log_file = "scheduled_task.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def print_message():
    message = f"Task executed at: {time.strftime('%H:%M:%S')}"
    print(message)
    logging.info(message)

# Schedule task to run every 5 seconds
schedule.every(5).seconds.do(print_message)

# Keep the program running to allow scheduled tasks to execute
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Scheduler stopped.")
    logging.info("Scheduler stopped.")
