import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SensorSOC(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"[!] ALERTA: Archivo modificado: {event.src_path}")
    def on_created(self, event):
        print(f"[+] NOTIFICACIÓN: Nuevo archivo detectado: {event.src_path}")

if __name__ == "__main__":
    print("[-] JARVIS: Sensor de Integridad Activo. Vigilando el sector...")
    event_handler = SensorSOC()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
