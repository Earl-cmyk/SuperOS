# orchestrator/process_manager.py
#
# Process Manager
#
# User-space authority responsible for managing process lifecycles.
# This component enforces policy; the kernel enforces mechanism.
# No direct execution occurs here.

import itertools
from enum import Enum
from typing import Dict
import importlib
import asyncio

from loguru import logger

from orchestrator.ipc_bus import IPCBus


class ProcessState(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    EXITED = "exited"
    TERMINATED = "terminated"


class Process:
    def __init__(self, pid: int, project_id: str):
        self.pid = pid
        self.project_id = project_id
        self.state = ProcessState.CREATED


class ProcessManager:
    def __init__(self, ipc: IPCBus):
        self.ipc = ipc
        self._pid_gen = itertools.count(start=1)
        self._processes: Dict[int, Process] = {}

    async def spawn(
        self,
        name: str,
        entrypoint: str,
        capabilities: set,
        metadata: dict,
    ):
        pid = next(self._pid_gen)
        proc = Process(pid=pid, project_id=name)
        self._processes[pid] = proc

        logger.info(f"Process spawned pid={pid} name={name}")

        await self.ipc.publish(
            "process.started",
            {
                "pid": pid,
                "name": name,
                "entrypoint": entrypoint,
                "state": proc.state,
            },
        )

        proc.state = ProcessState.RUNNING

        # 🔥 ACTUALLY RUN THE MODULE
        try:
            module = importlib.import_module(entrypoint)

            if hasattr(module, "main"):
                asyncio.create_task(
                    asyncio.to_thread(module.main)
                )
            else:
                logger.error(
                    f"{entrypoint} has no main()"
                )

        except Exception as e:
            logger.exception(f"Failed to start {entrypoint}: {e}")

    # -------------------------
    # Introspection
    # -------------------------

    def list_processes(self):
        return {
            pid: {
                "project_id": proc.project_id,
                "state": proc.state,
            }
            for pid, proc in self._processes.items()
        }
