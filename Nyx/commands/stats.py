import typer
from pathlib import Path
from rich.table import Table
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def folder(
        path: str,
        all_items: bool = typer.Option(
            False,
            "--all",
            "-a",
            help="Include folders in output"
        ),
        size_only: bool = typer.Option(
            False,
            "--size",
            "-s",
            help="Show only total size info"
        )
):  #TODO: Add option to show only file types
    """
    Displays detailed statistics for a folder, including total file count,
    total size in MB, and a breakdown of occurrences by file extension.

    Args:
        all_items:
        size_only:
        path (str): The directory path to analyze.
    """
    p = Path(path)

    total_files = 0
    total_size = 0
    file_types = {}

    for file in p.rglob("*"):
        if file.is_file():
            total_files += 1
            size = file.stat().st_size
            total_size += size

            ext = file.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        if all_items and file.is_dir():
            print(f"Folder: {file.name}")

    console.print(f"[bold cyan]Total files:[/bold cyan] {total_files}")
    print(f"Total size: {total_size / (1024 * 1024):.2f} MB")

    # print("\nFile types:")
    # for ext, count in file_types.items():
    #     print(f"{ext or 'no_ext'}: {count}")
    table = Table(title="File Types")
    table.add_column("Extension")
    table.add_column("Count")

    for ext, count in file_types.items():
        table.add_row(ext or "no_ext", str(count))

    console.print(table)


@app.command()
def size(path: str):
    """
    Calculates and displays the total number of items and the total size
    of a directory in MB.

    Args:
        path (str): The directory path to analyze.
    """
    p = Path(path)

    total_files = 0
    total_size = 0

    for file in p.rglob("*"):
        total_files += 1
        size = file.stat().st_size
        total_size += size

    print(f"Total files: {total_files}")
    print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
