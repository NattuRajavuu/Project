import json

from flask import Blueprint, jsonify, render_template, request

from models.database import get_db, row_to_dict

main_bp = Blueprint("main", __name__)


def fetch_all(table, order_by="id"):
    rows = get_db().execute(f"SELECT * FROM {table} ORDER BY {order_by}").fetchall()
    return [row_to_dict(row) for row in rows]


def fetch_one(table, item_id):
    row = get_db().execute(f"SELECT * FROM {table} WHERE id = ?", (item_id,)).fetchone()
    return row_to_dict(row) if row else None


@main_bp.route("/")
def home():
    db = get_db()
    characters = [row_to_dict(row) for row in db.execute("SELECT * FROM characters ORDER BY power_level DESC LIMIT 8").fetchall()]
    movies = [row_to_dict(row) for row in db.execute("SELECT * FROM movies ORDER BY release_year DESC, id DESC LIMIT 8").fetchall()]
    comics = [row_to_dict(row) for row in db.execute("SELECT * FROM comics ORDER BY year DESC LIMIT 4").fetchall()]
    return render_template("home.html", characters=characters, movies=movies, comics=comics)


@main_bp.route("/characters")
def characters():
    return render_template("characters.html", characters=fetch_all("characters", "name"))


@main_bp.route("/characters/<int:character_id>")
def character_detail(character_id):
    character = fetch_one("characters", character_id)
    if not character:
        return render_template("404.html"), 404
    return render_template("character_detail.html", character=character)


@main_bp.route("/movies")
def movies():
    all_movies = fetch_all("movies", "release_year, id")
    grouped = {}
    for movie in all_movies:
        grouped.setdefault(movie["phase"], []).append(movie)
    return render_template("movies.html", grouped=grouped)


@main_bp.route("/movies/<int:movie_id>")
def movie_detail(movie_id):
    movie = fetch_one("movies", movie_id)
    if not movie:
        return render_template("404.html"), 404
    return render_template("movie_detail.html", movie=movie)


@main_bp.route("/shows")
def shows():
    return render_template("shows.html", shows=fetch_all("shows", "title"))


@main_bp.route("/shows/<int:show_id>")
def show_detail(show_id):
    show = fetch_one("shows", show_id)
    if not show:
        return render_template("404.html"), 404
    return render_template("show_detail.html", show=show)


@main_bp.route("/comics")
def comics():
    return render_template("comics.html", comics=fetch_all("comics", "year"))


@main_bp.route("/comics/<int:comic_id>")
def comic_detail(comic_id):
    comic = fetch_one("comics", comic_id)
    if not comic:
        return render_template("404.html"), 404
    return render_template("comic_detail.html", comic=comic)


@main_bp.route("/timeline")
def timeline():
    return render_template("timeline.html", events=fetch_all("timeline_events", "id"))


@main_bp.route("/jarvis")
def jarvis():
    prompts = [
        "Compare Thor and Hulk power scaling.",
        "Explain the multiverse after Loki.",
        "Give me a reading order for Civil War.",
        "Which movies set up Avengers: Doomsday?",
    ]
    return render_template("jarvis.html", prompts=prompts)


@main_bp.route("/api/search")
def search_api():
    term = request.args.get("q", "").strip()
    if not term:
        return jsonify([])

    like = f"%{term}%"
    db = get_db()
    results = []
    queries = [
        ("characters", "name", "alias", "/characters/", "Character"),
        ("movies", "title", "phase", "/movies/", "Movie"),
        ("shows", "title", "platform", "/shows/", "Series"),
        ("comics", "title", "key_characters", "/comics/", "Comic"),
    ]
    for table, title_col, detail_col, path, label in queries:
        rows = db.execute(
            f"SELECT id, {title_col} AS title, {detail_col} AS detail FROM {table} WHERE {title_col} LIKE ? OR {detail_col} LIKE ? LIMIT 6",
            (like, like),
        ).fetchall()
        for row in rows:
            results.append(
                {
                    "title": row["title"],
                    "detail": row["detail"],
                    "type": label,
                    "url": f"{path}{row['id']}",
                }
            )
    return jsonify(results[:12])


@main_bp.route("/api/jarvis", methods=["POST"])
def jarvis_api():
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").lower()
    db = get_db()

    if "civil war" in question:
        answer = "Civil War is best read as Civil War #1-7 with Front Line tie-ins, then compared with Captain America: Civil War for the MCU adaptation."
    elif "timeline" in question or "order" in question:
        events = db.execute("SELECT era, title FROM timeline_events ORDER BY id LIMIT 8").fetchall()
        answer = "Core chronology: " + " -> ".join(f"{row['era']} {row['title']}" for row in events)
    elif "power" in question or "strong" in question:
        rows = db.execute("SELECT name, power_level FROM characters ORDER BY power_level DESC LIMIT 5").fetchall()
        answer = "Top seeded power readings: " + ", ".join(f"{row['name']} ({row['power_level']})" for row in rows) + "."
    elif "movie" in question or "phase" in question:
        rows = db.execute("SELECT title, phase FROM movies ORDER BY release_year DESC, id DESC LIMIT 6").fetchall()
        answer = "Recent and upcoming MCU entries in the database: " + ", ".join(f"{row['title']} [{row['phase']}]" for row in rows) + "."
    else:
        answer = "JARVIS scan complete: try asking about a character, power level, reading order, MCU phase, or multiverse timeline branch."

    return jsonify({"answer": answer})


@main_bp.app_template_filter("loads")
def loads_filter(value):
    if isinstance(value, list):
        return value
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []
