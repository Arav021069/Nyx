import ollama
import typer
from ollama import ResponseError
from rich.console import Console
from rich.table import Table
import uuid
from pathlib import Path

from Nyx.utils.formatters import format_size, validate_file
from Nyx.utils.ai_utils import check_ollama, get_best_model, validate_model, complete_models, _stream_ai_response
from Nyx.utils.db import save_message, load_messages
from Nyx.services.ai_service import gather_project_anomalies

app = typer.Typer(help="Interact with a language model")
console = Console()


@app.command()
def models():
    """
    Provides a command that lists available models using the ollama library.
    """
    if check_ollama():

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

            console.print(table)
        except ConnectionError as e:
            console.print(f"[red]Error: {e}[/red]")

    else:
        raise typer.Exit()


@app.command()
def run(
        model: str = typer.Argument(
            None,
            shell_complete=complete_models,
            help="Model to use for chatting"),
        prompt: str = typer.Argument(
            None,
            help="Prompt to send to the model")
):
    """
    Command to interact with a language model by providing a prompt or engaging in an interactive session.
    """
    session_id = str(uuid.uuid4())

    messages = load_messages(session_id)

    if check_ollama():
        if not model:
            model = get_best_model()
        else:
            model = validate_model(model)

        console.print(
            f"[bold cyan]Using model:[/bold cyan] {model}"
        )
        messages.append(
            {
                "role": "system",
                "content": "You are Nyx, a helpful local terminal AI assistant."
            }
        )

        if prompt:
            messages.append({"role": "user", "content": prompt})
            _stream_ai_response(model, messages)
            raise typer.Exit(code=1)

        else:

            while True:
                console.print("[green]>>> [/green]", end="")
                user_input = input("").strip()
                if user_input == "/exit" or user_input == "/quit":
                    raise typer.Exit()

                messages.append({
                    "role": "user",
                    "content": user_input
                })
                save_message(
                    session_id,
                    "user",
                    user_input
                )

                response = ollama.chat(
                    model=model,
                    messages=messages,
                    stream=True
                )
                assistant_response = ""
                for chunk in response:
                    content = chunk["message"]["content"]
                    assistant_response += content
                    console.print(content, end="")
                print()
                messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                save_message(
                    session_id,
                    "assistant",
                    assistant_response
                )
                if len(messages) > 10:
                    messages = [messages[0]] + messages[-9:]


@app.command()
def summarize(
        model: str = typer.Option(
            None,
            "--model",
            "-m",
            help="Model to use for summarization"),
        path: str = typer.Argument(
            ...,
            help="Path to the file to summarize")
):
    """
    Summarizes the content of a text file using a specified or default summarization model.
    """

    p = validate_file(path.strip())
    text = p.read_text(encoding="utf-8", errors="ignore")
    max_chars = 10_000
    text = text[:max_chars]

    prompt = (
        "Summarize the following text clearly:\n"
        f"{text}"
    )

    if not model:
        model = get_best_model()
    else:
        model = validate_model(model)

    console.print(f"[cyan]Using model:[/cyan] {model}")
    if check_ollama():
        _stream_ai_response(model, [{"role": "user", "content": prompt}])


@app.command()
def pull(
        model: str = typer.Argument(
            ...,
            help="Name of the model to pull"),
):
    """
    Pull a specified model from the repository.
    """
    if check_ollama():
        try:
            model = model.strip()
            if not model:
                raise typer.BadParameter("Model name is required")
            ollama.pull(model)
            console.print(f"[green]{model} successfully downloaded.[/green]")

        except ResponseError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(code=1)


@app.command()
def scan(
        model: str = typer.Option(
            None,
            "--model",
            "-m",
            help="Model to use for auditing"),
        path: str = typer.Argument(
            ...,
            help="Path to the project to scan")
):
    """
    AI-powered project audit. Scans for technical debt, secrets, and bloat,
    then uses a language model to provide a professional fix plan.
    """
    # 1. Validate directory
    # We use validate_file logic but check for directory
    p = Path(path.strip()).resolve()
    if not p.exists() or not p.is_dir():
        console.print("[bold red]Error:[/bold red] Valid project directory is required.")
        raise typer.Exit(code=1)

    # 2. Gather report
    anomaly_report = gather_project_anomalies(p)

    # 3. Resolve Model
    if not model:
        model = get_best_model()
    else:
        model = validate_model(model)

    # 4. Setup Professional Audit Prompt
    messages = [
        {
            "role": "system", 
            "content": "You are a Senior Project Auditor. Analyze the following project anomalies and provide a concise, actionable fix plan. Focus on security first, then technical debt, then bloat."
        },
        {
            "role": "user", 
            "content": f"PROJECT AUDIT REPORT:\n{anomaly_report}"
        }
    ]

    console.print(f"[bold magenta]NYX AI Auditor is analyzing {p.name}...[/bold magenta]\n")
    if check_ollama():
        _stream_ai_response(model, messages)


if __name__ == "__main__":
    app()
