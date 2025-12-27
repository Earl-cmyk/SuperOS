# ui/project_explorer.py
#
# Project Explorer
#
# Displays projects and project structure.
# Projects are discovered via IPC, not filesystem crawling.

class ProjectExplorer:
    def __init__(self, ipc):
        self.ipc = ipc
        self.projects: list[dict] = []

        self.ipc.subscribe("projects_list", self.on_projects_list)

    # -------------------------
    # User Actions
    # -------------------------

    def refresh(self):
        self.ipc.send("list_projects", {})

    def open_project(self, project_id: str):
        self.ipc.send("open_project", {"project_id": project_id})

    # -------------------------
    # IPC Handlers
    # -------------------------

    def on_projects_list(self, payload: dict):
        self.projects = payload.get("projects", [])
        self.render()

    # -------------------------
    # Rendering
    # -------------------------

    def render(self):
        print("\n=== Projects ===")
        for proj in self.projects:
            print(f"- {proj.get('name')} ({proj.get('id')})")
        print("================\n")
