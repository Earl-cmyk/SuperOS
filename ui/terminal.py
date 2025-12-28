# ui/terminal.py
#
# Controlled Terminal UI
#
# Acts as a frontend to shell services via IPC.
# No direct PTY or subprocess access.

class TerminalView:
    def __init__(self, ipc):
        self.ipc = ipc
        self.buffer: list[str] = []

        self.ipc.subscribe("terminal_output", self.on_output)
        self.ipc.subscribe("errors", self.on_error)

    # -------------------------
    # User Actions
    # -------------------------

    def send_input(self, text: str):
        self.ipc.send("terminal_input", {"data": text})

    # -------------------------
    # IPC Handlers
    # -------------------------

    def on_output(self, payload: dict):
        
        output = payload.get("data", "")
        self.buffer.append(output)
        self.render()

    def on_error(self, error: str):
        self.buffer.append(f"[ERROR] {error}")
        self.render()

    # -------------------------
    # Rendering
    # -------------------------

    def render(self):
        print("\n=== Terminal ===")
        for line in self.buffer[-50:]:
            print(line)
        print("================\n")

    def write(self, payload: dict | str):
            if isinstance(payload, dict):
                text = payload.get("data", "")
            else:
                text = str(payload)

            self.buffer.append(text)
            self.render()