from importlib.metadata import version as get_version
import typer
from rich.console import Console

from Nyx.commands import stats, run, notes, doctor, ai, monitor, update, serve, watch, scan
from Nyx.commands.organize import organize
from pathlib import Path
import subprocess

app = typer.Typer(help="Nyx: A terminal assistant for developers.")
console = Console()


def version_callback(value: bool):
    if value:
        print(f"Nyx version {get_version('nyx')}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show Nyx version"
    )
):
    if ctx.invoked_subcommand is None:

        console.print('''
        [bold cyan]
        ███╗   ██╗██╗   ██╗██╗  ██╗
        ████╗  ██║╚██╗ ██╔╝╚██╗██╔╝
        ██╔██╗ ██║ ╚████╔╝  ╚███╔╝
        ██║╚██╗██║  ╚██╔╝   ██╔██╗
        ██║ ╚████║   ██║   ██╔╝ ██╗
        ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
        [/bold cyan]
        
        [dim]Local AI terminal assistant[/dim
        ''')


@app.command("..")
def open_nyx_home():
    """
    Opens the Nyx config/workspace folder.
    """

    nyx_home = Path.home() / ".nyx"

    nyx_home.mkdir(exist_ok=True)

    subprocess.run(["explorer", str(nyx_home)])


app.command()(organize)
# app.add_typer(organize.app, name="organize")
app.add_typer(stats.app, name="stats", help="Get file stats")
app.add_typer(run.app, name="run", help="Run a Python script")
app.add_typer(notes.app, name="notes", help="Manage your notes")
app.add_typer(doctor.app, name="doctor", help="System health check")
app.add_typer(ai.app, name="ai", help="AI-powered assistant")
app.add_typer(monitor.app, name="monitor", help="System monitor")
app.add_typer(update.app, name="update", help="Update Nyx to the latest version")
app.add_typer(serve.app, name="serve", help="Serve a directory as a static site")
app.add_typer(watch.app, name="watch", help="Watch a directory for changes")
app.add_typer(scan.app, name="scan", help="Scan a directory for sensitive information")

if __name__ == "__main__":
    app()
