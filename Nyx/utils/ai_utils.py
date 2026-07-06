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

    except ConnectionError as e:
        console.print(
            f"[red]Error: {e}[/red]"
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


def get_model_names():
    return [
        m.model
        for m in ollama.list()["models"]
    ]


def validate_model(model):

    installed = get_model_names()

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
    models_installed = [m.model for m in llm["models"]]

    if not models_installed:
        console.print(
            "[red]No Ollama models installed[/red]"
        )
        console.print("run `nyx ai pull [MODEL NAME]` to install models")
        raise typer.Exit(code=1)

    PREFERRED_MODELS = [
        "llama3.1", 
        "llama3", 
        "mistral", 
        "qwen2.5", 
        "gemma2", 
        "phi3"
    ]

    for preferred in PREFERRED_MODELS:
        for installed in models_installed:
            if installed.startswith(preferred):
                return installed

    return models_installed[0]


def complete_models(
    ctx,
    param,
    incomplete: str
):
    installed = get_model_names()

    return [
        m
        for m in installed
        if m.startswith(incomplete)
    ]


def _stream_ai_response(model: str, messages: list):
    """Helper to handle the streaming response from Ollama."""
    try:
        response = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        for chunk in response:
            console.print(
                chunk["message"]["content"],
                end=""
            )
        print("\n")
    except ollama.ResponseError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
