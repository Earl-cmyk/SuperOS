# ui/ipc_bridge.py
#
# IPC Bridge
#
# UI-facing IPC client.
# Sends requests and subscribes to events.
# Does NOT execute or authorize actions.

import queue
import threading


class IPCBridge:
    def __init__(self):
        self._subscriptions: dict[str, list] = {}
        self._event_queue = queue.Queue()
        self._running = True

        self._thread = threading.Thread(
            target=self._event_loop,
            daemon=True,
        )
        self._thread.start()

    # -------------------------
    # Subscription API
    # -------------------------

    def subscribe(self, topic: str, handler):
        if topic not in self._subscriptions:
            self._subscriptions[topic] = []
        self._subscriptions[topic].append(handler)

    # -------------------------
    # Sending Requests
    # -------------------------

    def send(self, topic: str, payload: dict):
        """
        Send a request to user-space services or orchestrator.
        This is a stub; real transport is injected later.
        """
        self._event_queue.put((topic, payload))

    # -------------------------
    # Internal Event Loop
    # -------------------------

    def _event_loop(self):
        while self._running:
            try:
                topic, payload = self._event_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            handlers = self._subscriptions.get(topic, [])
            for handler in handlers:
                try:
                    handler(payload)
                except Exception as e:
                    err_handlers = self._subscriptions.get("errors", [])
                    for err in err_handlers:
                        err(str(e))

    # -------------------------
    # Shutdown
    # -------------------------

    def close(self):
        self._running = False
