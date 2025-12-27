"""
Capability Enforcer (User-Space Policy Layer)

This module enforces capability policy on the orchestrator side.
It does NOT grant authority — the kernel does that.
It only decides *what to request* and *what to deny*.

If this layer is bypassed, the kernel will still enforce security.
"""

from dataclasses import dataclass
from typing import Dict, Set


@dataclass(frozen=True)
class Capability:
    """
    Logical representation of a capability request.
    Kernel validates the real capability; this is policy-only.
    """
    name: str


class CapabilityViolation(Exception):
    """Raised when a capability request violates policy."""
    pass


class CapabilityEnforcer:
    """
    User-space capability policy engine.

    Responsibilities:
    - Define allowed capabilities per process type
    - Validate requests before syscall / IPC
    - Provide audit-friendly decision points
    """

    def __init__(self):
        self._policies: Dict[str, Set[str]] = {}

    def register_policy(self, role: str, capabilities: Set[str]) -> None:
        """
        Register allowed capabilities for a role.
        Example roles: runtime, ml_service, ui, build_service
        """
        self._policies[role] = set(capabilities)

    def check(self, role: str, capability: str) -> None:
        """
        Check whether a role is allowed to request a capability.
        Raises CapabilityViolation if denied.
        """
        allowed = self._policies.get(role)

        if allowed is None:
            raise CapabilityViolation(
                f"no capability policy defined for role '{role}'"
            )

        if capability not in allowed:
            raise CapabilityViolation(
                f"capability '{capability}' denied for role '{role}'"
            )

    def filter(self, role: str, requested: Set[str]) -> Set[str]:
        """
        Filter a requested capability set down to allowed ones.
        Denied capabilities are silently dropped.
        """
        allowed = self._policies.get(role, set())
        return requested.intersection(allowed)


# ---- Default policy bootstrap (example) ----

def default_enforcer() -> CapabilityEnforcer:
    enforcer = CapabilityEnforcer()

    enforcer.register_policy(
        role="ui",
        capabilities={
            "IPC_SEND",
            "IPC_RECV",
        },
    )

    enforcer.register_policy(
        role="runtime",
        capabilities={
            "PROC_SPAWN",
            "IPC_SEND",
            "IPC_RECV",
            "FS_READ",
            "FS_WRITE",
        },
    )

    enforcer.register_policy(
        role="ml_service",
        capabilities={
            "IPC_SEND",
            "IPC_RECV",
            "FS_READ",
            "NET_OUTBOUND",
        },
    )

    enforcer.register_policy(
        role="build_service",
        capabilities={
            "PROC_SPAWN",
            "IPC_SEND",
            "IPC_RECV",
            "FS_READ",
            "FS_WRITE",
        },
    )

    return enforcer
