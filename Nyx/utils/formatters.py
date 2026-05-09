from pathlib import Path
import typer
from rich.console import Console

console = Console()


def format_size(size_bytes: int) -> str:
    """
    Converts bytes into a human-readable format.
    """

    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


# TODO: Add validation for file and directory in commands
def validate_directory(path: str) -> Path:
    p = Path(path)

    if not p.exists():
        console.print(
            "[bold red]Error:[/bold red] Path does not exist"
        )
        raise typer.Exit()

    if not p.is_dir():
        console.print(
            "[bold red]Error:[/bold red] Path is not a directory"
        )
        raise typer.Exit()

    return p
