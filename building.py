import os
import git
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ListItem, ListView
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen

# Branch Content View

class BranchRoom(Screen):
    BINDINGS = [("escape", "back_to_building", "Exit Room")]

    def __init__(self, branch_name):
        super().__init__()
        self.branch_name = branch_name

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="room-view"):
            yield Label(f"🏠 Inside Room: {self.branch_name}", id="room-title")
            
            # --- SECTION 1: COMMIT POSTERS ---
            yield Label("📜 Latest Construction Logs (Commits):", classes="subtitle")
            repo = git.Repo(os.getcwd(), search_parent_directories=True)
            
            # Fetch last 5 commits for THIS branch
            try:
                commits = list(repo.iter_commits(self.branch_name, max_count=5))
                commit_gallery = Vertical(id="commit-gallery")
                for c in commits:
                    # Creating a 'Poster' for each commit
                    date_str = c.committed_datetime.strftime('%Y-%m-%d')
                    commit_gallery.mount(Static(f"📍 {c.summary} ({date_str})", classes="poster"))
                yield commit_gallery
            except Exception:
                yield Label("No logs found for this room.")

            # --- SECTION 2: FURNITURE ---
            yield Label("🪑 Furniture (Files):", classes="subtitle")
            items = [ListItem(Label(f"📄 {file}")) for file in os.listdir('.') if not file.startswith('.')]
            yield ListView(*items)
            
        yield Footer()

    def action_back_to_building(self) -> None:
        self.app.pop_screen()

# Branch Component (Window) ---

class BranchWindow(Static):
    
    def __init__(self, branch, is_active, **kwargs):
        super().__init__(**kwargs)
        self.branch = branch
        self.is_active = is_active

    def on_click(self) -> None:

        # "Enter" the room when clicked.
        self.app.push_screen(BranchRoom(self.branch.name))

    def compose(self) -> ComposeResult:
        icon = "🌟" if self.is_active else "🪟"
        yield Label(f"{icon}\n{self.branch.name}")


# Building --- Main App

class GitBuilding(App):
    CSS = """
    #building-grid {
        layout: grid;
        grid-size: 3;
        grid-gutter: 2;
        padding: 4;
    }
    BranchWindow {
        height: 7;
        border: round $primary;
        content-align: center middle;
        background: $surface;
        color: $text;
    }
    BranchWindow:hover {
        border: double $accent;
        background: $boost;
    }
    .active-branch {
        border: double $success;
        background: #064e3b;
    }
    #room-view {
        padding: 2;
        border: heavy $accent;
        margin: 2;
    }
    .subtitle {
    text-style: bold;
    color: $accent;
    margin-top: 1;
    }

    .poster {
        background: $boost;
        color: $secondary;
        border: left $secondary;
        padding: 0 1;
        margin-bottom: 1;
    }

    #commit-gallery {
        height: auto;
        margin-bottom: 1;
        border: dashed $secondary;
        padding: 1;
    }
    #room-title { text-style: bold italic ; color: $accent; margin-bottom: 1; width: 100%; content-align: center middle; }
    #exit-hint { text-align: center; color: $text-muted; }
    """

    def compose(self)-> ComposeResult:
        yield Header()
        with Container(id="building-grid"):
            try:
                repo = git.Repo(os.getcwd())
                for branch in  repo.branches:
                    is_current = (branch == repo.active_branch)
                    klass = "active-branch" if is_current else ""
                    yield BranchWindow(branch, is_current, classes=klass)
            except Exception as e:
                yield Label(f"Error: {e}\nEnsure 'seeMe' is a git init'd folder.")
        yield Footer()

    def on_mount(self)-> None:
        self.title = "Git Skyscraper v1.0"

if __name__ == "__main__":
    app = GitBuilding()
    app.run()