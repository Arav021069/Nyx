<div align="center">
<pre>
```
███╗   ██╗██╗   ██╗██╗  ██╗
████╗  ██║╚██╗ ██╔╝╚██╗██╔╝
██╔██╗ ██║ ╚████╔╝  ╚███╔╝ 
██║╚██╗██║  ╚██╔╝   ██╔██╗ 
██║ ╚████║   ██║   ██╔╝ ██╗
╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
```
</pre>
### **Neoteric Yield eXecution**

*The minimalist command-line nexus for productivity and system intelligence.*

<br/>

![Status](https://img.shields.io/badge/status-ACTIVE%20DEVELOPMENT-blueviolet?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-black?style=for-the-badge)
![Stack](https://img.shields.io/badge/stack-Python%20%2B%20Typer%20%2B%20Rich-indigo?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-6A0DAD?style=for-the-badge)

<br/>

> *"In the silence of the void, efficiency thrives."*

<br/>

---

</div>

## 𝕎𝕙𝕒𝕥 𝕚𝕤 ℕ𝕐𝕏?

**NYX** is a lightweight, high-performance command-line interface designed to streamline your development workflow. Built with the speed of Python and the beauty of the `Rich` library, NYX provides a unified set of tools for note-taking, file organization, system statistics, and script execution.

Inspired by the primordial goddess of the night, NYX operates in the shadows of your terminal, providing powerful capabilities without the bloat of traditional GUI applications. It is designed for developers who value keyboard-centric workflows and terminal-based productivity.

---

## ✦ Features That Pierce the Dark

### 📝 Persistent Note-Taking
A built-in note management system that lives in your home directory. Add thoughts, search through history, and edit your notes directly in your favorite editor.
- `nyx notes add "New idea"`
- `nyx notes search "bugfix"`
- `nyx notes edit`

### 🤖 Neural Engine (AI)
Integrated local model inference using Ollama. Chat with models, summarize documents, and manage your local library of LLMs.
- `nyx ai run "llama3"` (Interactive chat)
- `nyx ai summarize "README.md"`
- `nyx ai pull "mistral"`
- `nyx ai models`

### 📊 System & Folder Intelligence
Get deep insights into your file system and hardware. NYX analyzes directory structures, calculates sizes, and monitors system resources in real-time.
- `nyx stats folder .`
- `nyx stats size ./data`
- `nyx monitor` (Real-time CPU/RAM/Disk)

### 📂 Intelligent Organization
Quickly navigate, audit, and clean up your project structures. NYX identifies directories and files and can automatically organize them by extension.
- `nyx organize .`
- `nyx organize . --dry-run`

### ⚡ Rapid Script Execution
Execute Python scripts with zero friction. NYX handles the execution environment and provides clean error reporting through its internal runner.
- `nyx run script.py`

### 🌐 Local Web Server
Instantly serve any directory over HTTP for testing or sharing.
- `nyx serve`
- `nyx serve --port 8080 --open`

### 👁️ File & Directory Watching
Monitor any directory or specific file for modifications in real-time.
- `nyx watch .`
- `nyx watch path/to/file.txt`

### 🩺 System Diagnostics & Updates
Keep your environment healthy and stay up to date with the latest features.
- `nyx doctor` (Check system health)
- `nyx update` (Check for new versions)

### 🏠 Home Integration
One command to open your Nyx configuration and workspace folder.
- `nyx ..`

---

## ✦ The Aesthetic

NYX is designed for the terminal enthusiast who appreciates a dark, cosmic aesthetic.

```
Theme:        Neo-Minimalism × Void Violet × Cosmic Shadows
Primary:      #1A1A2E — deep space black
Accent:       #6A0DAD → #A020F0 — dark violet to neon purple
Output:       Rich-enhanced tables, panels, and syntax highlighting
Typography:   JetBrains Mono / Fira Code (recommended)
```

---

## ✦ Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| CLI Framework | Typer |
| Formatting | Rich |
| File System | Pathlib |
| Metadata | importlib.metadata |
| Monitoring | psutil |
| File Watching | watchdog |

---

## ✦ Roadmap

```
Phase 1 — Core CLI & Toolset                     [ RELEASED ]
Phase 2 — AI Integration (Ollama)                [ RELEASED ]
Phase 3 — System Monitoring Dashboard            [ RELEASED ]
Phase 4 — Advanced File Automation & Sorting     [ IN PROGRESS ]
Phase 5 — Plugin & Extension API                 [ COMING SOON ]
```

**On the horizon:**

- 🧹 **Auto-Organize:** Advanced rule-based file sorting and cleanup.
- 📉 **Telemetry:** Historical resource usage graphs in the terminal.
- 🕸️ **Nyx Web:** A minimal web interface to sync notes across devices.
- 🔌 **Extensions:** A simple API to build your own Nyx commands.

---

## ✦ Why NYX?

| The Old Way | The NYX Way |
|---|---|
| Scattered `.txt` files everywhere | Centralized, searchable note system |
| Manual `du -sh` and complex grep | Beautiful, formatted folder statistics |
| Opening Explorer to find config files | Instant access with `nyx ..` |
| Bloated task managers | Lightweight, terminal-native utilities |

---

## ✦ Getting Started

```bash
# Install Nyx locally
pip install -e .

# Check version
nyx --version

# Add your first note
nyx notes add "Nyx is successfully installed."
```

---

## ✦ License

MIT — Licensed under the stars.

---

<div align="center">

<br/>

```
「 Command the night. Execute with precision. 」
```

<br/>

**NYX is watching.**

*Embrace the void. Streamline the workflow.*

<br/>

---

*Built for speed. Styled for the dark.*

</div>
