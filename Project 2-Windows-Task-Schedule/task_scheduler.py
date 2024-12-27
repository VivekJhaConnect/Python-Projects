import schedule
import time
import logging

class TaskScheduler:
    def __init__(self, log_file="task_scheduler.log"):
        self.scheduler = schedule
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    def log_message(self, message):
        print(message)
        logging.info(message)

    def print_message(self):
        message = f"Task executed at: {time.strftime('%H:%M:%S')}"
        self.log_message(message)

    def schedule_task(self, interval_seconds):
        self.scheduler.every(interval_seconds).seconds.do(self.print_message)
        self.log_message(f"Task scheduled to run every {interval_seconds} seconds.")

    def run(self):
        try:
            while True:
                self.scheduler.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.log_message("Scheduler stopped.")
            print("Scheduler stopped.")

if __name__ == "__main__":
    task_scheduler = TaskScheduler()
    task_scheduler.schedule_task(5)  # Schedule the task to run every 5 seconds
    task_scheduler.run()
