# orchestrator/main.py

"""
SuperOS Orchestrator Entry Point

Bootstraps user-space policy layer.
Coordinates kernel, services, and UI.

If this process dies, the kernel must remain intact.
"""

import asyncio
import importlib
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
    # IPC → Process spawn bridge
    # -------------------------

    # async def handle_process_spawn(message: dict):
    #     role = message.get("metadata", {}).get("role", "user")
    #     entrypoint = message["entrypoint"]
    #     requested_caps = set(message.get("capabilities", []))

    #     sys_logger.info(
    #         "orchestrator",
    #         f"spawn request: {entrypoint} ({role})"
    #     )

    #     # 1️⃣ Policy check (DOES NOT EXECUTE)
    #     proc_control.spawn_process(
    #         role=role,
    #         entrypoint=entrypoint.encode(),
    #         requested_caps=requested_caps,
    #     )

    #     # 2️⃣ Actual execution (user-space for now)
    #     await process_manager.spawn(
    #         name=message.get("name", entrypoint),
    #         entrypoint=entrypoint,
    #         capabilities=requested_caps,
    #         metadata=message.get("metadata", {}),
    #     )
        
    #     if entrypoint == "ui.app":
    #         module = importlib.import_module(entrypoint)
    #         module.main()

    async def handle_process_spawn(payload):
        module = importlib.import_module(payload["entrypoint"])

        # UI process must block
        if payload["name"] == "system-ui":
            module.main()
        else:
            asyncio.create_task(asyncio.to_thread(module.main))

    ipc.subscribe("process.spawn", handle_process_spawn)

    # -------------------------
    # BOOT EVENT (important)
    # -------------------------

    await ipc.publish(
        "process.spawn",
        {
            "name": "system-ui",
            "entrypoint": "ui.app",
            "capabilities": [
                "IPC_SEND",
                "IPC_RECV",
                "DISPLAY",
                "INPUT",
            ],
            "metadata": {
                "role": "ui",
                "auto_restart": True,
            },
        },
    )

    sys_logger.info("orchestrator", "system entering steady state")

    # -------------------------
    # Enter IPC event loop
    # -------------------------

    await ipc.run()


if __name__ == "__main__":
    asyncio.run(main())
