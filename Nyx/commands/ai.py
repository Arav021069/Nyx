import ollama
import typer
from rich.console import Console
from rich.table import Table

from Nyx.utils.formatters import format_size

app = typer.Typer()
console = Console()


@app.command()
def models():
    """
    Provides a command that lists available models using the ollama library.
    """
    try:
        llm = ollama.list()
        table = Table(title="Available Models")
        table.add_column("S no.")
        table.add_column("Model")
        table.add_column("Size")
        table.add_column("Params")
        for i, model in enumerate(llm["models"], start=1):
            table.add_row(
                str(i),
                model.model,
                format_size(model.size),
                model.details.parameter_size or "-"
            )
            # print(model)
        console.print(table)
    except ConnectionError:
        console.print("[red]Error: Can't connect to ollama[/red]")
