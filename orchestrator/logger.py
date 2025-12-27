# orchestrator/logger.py

"""
Central Log Aggregator (User Space)

Collects and normalizes logs from:
- Kernel events
- Orchestrator decisions
- User-space services

This module does NOT generate authority.
It only observes and records.
"""

from datetime import datetime
from typing import Any, Dict, List


class LogRecord:
    def __init__(self, source: str, level: str, message: str, meta: Dict[str, Any] | None = None):
        self.timestamp = datetime.utcnow().isoformat()
        self.source = source
        self.level = level
        self.message = message
        self.meta = meta or {}

    def serialize(self) -> Dict[str, Any]:
        return {
            "ts": self.timestamp,
            "source": self.source,
            "level": self.level,
            "message": self.message,
            "meta": self.meta,
        }


class Logger:
    """
    Centralized, append-only logger.
    """

    def __init__(self):
        self._records: List[LogRecord] = []

    def log(self, source: str, level: str, message: str, meta: Dict[str, Any] | None = None) -> None:
        record = LogRecord(source, level, message, meta)
        self._records.append(record)

        # Stub: forward to file / stdout / external sink
        # print(record.serialize())

    def info(self, source: str, message: str, meta: Dict[str, Any] | None = None) -> None:
        self.log(source, "INFO", message, meta)

    def warn(self, source: str, message: str, meta: Dict[str, Any] | None = None) -> None:
        self.log(source, "WARN", message, meta)

    def error(self, source: str, message: str, meta: Dict[str, Any] | None = None) -> None:
        self.log(source, "ERROR", message, meta)

    def dump(self) -> List[Dict[str, Any]]:
        """
        Dump all logs (for debugging / UI).
        """
        return [r.serialize() for r in self._records]
