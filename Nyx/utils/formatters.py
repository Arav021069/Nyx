from pathlib import Path
import typer
from rich.console import Console

console = Console()


def format_size(size_bytes: int, byte_unit: str = None) -> str:
    """
    Converts bytes into a human-readable format.
    """

    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        if byte_unit is not None and byte_unit == unit:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def validate_path(path: str | Path) -> Path:
    """checks if the path exists and is a valid path"""

    p = Path(path).resolve()

    if not p.exists():
        console.print(
            "[bold red]Error:[/bold red] File does not exist"
        )
        raise typer.Exit(code=1)

    return p


def validate_directory(path: str) -> Path:
    """checks if the path is a valid directory"""
    p = validate_path(path)

    if not p.is_dir():
        console.print(
            "[bold red]Error:[/bold red] Path is not a directory"
        )
        raise typer.Exit(code=1)

    return p


def validate_file(path: str) -> Path:
    """checks if the path is a valid file"""
    p = validate_path(path)

    if not p.is_file():
        console.print(
            "[bold red]Error:[/bold red] Path is not a file"
        )
        raise typer.Exit(code=1)

    return p


def ensure_file():
    editor_path = Path.home() / ".nyx" / "notes.txt"
    editor_path.parent.mkdir(parents=True, exist_ok=True)
    editor_path.touch(exist_ok=True)

    return editor_path
