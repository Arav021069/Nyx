import typer
from rich.console import Console
from pathlib import Path

from Nyx.utils.ai_utils import check_ollama

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def check():
    nyx_home = Path.home() / ".nyx"

    console.print("[bold cyan]Running Nyx diagnostics...[/bold cyan]")

    if nyx_home.exists():
        console.print("[green]✓[/green] Nyx directory exists")
    else:
        console.print("[red]✗[/red] Nyx directory missing")

    if check_ollama():
        console.print("[green]✓[/green] Ollama is running.")
