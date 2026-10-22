# SPDX-License-Identifier: AGPL-3.0-or-later
# Concat Automation Client (JSON-RPC bridge to Concat app)

import json
import os
import socket
import sys
from typing import Any, Dict, Optional

class ConcatClient:
    """Communicates with a running Concat instance via JSON-RPC."""

    def __init__(self, address: Optional[str] = None, token: Optional[str] = None):
        self.address = address
        self.token = token
        if not self.address or not self.token:
            self._load_from_automation_info()

    def _load_from_automation_info(self) -> None:
        """Finds active automation.json in %APPDATA%/app.concat.editor."""
        appdata = os.environ.get("APPDATA", "")
        paths = [
            os.path.join(appdata, "app.concat.editor", "automation.json"),
            os.path.join(appdata, "Concat", "automation.json"),
        ]
        for p in paths:
            if os.path.isfile(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.address = data.get("address", "127.0.0.1:7420")
                        self.token = data.get("token")
                        return
                except Exception:
                    pass

    def call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Performs a JSON-RPC request to Concat server."""
        if not self.address or not self.token:
            raise RuntimeError("Concat is not running or Automation is disabled in Settings > Automation.")

        host, port_s = self.address.split(":")
        port = int(port_s)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        try:
            s.connect((host, port))
            # Handshake line 1
            auth_msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "auth",
                "params": {"token": self.token}
            }
            s.sendall(json.dumps(auth_msg).encode("utf-8") + b"\n")
            auth_resp_raw = s.recv(4096).decode("utf-8")
            auth_resp = json.loads(auth_resp_raw.strip())
            if "error" in auth_resp:
                raise RuntimeError(f"Auth failed: {auth_resp['error']}")

            # Call method
            req = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": method,
                "params": params or {}
            }
            s.sendall(json.dumps(req).encode("utf-8") + b"\n")
            
            resp_bytes = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp_bytes += chunk
                if b"\n" in chunk:
                    break

            resp = json.loads(resp_bytes.decode("utf-8").strip())
            if "error" in resp:
                raise RuntimeError(f"Error from Concat: {resp['error']}")
            return resp.get("result", {})
        finally:
            s.close()

if __name__ == "__main__":
    client = ConcatClient()
    try:
        ver = client.call("concat_version")
        print("Connected to Concat successfully:", ver)
    except Exception as e:
        print("Could not connect to Concat:", e)
