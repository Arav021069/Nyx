import typer
from rich.console import Console
import subprocess
from datetime import datetime
import os
import shutil
import platform

from Nyx.utils.formatters import ensure_file

console = Console()
app = typer.Typer()


@app.command()
def add(text: str):
    path = ensure_file()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(path, "a") as f:
        f.write(f"[{timestamp}] {text}\n")

    console.print("Note added.")


@app.command()
def list():
    path = ensure_file()
    console.print(path.read_text())


@app.command()
def search(query: str):
    path = ensure_file()
    lines = path.read_text().splitlines()

    for line in lines:
        if query.lower() in line.lower():
            console.print(line)


@app.command()
def clear():
    path = ensure_file()
    path.write_text("")
    console.print("All notes cleared.")


@app.command()
def edit():
    """
     Open the note file in the default editor.
     """
    path = ensure_file()

    editor = os.environ.get("EDITOR")
    try:
        if editor:
            subprocess.run([editor, str(path)])

        elif platform.system() == "Windows":
            subprocess.run(["notepad", str(path)])

        elif platform.system() in ["Linux", "Darwin"]:
            subprocess.run(["nano", str(path)])

    except FileNotFoundError:
        console.print("Editor not found. Please set the EDITOR environment variable.")