import os
import git
from textual.app import App, ComposeResult
import textual.widgets import Header, Footer, Static, Label, ListItem, ListView
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen

# Branch Content View

class BranchRoom(Screen):

    # Inside of a branch window
    def __init__(self, branch_name):
        super().__init__()
        self.branch_name = branch_name

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="room-view"):
            yield Label(f" Inside Room :  {self.branch_name}", id="room-title")
            yield Label("Furniture (Files in this branch): ",classes = "subtitle")

            #List files in the current directory as 'Furniture'

            file_list = ListView()
            
            for file in os.listdir('.'):
                if not file.startswith('.'):
                    file_list.append(ListItem(Label(f" {file}")))
            yield file_list
        
        yield Label("Press 'ESC' to exit the room", id = "exit-hint")
        yield Footer()


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
    #room-title { font-size: 150%; color: $accent; margin-bottom: 1; }
    #exit-hint { text-align: center; color: $text-muted; }
    """

    def compose(self)-> ComposeResult:
        yield Header()
        with Container(id="building-grid"):
            try:
                repo = git.Repo(os.getcwd())
                for branch in  repo.branches:
                    is_current = (branch == repo.active_branch)
                    kclass = "active-branch" if is_current else ""
                    yield BranchWindow(branch, is_current, classes=klass)
            except Exception as e:
                yield Label(f"Error: {e}\nEnsure 'seeMe' is a git init'd folder.")
        yield Footer()

    def on_mount(self)-> None:
        self.title = "Git Skyscraper v1.0"

if __name__ == "__main__":
    app = GitBuilding()
    app.run()