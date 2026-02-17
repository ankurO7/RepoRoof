import os
import git
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ListItem, ListView
from textual.containers import Container, Vertical
from textual.screen import Screen

class BranchRoom(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back to Building")]

    def __init__(self, branch_name):
        super().__init__()
        self.branch_name = branch_name

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="room-view"):
            yield Label(f"🏠 Inside Room: {self.branch_name}", id="room-title")
            
            # --- LOGS ---
            yield Label("📜 Latest Construction Logs:", classes="subtitle")
            try:
                repo = git.Repo(os.getcwd(), search_parent_directories=True)
                # We use a broader search for commits to ensure we see SOMETHING
                commits = list(repo.iter_commits(self.branch_name, max_count=5))
                if not commits:
                    yield Label("  (This room is brand new - no history yet)")
                else:
                    for c in commits:
                        yield Static(f"📍 {c.summary}", classes="poster")
            except Exception as e:
                yield Label(f"  Error loading logs: {e}")

            # --- FILES ---
            yield Label("🪑 Furniture (Files):", classes="subtitle")
            items = [ListItem(Label(f"📄 {f}")) for f in os.listdir('.') if not f.startswith('.')]
            yield ListView(*items)
        yield Footer()

class GitBuilding(App):
    # This allows you to exit the app from the main screen
    BINDINGS = [("q", "quit", "Quit"), ("escape", "quit", "Quit")]
    
    CSS = """
    #building-grid { layout: grid; grid-size: 3; grid-gutter: 2; padding: 4; }
    BranchWindow { height: 7; border: round $primary; content-align: center middle; background: $surface; }
    .active-branch { border: double $success; background: #064e3b; }
    .subtitle { text-style: bold; color: $accent; margin-top: 1; }
    .poster { background: $boost; border-left: solid $secondary; padding: 0 1; margin-bottom: 1; }
    #room-title { text-style: bold; color: $accent; margin-bottom: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="building-grid"):
            try:
                repo = git.Repo(os.getcwd(), search_parent_directories=True)
                for branch in repo.branches:
                    is_active = (branch == repo.active_branch)
                    klass = "active-branch" if is_active else ""
                    yield BranchWindow(branch, is_active, classes=klass)
            except Exception as e:
                yield Label(f"⚠️ Error: {e}")
        yield Footer()

class BranchWindow(Static):
    def __init__(self, branch, is_active, **kwargs):
        super().__init__(**kwargs)
        self.branch = branch

    def on_click(self) -> None:
        self.app.push_screen(BranchRoom(self.branch.name))

    def compose(self) -> ComposeResult:
        yield Label(f"🪟\n{self.branch.name}")

def main():
    app = GitBuilding()
    app.run()

if __name__ == "__main__":
    main()