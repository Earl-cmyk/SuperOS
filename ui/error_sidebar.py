# ui/error_sidebar.py
#
# Error Sidebar
#
# Displays system and process errors emitted via IPC.
# The UI does not interpret or suppress errors.

class ErrorSidebar:
    def __init__(self):
        self._errors: list[str] = []

    def push(self, error: str):
        self._errors.append(error)
        self.render()

    def render(self):
        print("\n=== Errors ===")
        for err in self._errors[-10:]:
            print(f"• {err}")
        print("==============\n")
