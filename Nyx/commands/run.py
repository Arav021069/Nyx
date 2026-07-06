import typer
import subprocess
import shlex
from rich.console import Console


app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def script(
    ctx: typer.Context,
    file: str = typer.Argument(None, help="Path to the Python script to run")
):
    """
    Executes a specified Python script.

    Args:
        file (str): The path to the Python script to run.
        ctx (typer.Context): The context to run the script with.
    """

    if file:
        try:
            command = shlex.quote(file)
            subprocess.run([str(command)], check=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Program exited with error code {e.returncode}[/red]")
        except Exception as e:
            console.print(f"[red]An unexpected error occurred: {e}[/red]")
    elif ctx.invoked_subcommand is None:
        console.print("[red]Provide a file to run[/red]")

#
# @app.command()
# def shell(cmd: str):
#     """
#     Executes an arbitrary shell command.
#
#     Args:
#         cmd (str): The shell command to execute.
#     """
#     subprocess.run(cmd, shell=True)
#
#
# @app.command()
# def tests():
#     """
#     Runs the project's test suite using pytest.
#     """
#     subprocess.run(["pytest"])
