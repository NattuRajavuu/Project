from pathlib import Path

from flask import send_from_directory

from backend.app import create_app


PORT = 8000
ROOT = Path(__file__).parent / "python_site"

app = create_app()


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/<path:path>")
def static_or_spa(path):
    requested = ROOT / path
    if requested.is_file():
        return send_from_directory(ROOT, path)
    return send_from_directory(ROOT, "index.html")


if __name__ == "__main__":
    print(f"Luxe Atelier running at http://127.0.0.1:{PORT}")
    print("API endpoints are available on the same server under /api.")
    print("Press Ctrl+C to stop.")
    app.run(debug=True, host="127.0.0.1", port=PORT)
