import os
import time
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer

class Watcher:
    DIRECTORY_TO_WATCH = "C:\\Watcher"  # Set this to the directory you want to monitor

    def __init__(self):
        self.observer = Observer()
        self.event_handler = Handler()
        self.running = True

    def run(self):
        self.schedule_observer()
        print("Observer started, monitoring directory:", self.DIRECTORY_TO_WATCH)
        try:
            while self.running:
                time.sleep(5)
        except KeyboardInterrupt:
            self.stop()

    def schedule_observer(self):
        self.observer.schedule(self.event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()

    def stop(self):
        self.running = False
        self.observer.stop()
        self.observer.join()
        print("Observer stopped and resources cleaned up.")

    def clear_events(self):
        # Stop the current observer
        self.observer.unschedule_all()
        # Reset the event handler if necessary
        self.event_handler = Handler()
        # Reschedule the observer
        self.schedule_observer()
        print("Events cleared and observer rescheduled.")

class Handler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.debounce_timer = None
        self.debounce_interval = 1.0  # 1 second debounce interval
        self.last_event_path = None

    def on_any_event(self, event):
        print("*****************Start**********************")
        if event.is_directory:
            return

        if event.event_type in ('created', 'modified'):
            self.last_event_path = event.src_path
            if self.debounce_timer is not None:
                self.debounce_timer.cancel()
            self.debounce_timer = Timer(self.debounce_interval, self.process_event)
            self.debounce_timer.start()
        print("*************End********************")

    def process_event(self):
        if self.last_event_path:
            self.read_file(self.last_event_path)
            self.last_event_path = None

    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print(f"Content of {file_path}:\n{content}")
        except Exception as e:
            print(f"Failed to read file {file_path}: {e}")

def signal_handler(sig, frame):
    print('Signal received:', sig)
    watcher.clear_events()

if __name__ == '__main__':
    watcher = Watcher()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    watcher.run()
