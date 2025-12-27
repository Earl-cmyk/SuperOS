# services/shells/bash/bash_service.py
#
# Bash Shell Service (User-Space)
#
# Provides a controlled Bash shell via a pseudo-terminal.
# This shell is an IPC client, not an execution authority.

import os
import pty
import subprocess


class BashShellService:
    def __init__(self, shell_path: str = "/bin/bash"):
        self.shell_path = shell_path

    def spawn(self, env: dict | None = None):
        env = env or {}

        pid, fd = pty.fork()
        if pid == 0:
            # Child process: exec bash
            os.execve(
                self.shell_path,
                [self.shell_path],
                {**os.environ, **env},
            )

        # Parent process: return PTY fd + pid
        return {
            "pid": pid,
            "pty_fd": fd,
        }

    def write(self, pty_fd: int, data: str):
        os.write(pty_fd, data.encode())

    def read(self, pty_fd: int, size: int = 1024) -> str:
        return os.read(pty_fd, size).decode(errors="ignore")
