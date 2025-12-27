# orchestrator/main.py

"""
SuperOS Orchestrator Entry Point

Bootstraps user-space policy layer.
Coordinates kernel, services, and UI.

If this process dies, the kernel must remain intact.
"""

import asyncio
from loguru import logger

from orchestrator.capability_enforcer import default_enforcer
from orchestrator.process_control import ProcessControl
from orchestrator.scheduler import SchedulerPolicyEngine
from orchestrator.logger import Logger
from orchestrator.process_manager import ProcessManager
from orchestrator.ipc_bus import IPCBus


async def main() -> None:
    # -------------------------
    # Boot logging first
    # -------------------------

    sys_logger = Logger()
    sys_logger.info("orchestrator", "orchestrator starting")

    # -------------------------
    # Core IPC spine
    # -------------------------

    ipc = IPCBus()

    # -------------------------
    # Policy & control layers
    # -------------------------

    enforcer = default_enforcer()
    scheduler = SchedulerPolicyEngine()
    proc_control = ProcessControl(enforcer)

    # -------------------------
    # Process lifecycle manager
    # -------------------------

    process_manager = ProcessManager(ipc)

    sys_logger.info("orchestrator", "core managers online")

    # -------------------------
    # BOOT EVENT (important)
    # -------------------------

    await ipc.publish(
        "process.spawn",
        {"project_id": "boot-demo"},
    )

    sys_logger.info("orchestrator", "system entering steady state")

    # -------------------------
    # Enter IPC event loop
    # -------------------------

    await ipc.run()


if __name__ == "__main__":
    asyncio.run(main())
