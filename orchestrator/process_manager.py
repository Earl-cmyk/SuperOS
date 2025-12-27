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

        # IPC handlers
        self.ipc.subscribe("process.spawn", self._on_spawn)
        self.ipc.subscribe("process.kill", self._on_kill)

    # -------------------------
    # IPC Handlers
    # -------------------------

    async def _on_spawn(self, payload: dict):
        project_id = payload.get("project_id")
        if not project_id:
            logger.error("process.spawn missing project_id")
            return

        pid = next(self._pid_gen)
        proc = Process(pid=pid, project_id=project_id)
        self._processes[pid] = proc

        logger.info(f"Process spawned pid={pid} project={project_id}")

        await self.ipc.publish(
            "process.started",
            {
                "pid": pid,
                "project_id": project_id,
                "state": proc.state,
            },
        )

        # Simulated execution
        proc.state = ProcessState.RUNNING

    async def _on_kill(self, payload: dict):
        pid = payload.get("pid")
        proc = self._processes.get(pid)

        if not proc:
            logger.warning(f"process.kill unknown pid={pid}")
            return

        proc.state = ProcessState.TERMINATED
        logger.info(f"Process terminated pid={pid}")

        await self.ipc.publish(
            "process.exited",
            {
                "pid": pid,
                "project_id": proc.project_id,
                "state": proc.state,
            },
        )

        self._processes.pop(pid, None)

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
