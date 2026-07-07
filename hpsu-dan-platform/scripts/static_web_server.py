from __future__ import annotations

import argparse
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "apps" / "web" / "dist"
API_BASE = "http://127.0.0.1:8000"


class Handler(BaseHTTPRequestHandler):
    server_version = "HPSUDANStatic/0.1"

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "web"})
            return
        if self.path.startswith("/api/"):
            self.proxy()
            return
        self.serve_static()

    def do_POST(self) -> None:
        if self.path.startswith("/api/"):
            self.proxy()
            return
        self.send_error(404)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization,Content-Type")
        self.end_headers()

    def serve_static(self) -> None:
        requested = self.path.split("?", 1)[0].lstrip("/")
        file_path = (DIST / requested).resolve() if requested else DIST / "index.html"
        if not str(file_path).startswith(str(DIST.resolve())):
            self.send_error(403)
            return
        if requested.startswith("assets/") and not file_path.is_file():
            self.send_error(404, "Static asset not found")
            return
        if not file_path.is_file():
            file_path = DIST / "index.html"
        if not file_path.is_file():
            self.send_error(503, "Frontend dist is missing. Run npm run build first.")
            return
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type = f"{content_type}; charset=utf-8"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        if "/assets/" in self.path:
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def proxy(self) -> None:
        body = self.rfile.read(int(self.headers.get("Content-Length", "0") or "0"))
        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in {"host", "content-length", "connection"}
        }
        request = Request(
            API_BASE + self.path,
            data=body if body else None,
            headers=headers,
            method=self.command,
        )
        try:
            with urlopen(request, timeout=60) as response:
                data = response.read()
                self.send_response(response.status)
                for key, value in response.headers.items():
                    if key.lower() not in {"transfer-encoding", "connection"}:
                        self.send_header(key, value)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except HTTPError as exc:
            data = exc.read()
            self.send_response(exc.code)
            self.send_header("Content-Type", exc.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except URLError:
            self.send_error(502, "API service is unavailable")

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"{self.client_address[0]} - {fmt % args}")

    def send_json(self, payload: dict[str, str]) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("WEB_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("WEB_PORT", "8080")))
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Frontend: http://127.0.0.1:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
