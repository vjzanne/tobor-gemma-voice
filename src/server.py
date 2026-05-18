"""
Visualizer Server
=================
Flask + Socket.IO: serves the canvas visualization and pushes
relational state readings to connected browsers in real time.
"""

import os
from threading import Lock

try:
    from flask import Flask, send_from_directory
    from flask_socketio import SocketIO
    _SERVER_AVAILABLE = True
except ImportError:
    _SERVER_AVAILABLE = False

_WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")


class VisualizerServer:
    """Minimal Flask-SocketIO server for real-time emotional visualization."""

    def __init__(self, port: int = 5000):
        if not _SERVER_AVAILABLE:
            raise RuntimeError(
                "Flask / flask-socketio missing. Install with:\n"
                "  pip install flask flask-socketio"
            )
        self.port = port
        self._lock = Lock()
        self._app = Flask(__name__, static_folder=_WEB_DIR)
        self._app.config["SECRET_KEY"] = "tobor-gemma-voice"
        self._sio = SocketIO(self._app, cors_allowed_origins="*", async_mode="threading")
        self._setup_routes()

    def _setup_routes(self):
        @self._app.route("/")
        def index():
            return send_from_directory(_WEB_DIR, "index.html")

    def broadcast(self, state: dict):
        """Push a relational state reading to all connected browsers."""
        with self._lock:
            self._sio.emit("state", state)

    def run(self):
        self._sio.run(
            self._app,
            host="0.0.0.0",
            port=self.port,
            log_output=False,
            allow_unsafe_werkzeug=True,
        )
