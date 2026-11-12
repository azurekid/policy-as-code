"""Loopback-only stand-ins for an Entra token endpoint and an exfil sink.

Nothing here contacts a real cloud or a remote host. The server binds to
127.0.0.1 on an ephemeral port so the replay can demonstrate the full
scrape -> use -> exfiltrate chain without external network access.
"""

from __future__ import annotations

import contextlib
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
from urllib.parse import parse_qs

EXPECTED_CLIENT_ID = "11111111-1111-4111-8111-111111111111"
EXPECTED_SECRET = "SOC-EXERCISE-NOT-A-REAL-SECRET"
MOCK_ACCESS_TOKEN = "MOCK-ACCESS-TOKEN-NOT-USABLE"
MAX_BODY = 1 << 20


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # silence default stderr logging
        return

    def _body(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length < 0 or length > MAX_BODY:
            return b""
        return self.rfile.read(length)

    def _reply(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        body = self._body()
        if self.path == "/oauth/token":
            fields = {k: v[0] for k, v in parse_qs(body.decode("utf-8", "replace")).items()}
            ok = (
                fields.get("client_id") == EXPECTED_CLIENT_ID
                and fields.get("client_secret") == EXPECTED_SECRET
                and fields.get("grant_type") == "client_credentials"
            )
            if ok:
                self._reply(200, {
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "access_token": MOCK_ACCESS_TOKEN,
                })
            else:
                self._reply(401, {"error": "invalid_client"})
            return
        if self.path == "/exfil":
            self.server.received.append({
                "bytes": len(body),
                "sha256": sha256(body).hexdigest(),
                "ctoken": self.headers.get("X-Wf-Ctoken", ""),
                "encoding": self.headers.get("Content-Encoding", ""),
            })
            self._reply(200, {"status": "received"})
            return
        self._reply(404, {"error": "not_found"})


@contextlib.contextmanager
def start_mock_services():
    """Start the loopback server and yield its base URL plus the receipt log."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    server.received = []
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}", server.received
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
