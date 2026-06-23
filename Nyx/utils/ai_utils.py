import ollama
import typer
from rich.console import Console
from rich.live import Live
from rich.text import Text

import subprocess
import time


console = Console()


def check_ollama():

    try:
        ollama.list()
        return True

    except ConnectionError:
        console.print(
            "[red]Error: Can't connect to Ollama server[/red]"
        )
        return False

    except Exception:

        subprocess.Popen(
            ["ollama", "serve"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    frames = [".", "..", "..."]

    with Live(
        "",
        refresh_per_second=5,
        console=console,
        transient=True
    ) as live:

        max_checks = 5
        checks = 0
        i = 0

        while checks < max_checks:

            message = (
                "Starting Ollama server"
                + frames[i % len(frames)]
            )

            live.update(
                Text(message, style="yellow")
            )

            time.sleep(0.3)

            i += 1

            if i % 5 == 0:

                try:
                    ollama.list()

                    return True

                except Exception:
                    checks += 1

    console.print(
        "[bold red]Failed to start Ollama server[/bold red]"
    )

    return False


def get_installed_models():
    return [
        m.model
        for m in ollama.list()["models"]
    ]

def validate_model(model):

    installed = get_installed_models()

    if model in installed:
        return model

    matches = [
        m for m in installed
        if m.startswith(model)
    ]
    if len(matches) == 1:
        return matches[0]

    console.print(
        f"[red]Model '{model}' not found[/red]"
    )
    if matches:
        console.print(
            "[yellow]Did you mean:[/yellow]"
        )

        for m in matches:
            console.print(f" - {m}")

    raise typer.Exit(code=1)


def get_best_model():
    llm = ollama.list()

    # PREFERRED_MODELS = [
    #     "llama3",
    #     "llama3.1",
    #     "mistral",
    #     "qwen",
    #     "gemma"
    # ]

    if not llm:
        console.print(
            "[red]No Ollama models installed[/red]"
        )
        raise typer.Exit(code=1)

    return llm["models"][0]["model"]


def complete_models(
    ctx,
    param,
    incomplete: str
):
    installed = get_installed_models()

    return [
        m
        for m in installed
        if m.startswith(incomplete)
    ]
