import time

import psutil
import typer

from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.console import Console

from Nyx.utils.formatters import format_size

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def monitor(
        refresh: float = typer.Option(
            1.0,
            "--refresh",
            "-r",
            help="Refresh rate in seconds"
        )
):
    """
    Real-time system monitor for CPU, RAM, and Disk usage.
    """

    try:

        with Live(
                refresh_per_second=10,
                console=console,
                screen=True
        ) as live:

            while True:

                # CPU
                cpu = psutil.cpu_percent()

                # RAM
                memory = psutil.virtual_memory()

                # Disk
                disk = psutil.disk_usage("/")

                table = Table(title="System Monitor")

                table.add_column("Resource", style="cyan")
                table.add_column("Usage", style="green")

                table.add_row(
                    "CPU",
                    f"{cpu}%"
                )

                table.add_row(
                    "RAM",
                    (
                        f"{format_size(memory.used)} / "
                        f"{format_size(memory.total)} "
                        f"({memory.percent}%)"
                    )
                )

                table.add_row(
                    "Disk",
                    (
                        f"{format_size(disk.used)} / "
                        f"{format_size(disk.total)} "
                        f"({disk.percent}%)"
                    )
                )

                panel = Panel(
                    table,
                    title="Nyx",
                    border_style="blue"
                )

                live.update(panel)

                time.sleep(refresh)

    except KeyboardInterrupt:

        console.print(
            "\n[yellow]Monitor stopped.[/yellow]"
        )
