import ollama
import typer
from ollama import ResponseError
from rich.console import Console
from rich.table import Table
import uuid

from Nyx.utils.formatters import format_size, validate_file
from Nyx.utils.ai_utils import check_ollama, get_best_model, validate_model
from Nyx.utils.db import save_message, load_messages

app = typer.Typer()
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
        except ConnectionError:
            console.print("[red]Error: Can't connect to ollama[/red]")

    else:
        raise typer.Exit()


@app.command()
def run(
        model: str = typer.Argument(
            None,
            help="Model to use for chatting"),
        prompt: str = typer.Argument(
            None,
            help="Prompt to send to the model")
):
    """
    Command to interact with a language model by providing a prompt or engaging in an interactive session.
    If a prompt is provided, the model responds to it directly. Without a prompt, the user enters an
    interactive conversation. The active model is displayed at the start.

    Arguments:
        model (str): Model to use for chatting. Required and must be specified
        prompt (str): Prompt to send to the model. If not provided, enters interactive mode

    Raises:
        typer.Exit: Terminates the application when finished or upon user exit command in interactive mode.
    """
    session_id = str(uuid.uuid4())

    messages = load_messages(session_id)

    check_ollama()
    if not model:
        model = get_best_model()
    else:
        model = validate_model(model)

    console.print(
        f"[bold cyan]Using model:[/bold cyan] {model}"
    )
    messages.append([
        {
            "role": "system",
            "content": "You are Nyx AI assistant..."
        }
    ])

    if prompt:
        # messages.append({"role": "user", "content": prompt})

        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        for chunk in response:
            console.print(
                chunk["message"]["content"],
                end=""
            )
        raise typer.Exit()

    else:

        while True:
            user_input = input(">>> ").strip()
            if user_input == "/exit" or user_input == "/quit":
                raise typer.Exit()

            # messages.append({
            #     "role": "user",
            #     "content": user_input
            # })
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

                console.print(
                    content,
                    end=""
                )
            print()
            # messages.append({
            #     "role": "assistant",
            #     "content": assistant_response
            # })
            save_message(
                session_id,
                "assistant",
                assistant_response
            )
            messages = messages[-10:]


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

    Parameters:
        model (str): The specific model to use for summarization. If not provided,
            the best model is selected automatically
        path (str): The file path to the text file that needs to be summarized.

    Raises:
        typer.Exit: Exits with an error code if an issue occurs during the summarization
            process, such as a failed response from the model.
    """

    p = validate_file(path.strip())

    text = p.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    max_chars = 10_000
    text = text[:max_chars]

    prompt = (
        "Summarize the following text clearly:\n"
        f"{text}"
    )

    if not model:
        model = get_best_model()
    console.print(
        f"[cyan]Using model:[/cyan] {model}"
    )
    if check_ollama():
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True
            )
            for chunk in response:
                console.print(
                    chunk["message"]["content"],
                    end=""
                )
            print("\n")
        except ollama.ResponseError as e:

            console.print(
                f"[red]Error:[/red] {e}"
            )

            raise typer.Exit(code=1)


@app.command()
def pull(
        model: str = typer.Argument(
            ...,
            help="Name of the model to pull"),
):
    """
    Pull a specified model from the repository.

    Summary:
    This command attempts to pull the specified model by its name. If the repository
    is accessible and the model name is valid, it downloads the model and indicates
    successful completion. In case of an error, it provides a descriptive message
    and exits the command with a non-zero status code.

    Args:
        model (str): Name of the model to be pulled. This is a required argument.

    Raises:
        typer.BadParameter: Raised when the model name is empty or invalid
        typer.Exit: Rose with a non-zero exit code in case of an error

    Return:
        None
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
