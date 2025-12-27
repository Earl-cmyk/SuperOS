# services/shells/powershell/pwsh_service.py
#
# PowerShell Shell Service (User-Space)
#
# Provides a controlled PowerShell shell via a pseudo-terminal.
# PowerShell is treated as an unprivileged IPC client.

import os
import pty


class PowerShellShellService:
    def __init__(self, shell_path: str = "pwsh"):
        self.shell_path = shell_path

    def spawn(self, env: dict | None = None):
        env = env or {}

        pid, fd = pty.fork()
        if pid == 0:
            # Child process: exec PowerShell
            os.execve(
                self.shell_path,
                [self.shell_path],
                {**os.environ, **env},
            )

        return {
            "pid": pid,
            "pty_fd": fd,
        }

    def write(self, pty_fd: int, data: str):
        os.write(pty_fd, data.encode())

    def read(self, pty_fd: int, size: int = 1024) -> str:
        return os.read(pty_fd, size).decode(errors="ignore")
