import typer
import requests
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from packaging import version
from importlib.metadata import version as get_version

from rich.console import Console

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def check_for_updates():
    try:
        current_version = get_version("nyx")
    except Exception:
        # Fallback if package is not installed via pip
        current_version = "0.0.0"

    url = "https://raw.githubusercontent.com/Arav021069/Nyx/main/pyproject.toml"

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse TOML content
        pyproject_data = tomllib.loads(response.text)
        remote_version = pyproject_data.get("project", {}).get("version")

        if not remote_version:
            console.print("[yellow]Warning: Could not find version in remote pyproject.toml[/yellow]")
            return None

        if version.parse(remote_version) > version.parse(current_version):
            console.print(f"New version available: [bold green]{remote_version}[/bold green]")
            console.print(f"Current version: {current_version}")
            console.print("Run 'pip install --upgrade nyx' to update.")
            return remote_version

        console.print(f"You are using the latest version: [bold cyan]{current_version}[/bold cyan]")
    except requests.RequestException as e:
        console.print(f"[red]Failed to check for updates: {e}[/red]")
        return None
    except tomllib.TOMLDecodeError:
        console.print("[red]Failed to parse remote pyproject.toml[/red]")
        return None
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        return None
