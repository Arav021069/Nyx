import typer
from pathlib import Path
import subprocess
from datetime import datetime

app = typer.Typer()

NOTES_FILE = Path.home() / ".nyx" / "notes.txt"


def ensure_file():
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.touch(exist_ok=True)


@app.command()
def add(text: str):
    ensure_file()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(NOTES_FILE, "a") as f:
        f.write(f"[{timestamp}] {text}\n")

    print("Note added.")


@app.command()
def list():
    ensure_file()
    print(NOTES_FILE.read_text())


@app.command()
def search(query: str):
    ensure_file()
    lines = NOTES_FILE.read_text().splitlines()

    for line in lines:
        if query.lower() in line.lower():
            print(line)


@app.command()
def clear():
    ensure_file()
    NOTES_FILE.write_text("")
    print("All notes cleared.")


@app.command()
def edit():
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.touch(exist_ok=True)

    subprocess.run(["notepad", str(NOTES_FILE)])