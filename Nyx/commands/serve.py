import os
import webbrowser
from http.server import BaseHTTPRequestHandler
import socketserver
from pathlib import Path
import typer

from rich.console import Console

from Nyx.utils.formatters import validate_directory
app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def serve(
    path: str = typer.Argument(
        ".",
        help="Directory to serve"
    ),
    port: int = typer.Option(
        3000,
        "--port",
        "-p",
        help="Port to serve on"
    ),
    open_browser: bool = typer.Option(
        False,
        "--open",
        "-o",
        help="Open the browser after starting the server"
    )
):
    """
    Start a local HTTP server.
    """

    class NyxHandler(BaseHTTPRequestHandler):

        assets = (
                Path(__file__)
                .parent.parent
                / "assets"
        )
        address = assets / "dashboard.html"

        try:
            with open(address, "r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            html = "File not found"

        def do_GET(self, html):

            self.send_response(200)
            self.send_header(
                "Content-type",
                "text/html"
            )
            self.end_headers()

            self.wfile.write(
                html.encode()
            )

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    path = Path(path).resolve()
    path = validate_directory(path)
    os.chdir(path)

    for port in range(port, port + 10):
        try:
            with ReusableTCPServer(
                ("", port),
                NyxHandler
            ) as httpd:
                if open_browser:
                    webbrowser.open(
                        f"http://localhost:{port}"
                    )

                console.print(
                    f"[bold green]Nyx server started[/bold green]\n"
                    f"[cyan]Localhost:[/cyan] "
                    f"http://localhost:{port}\n"
                    f"[cyan]Serving:[/cyan] "
                    f"{os.getcwd()}\n\n"
                    f"[yellow]Press Ctrl+C to stop[/yellow]"
                )
                httpd.serve_forever()

        except KeyboardInterrupt:
            console.print(
                "\n[yellow]Server stopped.[/yellow]"
            )
            break
        except OSError as e:
            console.print(
                f"[red]Port {port} is already in use.[/red]"
            )
            console.print(e)
# TODO: fix Nyx serve: serve me
