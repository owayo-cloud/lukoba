import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_any_event(self, event):
        if event.is_directory:
            return
        self.restart_server()

    def restart_server(self):
        print("Changes detected. Restarting server...")
        self.process.terminate()
        self.process.wait()
        self.process = subprocess.Popen(['python', 'server.py'])

def start_server():
    process = subprocess.Popen(['python', 'server.py'])
    return process

if __name__ == "__main__":
    server_process = start_server()
    event_handler = ChangeHandler(server_process)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    print("Watching for file changes...")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    server_process.terminate()
