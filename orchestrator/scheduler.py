# orchestrator/scheduler.py

"""
Scheduling Policy Engine (User Space)

Defines scheduling policy only.
The kernel enforces the actual scheduling.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class SchedulingPolicy:
    priority: int
    time_slice_ms: int
    foreground: bool = False


class SchedulerPolicyEngine:
    def __init__(self):
        self._policies: Dict[int, SchedulingPolicy] = {}

    def assign_policy(
        self,
        pid: int,
        priority: int,
        time_slice_ms: int,
        foreground: bool = False,
    ) -> None:
        """
        Assign or update scheduling policy for a process.
        """
        self._policies[pid] = SchedulingPolicy(
            priority=priority,
            time_slice_ms=time_slice_ms,
            foreground=foreground,
        )

        # kernel_ipc.update_scheduler(pid, policy)
        return

    def remove_policy(self, pid: int) -> None:
        """
        Remove scheduling policy when process exits.
        """
        self._policies.pop(pid, None)

    def get_policy(self, pid: int) -> SchedulingPolicy | None:
        """
        Retrieve scheduling policy for a process.
        """
        return self._policies.get(pid)
