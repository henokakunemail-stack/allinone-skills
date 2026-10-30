"""Tiny shop API (stdlib only). Run: PORT=8080 python app.py"""
import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer

USERS = {"admin": "secret"}
ITEMS = [{"id": 1, "name": "Pen", "price": 10}, {"id": 2, "name": "Book", "price": 60}, {"id": 3, "name": "Bag", "price": 100}]


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authed(self):
        return self.headers.get("Authorization") == "Bearer t-admin"

    def _json(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n) or b"{}")

    def do_POST(self):
        data = self._json()
        if self.path == "/login":
            if USERS.get(data.get("user")) == data.get("password"):
                return self._send(200, {"token": "t-admin"})
            return self._send(401, {"error": "bad credentials"})
        if self.path == "/cart":
            if not self._authed():
                return self._send(401, {"error": "unauthorized"})
            subtotal = 0
            for line in data.get("items", []):
                item = next((i for i in ITEMS if i["id"] == line["id"]), None)
                if item is None:
                    return self._send(404, {"error": "no such item"})
                subtotal += item["price"] * line["qty"]
            total = subtotal * 0.9 if subtotal >= 100 else subtotal
            return self._send(200, {"subtotal": subtotal, "total": total})
        self._send(404, {"error": "not found"})

    def do_GET(self):
        if self.path == "/items":
            if not self._authed():
                return self._send(401, {"error": "unauthorized"})
            return self._send(200, ITEMS)
        self._send(404, {"error": "not found"})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", int(os.environ.get("PORT", "8080"))), H).serve_forever()
