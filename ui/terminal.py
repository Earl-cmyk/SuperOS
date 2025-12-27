# ui/sql_viewer.py
#
# SQL Viewer
#
# Displays SQL query results returned from the SQL runtime.
# This UI does NOT execute SQL itself.

class SQLViewer:
    def __init__(self, ipc):
        self.ipc = ipc
        self.last_result: str | None = None

        self.ipc.subscribe("sql_result", self.on_result)
        self.ipc.subscribe("errors", self.on_error)

    # -------------------------
    # User Actions
    # -------------------------

    def submit_query(self, sql: str):
        self.ipc.send("sql_query", {"sql": sql})

    # -------------------------
    # IPC Handlers
    # -------------------------

    def on_result(self, payload: dict):
        self.last_result = payload.get("output", "")
        self.render()

    def on_error(self, error: str):
        self.last_result = f"ERROR: {error}"
        self.render()

    # -------------------------
    # Rendering
    # -------------------------

    def render(self):
        print("\n=== SQL Viewer ===")
        if self.last_result:
            print(self.last_result)
        else:
            print("(no results)")
        print("==================\n")
