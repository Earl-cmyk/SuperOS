# orchestrator/process_control.py

"""
Process Lifecycle Control (Policy Layer)

This module manages process lifecycles from user space.
It never executes code directly and never grants authority.
"""

from typing import List, Set
from orchestrator.capability_enforcer import CapabilityEnforcer, CapabilityViolation


class ProcessControl:
    def __init__(self, enforcer: CapabilityEnforcer):
        self.enforcer = enforcer

    def spawn_process(
        self,
        role: str,
        entrypoint: bytes,
        requested_caps: Set[str],
    ) -> None:
        """
        Request the kernel to spawn a process.
        """
        allowed_caps = self.enforcer.filter(role, requested_caps)

        if not allowed_caps:
            raise CapabilityViolation("no allowed capabilities for process")

        # IPC / syscall bridge stub
        # kernel_syscall.spawn(entrypoint, allowed_caps)
        return

    def kill_process(self, role: str, pid: int) -> None:
        """
        Request termination of a process.
        """
        self.enforcer.check(role, "PROC_KILL")

        # kernel_syscall.kill(pid)
        return

    def list_processes(self) -> List[int]:
        """
        Query kernel for running processes.
        """
        # kernel_ipc.list_processes()
        return []
