from importlib.metadata import version as get_version
import typer
from Nyx.commands import organize, stats, run, notes
from pathlib import Path
import subprocess

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"Nyx version {get_version('nyx')}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show Nyx version"
    )
):
    pass


@app.command("..")
def open_nyx_home():
    """
    Opens the Nyx config/workspace folder.
    """

    nyx_home = Path.home() / ".nyx"

    nyx_home.mkdir(exist_ok=True)

    subprocess.run(["explorer", str(nyx_home)])


app.add_typer(organize.app, name="organize")
app.add_typer(stats.app, name="stats")
app.add_typer(run.app, name="run")
app.add_typer(notes.app, name="notes")


if __name__ == "__main__":
    app()
