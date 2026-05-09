# from pathlib import Path
import typer

from rich.console import Console
from rich.table import Table

from Nyx.utils.formatters import format_size, validate_directory

app = typer.Typer()
console = Console()


@app.command()
def files(
    path: str,
    all_items: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Include hidden files"
    ),
    detailed: bool = typer.Option(
        False,
        "--detailed",
        "-d",
        help="Show detailed file info"
    )
):
    """
    Lists contents of a directory.
    """

    p = validate_directory(path)

    table = Table(title=f"Contents of {p}")

    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")

    if detailed:
        table.add_column("Size")

    try:
        items = sorted(
            p.iterdir(),
            key=lambda x: (x.is_file(), x.name.lower())
        )

        for item in items:

            if not all_items and item.name.startswith("."):
                continue

            item_type = "Folder" if item.is_dir() else "File"

            if detailed and item.is_file():
                size = item.stat().st_size
                size_text = f"{format_size(size)}"

                table.add_row(
                    item.name,
                    item_type,
                    size_text
                )

            else:
                table.add_row(
                    item.name,
                    item_type,
                    # "-"
                )

    except PermissionError:
        console.print(
            "[bold yellow]Permission denied[/bold yellow]"
        )
        raise typer.Exit()

    console.print(table)
