import typer
from rich.console import Console
from pathlib import Path
from Nyx.utils.formatters import validate_path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

app = typer.Typer()
console = Console()


class Watcher(FileSystemEventHandler):

    def __init__(self, target):
        self.target = target

    def on_modified(self, event):
        event_path = Path(event.src_path).resolve()

        if self.target.is_file():
            if event_path == self.target:
                console.print(
                    f"[green]Modified:[/green] {self.target.name}"
                )
        else:
            console.print(
                f"[green]Modified:[/green] {event_path.name}"
            )


@app.callback(invoke_without_command=True)
def watch_directory(path: str):
    validate_path(path)
    path = Path(path).resolve()

    if path.is_file():
        watch_dir = path.parent
    else:
        watch_dir = path

    console.print(f"Watching: {path}")

    observer = Observer()

    observer.schedule(Watcher(path), str(watch_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
