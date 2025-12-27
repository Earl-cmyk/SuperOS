# ui/ml_panel.py
#
# ML Panel
#
# UI panel for interacting with machine-learning services.
# This panel NEVER runs models locally.
# It only sends requests and displays results.

class MLPanel:
    def __init__(self, ipc):
        self.ipc = ipc
        self._history: list[dict] = []

    # -------------------------
    # User Actions
    # -------------------------

    def submit_prompt(self, prompt: str):
        """
        Send an ML inference request.
        """
        request = {
            "prompt": prompt,
        }

        self._history.append({"role": "user", "content": prompt})
        self.ipc.send("ml_request", request)

    # -------------------------
    # IPC Handlers
    # -------------------------

    def on_response(self, response: dict):
        """
        Receive ML inference output.
        """
        content = response.get("content", "")
        self._history.append({"role": "model", "content": content})
        self.render()

    def on_error(self, error: str):
        self._history.append({"role": "error", "content": error})
        self.render()

    # -------------------------
    # Rendering
    # -------------------------

    def render(self):
        print("\n=== ML Panel ===")
        for item in self._history[-20:]:
            role = item["role"]
            content = item["content"]
            print(f"[{role.upper()}] {content}")
        print("================\n")
