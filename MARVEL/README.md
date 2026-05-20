# MarvelVerse Explorer

MarvelVerse Explorer is a Python-powered Flask website styled like a cinematic comic-book encyclopedia. It includes Marvel character profiles, MCU movie phases, series pages, comic arcs, a glowing timeline, live search, an admin dashboard, and a local JARVIS-style assistant.

## Features

- Flask + Jinja website running on Python 3.12+
- SQLite database with seeded Marvel-inspired encyclopedia data
- 20 character profiles with powers, weaknesses, teams, enemies, variants, and power meters
- 30+ MCU movie entries across Phases 1-6
- Marvel series archive and 15 comic story arcs
- Live search across characters, movies, shows, and comics
- Interactive multiverse timeline
- Admin dashboard for adding characters, movies, timeline nodes, uploading images, and editing comics
- Comic-book UI with animated panels, glowing cards, particle sparks, and responsive design

## VS Code Setup

1. Open this folder in Visual Studio Code.
2. Open the VS Code terminal with `Ctrl + Shift + \``.
3. Make sure Python 3.12 or newer is selected as the interpreter.

## Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```powershell
pip install -r requirements.txt
```

## Initialize Database

The app creates the database automatically on first run. You can also rebuild it manually:

```powershell
python init_db.py
```

To add real character images and movie/series posters from Wikimedia thumbnails:

```powershell
python populate_media.py
```

## Run Website

```powershell
python app.py
```

For a no-reloader local run, use:

```powershell
python run_server.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

## Admin Login

```text
Username: admin
Password: avengers
```

Change these defaults in `config.py` before using the app outside local development.

## Project Structure

```text
app.py
run_server.py
populate_media.py
config.py
init_db.py
requirements.txt
database/
  schema.sql
models/
  database.py
routes/
  main.py
  admin.py
templates/
  *.html
  admin/
static/
  css/style.css
  js/app.js
  images/*.svg
assets/
```

## Notes

This is a fan-made educational project. The included character art is custom SVG placeholder artwork generated for the app, not official Marvel artwork.
