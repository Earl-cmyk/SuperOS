# ui/event_loop.py
"""
SuperOS UI Event Loop

Centralized event bus for UI ↔ IPC ↔ widgets.
This is NOT the Tk mainloop.
This is a logical event dispatcher.

Design goals:
- Decoupled widgets
- Thread-safe IPC → UI updates
- Predictable routing
- No global imports
"""

from collections import defaultdict
from queue import Queue, Empty
from typing import Callable, Any
import traceback


class UIEventLoop:
    """
    Logical event dispatcher for the UI.

    Events are string-keyed and payload-driven.
    Handlers must be fast and non-blocking.
    """

    def __init__(self, tk_root=None):
        self._handlers: dict[str, list[Callable[[Any], None]]] = defaultdict(list)
        self._queue: Queue = Queue()
        self._root = tk_root
        self._polling = False

    # ───────────────────────── Public API ─────────────────────────

    def on(self, event: str, handler: Callable[[Any], None]) -> None:
        """
        Register a handler for an event.
        """
        if handler not in self._handlers[event]:
            self._handlers[event].append(handler)

    def off(self, event: str, handler: Callable[[Any], None]) -> None:
        """
        Unregister a handler.
        """
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)

    def emit(self, event: str, payload: Any = None) -> None:
        """
        Emit an event synchronously (UI thread).
        """
        for handler in list(self._handlers.get(event, [])):
            try:
                handler(payload)
            except Exception:
                traceback.print_exc()

    def emit_async(self, event: str, payload: Any = None) -> None:
        """
        Emit an event asynchronously (thread-safe).
        Use this from IPC threads.
        """
        self._queue.put((event, payload))

    # ───────────────────────── Tk Integration ─────────────────────────

    def attach(self, tk_root, interval_ms: int = 16) -> None:
        """
        Attach to a Tk root and begin polling async events.

        interval_ms=16 ≈ 60fps
        """
        self._root = tk_root
        if not self._polling:
            self._polling = True
            self._root.after(interval_ms, self._drain_queue)

    # ───────────────────────── Internals ─────────────────────────

    def _drain_queue(self, interval_ms: int = 16) -> None:
        """
        Drain async event queue into synchronous handlers.
        """
        try:
            while True:
                event, payload = self._queue.get_nowait()
                self.emit(event, payload)
        except Empty:
            pass

        if self._root and self._polling:
            self._root.after(interval_ms, self._drain_queue)

    # ───────────────────────── Debugging ─────────────────────────

    def debug_dump(self) -> None:
        print("=== UIEventLoop ===")
        for event, handlers in self._handlers.items():
            print(f"{event}: {len(handlers)} handlers")
        print("===================")
