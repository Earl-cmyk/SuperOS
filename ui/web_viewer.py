# ui/web_viewer.py
#
# Web Viewer
#
# Displays content fetched by the web_service.
# No direct network access from UI.

class WebViewer:
    def __init__(self, ipc):
        self.ipc = ipc
        self.current_url: str | None = None
        self.content: str | None = None

        self.ipc.subscribe("web_content", self.on_content)
        self.ipc.subscribe("errors", self.on_error)

    # -------------------------
    # User Actions
    # -------------------------

    def navigate(self, url: str):
        self.current_url = url
        self.ipc.send("web_fetch", {"url": url})

    # -------------------------
    # IPC Handlers
    # -------------------------

    def on_content(self, payload: dict):
        self.content = payload.get("content", "")
        self.render()

    def on_error(self, error: str):
        self.content = f"ERROR: {error}"
        self.render()

    # -------------------------
    # Rendering
    # -------------------------

    def render(self):
        print("\n=== Web Viewer ===")
        if self.current_url:
            print(f"URL: {self.current_url}\n")
        print(self.content or "(no content)")
        print("==================\n")
