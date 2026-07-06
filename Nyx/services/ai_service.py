from pathlib import Path

from Nyx.services.scanner_service import scan_todos, scan_secrets, scan_bloat

def gather_project_anomalies(path: Path) -> str:
    """
    Gathers all anomalies from the project and formats them
    into a clean, professional report for the AI to analyze.
    """
    # 1. Gather raw data from the scanner service
    todos = scan_todos(path)
    secrets = scan_secrets(path)
    bloat = scan_bloat(path)

    # We use a list to collect our report sections
    report = ["PROJECT AUDIT REPORT\n"]

    # --- Section 1: Technical Debt ---
    report.append("--- Technical Debt ---")
    if todos:
        for t in todos:
            # Format: - file.py (Line 10) [TODO]: The text
            report.append(f"- {t['file']} (Line {t['line']}) [{t['type']}]: {t['text']}")
    else:
        report.append("No technical debt found.")
    report.append("")  # Add a newline for spacing

    # --- Section 2: Security Risks ---
    report.append("--- Security Risks ---")
    if secrets:
        for s in secrets:
            # Format: - file.py [POTENTIAL SECRET]: Found secret pattern
            report.append(f"- {s['file']} [{s['type']}]: {s['text']}")
    else:
        report.append("No security risks detected.")
    report.append("")

    # --- Section 3: File Bloat ---
    report.append("--- File Bloat ---")
    if bloat:
        for b in bloat:
            # Format: - file.bin: 45.20 MB
            report.append(f"- {b['file']}: {b['text']}")
    else:
        report.append("No oversized files found.")

    # Join all the list items with a newline character
    return "\n".join(report)
