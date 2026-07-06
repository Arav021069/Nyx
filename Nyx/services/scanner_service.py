import re
from pathlib import Path

from Nyx.utils.formatters import format_size

# Configuration
BLOAT_THRESHOLD_MB = 10
SECRET_PATTERNS = [
    r"(?i)api_key\s*=\s*['\"].*['\"]",
    r"(?i)secret\s*=\s*['\"].*['\"]",
    r"(?i)password\s*=\s*['\"].*['\"]",
]
SECRET_FILES = {"secrets.json", "key.pem", "id_rsa"}
IGNORE_DIRS = {".git", "venv", "__pycache__", ".idea", ".vscode", "node_modules", ".venv"}

RSA = r"-----BEGIN RSA PRIVATE KEY-----['\"]"


def is_ignored(path: Path):
    return any(part in IGNORE_DIRS for part in path.parts)


def scan_todos(root_path: Path):
    """Finds TODO, FIXME, and HACK comments."""
    results = []
    for path in root_path.rglob("*"):
        if path.is_file() and not is_ignored(path) and path.suffix in {'.py', '.md', '.txt', '.js', '.ts'}:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        match = re.search(r"(TODO|FIXME|HACK):", line, re.IGNORECASE)
                        if match:
                            results.append({"file": path.relative_to(root_path), "line": i,
                                            "type": match.group(1).upper(), "text": line.strip()})
            except Exception:
                continue
    return results


def scan_secrets(root_path: Path):
    """Scans for exposed secrets in filenames or content."""
    results = []
    for path in root_path.rglob("*"):
        if is_ignored(path):
            continue

        if path.name in SECRET_FILES:
            results.append({"file": path.relative_to(root_path),
                            "type": "SENSITIVE FILE", "text": f"Found {path.name}"})
            continue

        if path.is_file() and path.suffix in {'.py', '.txt', '.env', '.json', '.yaml', '.yml'}:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern in SECRET_PATTERNS:
                        if re.search(pattern, content):
                            results.append({"file": path.relative_to(root_path), "type": "POTENTIAL SECRET",
                                            "text": "Pattern match found in content"})
                            break
                    if re.search(RSA, content):
                        results.append({"file": path.relative_to(root_path), "type": "PRIVATE KEY",
                                        "text": "Potential RSA private key"})
            except Exception:
                continue

    return results


def scan_bloat(root_path: Path):
    """Finds files larger than the threshold."""
    results = []
    for path in root_path.rglob("*"):
        if path.is_file() and not is_ignored(path):
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > BLOAT_THRESHOLD_MB:
                results.append({"file": path.relative_to(root_path), "type": "BLOAT", "text": format_size(size_mb)})
    return results
