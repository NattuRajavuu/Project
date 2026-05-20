from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PORT = 8000
ROOT = Path(__file__).parent / "python_site"


class SpaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        requested = ROOT / path.lstrip("/")
        if path != "/" and not requested.exists():
            self.path = "/index.html"
        return super().do_GET()


if __name__ == "__main__":
    server = ThreadingHTTPServer(("localhost", PORT), SpaHandler)
    print(f"Luxe Atelier running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
