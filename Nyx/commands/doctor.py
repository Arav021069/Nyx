import typer
from rich.console import Console
from pathlib import Path

app = typer.Typer()
console = Console()


@app.command()
def check():
    nyx_home = Path.home() / ".nyx"

    console.print("[bold cyan]Running Nyx diagnostics...[/bold cyan]")

    if nyx_home.exists():
        console.print("[green]✓[/green] Nyx directory exists")
    else:
        console.print("[red]✗[/red] Nyx directory missing")