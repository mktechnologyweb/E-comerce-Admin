import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback

    def on_any_event(self, event):
        if event.src_path.endswith(".py") or event.src_path.endswith(".html") or event.src_path.endswith(".css") or event.src_path.endswith(".js"):
            print(f"Arquivo alterado: {event.src_path}")
            self.restart_callback()

class ServerWatcher:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = directory_to_watch
        self.server_process = None
        self.observer = Observer()

    def start(self):
        self.run_server()
        event_handler = ChangeHandler(self.restart_server)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Monitoramento interrompido.")
        
        self.observer.join()

    def run_server(self):
        print("Iniciando servidor...")
        self.server_process = subprocess.Popen(['python', 'app.py'])

    def restart_server(self):
        print("Reiniciando servidor...")
        if self.server_process:
            self.server_process.kill()
        self.run_server()

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    server_watcher = ServerWatcher(path)
    server_watcher.start()
