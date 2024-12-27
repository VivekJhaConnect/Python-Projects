import time
import signal
import sys
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

    @staticmethod
    def on_any_event(event):
        thread = threading.Thread(target=Handler.handle_event, args=(event,))
        thread.start()

    @staticmethod
    def handle_event(event):
        print("******************************Start*****************************")
        print(event.event_type)
        if event.is_directory:
            if event.event_type == 'created':
                print(f"Directory created - {event.src_path}")
            if event.event_type == 'modified':
                print(f"Directory modified - {event.src_path}")
            elif event.event_type == 'deleted':
                print(f"Directory deleted - {event.src_path}")
        else:
            if event.event_type == 'created':
                print(f"File created - {event.src_path}")
            elif event.event_type == 'modified':
                print(f"File modified - {event.src_path}")
            elif event.event_type == 'deleted':
                print(f"File deleted - {event.src_path}")
        print("******************************End*****************************")

def signal_handler(sig, frame):
    print('Signal received:', sig)
    watcher.clear_events()

if __name__ == '__main__':
    watcher = Watcher()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    watcher.run()
