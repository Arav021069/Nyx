import typer
from rich.console import Console
from pathlib import Path
from Nyx.utils.formatters import validate_path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
from datetime import datetime

app = typer.Typer(help="Watch a directory for changes")
console = Console()

EVENT_COLORS = {
            "Created": "green",
            "Modified": "yellow",
            "Deleted": "red",
            "Moved": "cyan",
        }


class Watcher(FileSystemEventHandler):

    def __init__(self, target, log: Path | None = None):
        self.target = target
        self.log = (log / "watch.log" if log and log.is_dir() else log)
        self.log = self.log.resolve() if self.log else None

    def _print_event(self, action: str, event):
        # if event.is_directory:
        #     return
        event_path = Path(event.src_path).resolve()

        if self.log and event_path == self.log:
            return

        # If we are watching a specific file, ignore everything else
        if self.target.is_file():
            if event_path != self.target:
                return
            display_path = event_path.name
        else:
            display_path = event_path.relative_to(self.target)

        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] [{EVENT_COLORS[action]}]{action}:[/{EVENT_COLORS[action]}] {display_path}"
        console.print(message)

        if self.log:
            with open(self.log, "a", encoding="utf-8") as f:
                f.write(message + "\n")

    def on_modified(self, event):
        self._print_event("Modified", event)

    def on_created(self, event):
        self._print_event("Created", event)

    def on_deleted(self, event):
        self._print_event("Deleted", event)

    def on_moved(self, event):
        # self._print_event("Moved", path)
        if event.is_directory:
            return

        src_path = Path(event.src_path).resolve()
        dest_path = Path(event.dest_path).resolve()

        if self.target.is_file():
            if src_path != self.target:
                return

        console.print(
            f"[cyan]Moved:[/cyan] "
            f"{src_path.name}"
            f" → "
            f"{dest_path.name}"
        )


@app.callback(invoke_without_command=True)
def watch_directory(
        path: str = typer.Argument(
            ".",
            help="Directory or file to watch"
        ),
        recursive: bool = typer.Option(
            False,
            "--recursive",
            "-r",
            help="Watch subdirectories recursively"
        ),
        log: Path | None = typer.Option(
            None,
            "--log",
            "-l",
            help="Write events to a log file"
        )
):
    path = Path(path).resolve()
    validate_path(path)

    if path.is_file():
        watch_dir = path.parent
    else:
        watch_dir = path

    mode = " (recursive)" if recursive else ""
    console.print(f"Watching: {path}{mode}")

    observer = Observer()

    observer.schedule(Watcher(path, log), str(watch_dir), recursive=recursive)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping Nyx Watch[/yellow]")
        observer.stop()

    observer.join()
# TODO: Normalize Windows Extended-Length Paths
