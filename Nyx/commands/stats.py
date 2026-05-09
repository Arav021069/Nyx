import typer
from pathlib import Path
from rich.table import Table
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from Nyx.utils.formatters import format_size, validate_directory

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
):
    """
    Displays detailed statistics for a folder, including total file count,
    total size in MB, and a breakdown of occurrences by file extension.

    Args:
        all_items:
        size_only:
        path (str): The directory path to analyze.
    """
    p = validate_directory(path)

    total_files = 0
    total_size = 0
    file_types = {}

    with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Scanning files..."),
            console=console,
            transient=True
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)

        for file in p.rglob("*"):
            try:
                if file.is_file():
                    total_files += 1
                    stat = file.stat()
                    size = stat.st_size
                    total_size += size

            except PermissionError:
                console.print(
                    f"[yellow]Skipped:[/yellow] {file}"
                )

        ext = file.suffix.lower()
        if not ext or len(ext) > 10:
            ext = "unknown"
        file_types[ext] = file_types.get(ext, 0) + 1

        if all_items and file.is_dir():
            console.print(f"[yellow]Folder:[/yellow] {file.name}")

    # print("\nFile types:")
    # for ext, count in file_types.items():
    #     print(f"{ext or 'no_ext'}: {count}")
    table = Table(title="File Types")
    table.add_column("Extension")
    table.add_column("Count")

    for ext, count in file_types.items():
        table.add_row(ext or "no_ext", str(count))

    console.print(table)

    if size_only:
        console.print(f"[bold cyan]Total files:[/bold cyan] {total_files}")
        console.print(
            f"[bold cyan]Total size:[/bold cyan] "
            f"{total_size / (1024 * 1024):.2f} MB"
        )
        # raise typer.Exit()


@app.command()
def size(path: str):
    """
    Calculates and displays the total number of items and the total size
    of a directory in MB.

    Args:
        path (str): The directory path to analyze.
    """
    p = validate_directory(path)

    total_files = 0
    total_size = 0

    for file in p.rglob("*"):
        total_files += 1
        size = file.stat().st_size
        total_size += size

    print(f"Total files: {total_files}")
    print(f"Total size: {format_size(total_size)}")
