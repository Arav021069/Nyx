# from pathlib import Path
import typer
from typing import Literal
import shutil

from rich.console import Console

from Nyx.utils.formatters import validate_directory

# app = typer.Typer()
console = Console()


# @app.command()
def organize(
    path: str = typer.Argument(None, help="Path to the directory to organize"),
    sort_by: Literal["extension", "size", "date"] = typer.Option(
        "extension",
        "--by",
        help="Organization strategy"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without moving files"
    ),
):
    """
    Organizes files in a directory based on the specified criteria.
    """

    if not path:
        console.print(
            "[red]Provide a directory to organize[/red]"
        )
        raise typer.Exit()

    p = validate_directory(path)

    items = list(p.iterdir())

    if sort_by == "extension":
        all_ext = set()

        for item in items:
            if item.is_file():
                ext = item.suffix.lower()
                all_ext.add(ext[1:])
                if not ext:
                    ext = "Other"
                    all_ext.add(ext)

        for ext in sorted(all_ext):
            target = p / ext
            for item in items:
                if item.is_file():
                    if item.suffix.lower() == f".{ext}":
                        if dry_run:
                            console.print(f"[yellow]Would move[/yellow] {item.name} to {target}")
                        else:
                            target.mkdir(exist_ok=True)

                            target_path = target / item.name
                            shutil.move(str(item), str(target_path))
