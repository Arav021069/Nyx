import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from Nyx.services.scanner_service import scan_todos, scan_secrets, scan_bloat

app = typer.Typer(help="Project Auditor: Scans for technical debt, secrets, and bloat.")
console = Console()


# def scan_todos(root_path: Path):
#     """Finds TODO, FIXME, and HACK comments."""
#     results = []
#     for path in root_path.rglob("*"):
#         if path.is_file() and not is_ignored(path) and path.suffix in {'.py', '.md', '.txt', '.js', '.ts'}:
#             try:
#                 with open(path, 'r', encoding='utf-8', errors='ignore') as f:
#                     for i, line in enumerate(f, 1):
#                         match = re.search(r"(TODO|FIXME|HACK):", line, re.IGNORECASE)
#                         if match:
#                             results.append({"file": path.relative_to(root_path), "line": i,
#                                             "type": match.group(1).upper(), "text": line.strip()})
#             except Exception:
#                 continue
#     return results


# def scan_secrets(root_path: Path):
#     """Scans for exposed secrets in filenames or content."""
#     results = []
#     for path in root_path.rglob("*"):
#         if is_ignored(path):
#             continue
#
#         if path.name in SECRET_FILES:
#             results.append({"file": path.relative_to(root_path),
#                             "type": "SENSITIVE FILE", "text": f"Found {path.name}"})
#             continue
#
#         if path.is_file() and path.suffix in {'.py', '.txt', '.env', '.json', '.yaml', '.yml'}:
#             try:
#                 with open(path, 'r', encoding='utf-8', errors='ignore') as f:
#                     content = f.read()
#                     for pattern in SECRET_PATTERNS:
#                         if re.search(pattern, content):
#                             results.append({"file": path.relative_to(root_path), "type": "POTENTIAL SECRET",
#                                             "text": "Pattern match found in content"})
#                             break
#                     if re.search(RSA, content):
#                         results.append({"file": path.relative_to(root_path), "type": "PRIVATE KEY",
#                                         "text": "Potential RSA private key"})
#             except Exception:
#                 continue
#
#     return results


# def scan_bloat(root_path: Path):
#     """Finds files larger than the threshold."""
#     results = []
#     for path in root_path.rglob("*"):
#         if path.is_file() and not is_ignored(path):
#             size_mb = path.stat().st_size / (1024 * 1024)
#             if size_mb > BLOAT_THRESHOLD_MB:
#                 results.append({"file": path.relative_to(root_path), "type": "BLOAT", "text": format_size(size_mb)})
#     return results


@app.callback(invoke_without_command=True)
def main(
        path: Path = typer.Argument(
            ".",
            help="The directory to scan"
        ),
        full: bool = typer.Option(
            False,
            "--full",
            "-f",
            help="Show full paths in the output"
        )
):
    """
    Analyzes the project for technical debt, potential security leaks, and file bloat.
    """
    rprint(Panel.fit("[bold magenta]NYX Project Auditor[/bold magenta]\n[dim]"
                     "Scanning the void for anomalies...[/dim]", border_style="magenta"))
    
    # TODOs
    todos = scan_todos(path)
    if todos:
        table = Table(title="📝 Technical Debt (TODOs)", border_style="blue", header_style="bold cyan")
        table.add_column("File", style="dim")
        table.add_column("Line", justify="right")
        table.add_column("Type", style="bold yellow")
        table.add_column("Content")
        for t in todos:
            display_path = str(t['file']) if not full else f"{(path / t['file']).resolve()}"
            table.add_row(display_path, str(t["line"]), t["type"], t["text"])
        console.print(table)
    else:
        rprint("[green]✓ No pending TODOs found.[/green]")

    # Secrets
    secrets = scan_secrets(path)
    if secrets:
        table = Table(title="⚠️ Security Alerts", border_style="red", header_style="bold red")
        table.add_column("File")
        table.add_column("Type")
        table.add_column("Details")
        for s in secrets:
            display_path = str(s['file']) if not full else f"{(path / s['file']).resolve()}"
            table.add_row(display_path, s["type"], s["text"])
        console.print(table)
    else:
        rprint("[green]✓ No obvious secrets leaked.[/green]")

    # Bloat
    bloat = scan_bloat(path)
    if bloat:
        table = Table(title="🐘 File Bloat", border_style="yellow", header_style="bold yellow")
        table.add_column("File")
        table.add_column("Size", justify="right")
        for b in bloat:
            display_path = str(b['file']) if not full else f"{(path / b['file']).resolve()}"
            table.add_row(display_path, b["text"])
        console.print(table)
    else:
        rprint("[green]✓ No oversized files detected.[/green]")


if __name__ == "__main__":
    app()
