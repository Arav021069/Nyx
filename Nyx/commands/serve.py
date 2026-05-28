import os
import webbrowser
import http.server
import socketserver

import typer

from rich.console import Console

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def serve(
    port: int = typer.Option(
        3000,
        "--port",
        "-p",
        help="Port to serve on"
    ),
    open: bool = typer.Option(
        False,
        "--open",
        "-o",
        help="Open the browser after starting the server"
    )
):
    """
    Start a local HTTP server.
    """

    handler = http.server.SimpleHTTPRequestHandler

    try:

        with socketserver.TCPServer(
            ("", port),
            handler
        ) as httpd:
            if open:
                webbrowser.open(
                    f"http://localhost:{port}"
                )

            # console.print(
            #     f"[green]Serving[/green] "
            #     f"{os.getcwd()} "
            #     f"at http://localhost:{port}"
            # )
            console.print(
                f"[bold green]Nyx server started[/bold green]\n"
                f"[cyan]Localhost:[/cyan] "
                f"http://localhost:{port}\n"
                f"[cyan]Serving:[/cyan] "
                f"{os.getcwd()}\n\n"
                f"[yellow]Press Ctrl+C to stop the server[/yellow]"
            )

            httpd.serve_forever()

    except KeyboardInterrupt:

        console.print(
            "\n[yellow]Server stopped.[/yellow]"
        )

    except OSError:

        console.print(
            f"[red]Port {port} is already in use.[/red]"
        )
