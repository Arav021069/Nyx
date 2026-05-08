import typer
from pathlib import Path

app = typer.Typer()


@app.command()
def files(path: str):
    """
    Lists the contents of a directory, identifying which items are folders.

    Args:
        path (str): The directory path to the list.
    """
    folder = Path(path)
    for file in folder.iterdir():
        if file.is_dir():
            print(f"Folder: {file.name}")
            continue
        print(file.name)
