# 🏠 RepoRoof
**A Structural TUI for Git Visualization**

**RepoRoof** is an interactive Terminal User Interface (TUI) that reimagines a Git repository as a physical architectural structure. By mapping abstract version control concepts (branches, HEAD, commits) to tangible elements (windows, rooms, posters), RepoRoof makes project orientation intuitive—even for developers "dumb enough to contribute" to open source.

---

## 🏗️ The Metaphor
The core of RepoRoof is its physical-to-technical mapping:

* **The Foundation:** Your `.git` directory and initial commit.
* **Windows:** Git Branches. Parallel realities of the building visible from the outside.
* **The Glow:** The active `HEAD` branch. The window that is "lit up" shows where you are.
* **Rooms:** The file state. Entering a window reveals the "furniture" (source code) of that branch.
* **Posters:** Commit logs. Visual history of the construction changes made in that specific room.

---

## 🚀 Features
* **Automatic Blueprinting:** Crawls your local `.git` to dynamically generate a grid of branch "windows."
* **Interactive Exploration:** Navigate your repo using arrow keys or a mouse. Click a window to "step inside" and view branch-specific files.
* **Construction Logs:** View the last 5 commits for any branch displayed as posters on the room walls.
* **CLI Integration:** Fully packaged as a command-line tool for use in any repository.

---

## 🛠️ Tech Stack
* **Language:** Python 3.8+
* **UI Framework:** [Textual](https://textual.textualize.io/) (Reactive TUI framework)
* **Data Engine:** [GitPython](https://gitpython.readthedocs.io/) (Direct Git API integration)

---

## 📥 Installation

### 1. Global CLI Install (Recommended)
To use `repo-roof` as a global command in any project:
```bash
git clone [https://github.com/yourusername/repo-roof.git](https://github.com/yourusername/repo-roof.git)
cd repo-roof
pip install .
```

### 2. Local Development
```bash
#Install dependencies
pip install textual gitpython

# Run the architect
python building.py
```

## Controls

Key             -> Action
Enter / Click   -> Enter the selected Branch (Room)
Esc             -> Back to Building / Quit App
Q               -> Quick Quit
Arrows          -> Navigate windows

## Usage
Once installed via ```pip install .``` , you can run the tool in any Git repository on your system:

```bash
cd path/to/any/repo
repo-roof
```

## Upcoming features:
- [] Demolition tool : Press ```D``` to safely delete merged branches.
- [] Blueprint Zoom : A bird's-eye view of the branch merge history.
- [] Live Construction: Real-time updates as files are modified in the background.

## Contributing
This project is open to contribute, feel free to open a PR!