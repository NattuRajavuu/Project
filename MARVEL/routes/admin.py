import json
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from models.database import get_db, row_to_dict

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_user"):
            flash("Please log in to access the admin dashboard.", "warning")
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["admin_user"] = username
            flash("Welcome back to the command deck.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid admin credentials.", "danger")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("main.home"))


@admin_bp.route("/")
@login_required
def dashboard():
    db = get_db()
    counts = {
        "characters": db.execute("SELECT COUNT(*) FROM characters").fetchone()[0],
        "movies": db.execute("SELECT COUNT(*) FROM movies").fetchone()[0],
        "shows": db.execute("SELECT COUNT(*) FROM shows").fetchone()[0],
        "comics": db.execute("SELECT COUNT(*) FROM comics").fetchone()[0],
        "timeline": db.execute("SELECT COUNT(*) FROM timeline_events").fetchone()[0],
    }
    recent_characters = [row_to_dict(row) for row in db.execute("SELECT * FROM characters ORDER BY id DESC LIMIT 5").fetchall()]
    recent_comics = [row_to_dict(row) for row in db.execute("SELECT * FROM comics ORDER BY id DESC LIMIT 5").fetchall()]
    return render_template("admin/dashboard.html", counts=counts, recent_characters=recent_characters, recent_comics=recent_comics)


@admin_bp.route("/characters/new", methods=["GET", "POST"])
@login_required
def add_character():
    if request.method == "POST":
        data = character_form()
        get_db().execute(
            """
            INSERT INTO characters
            (name, alias, category, image, image_url, tagline, origin, powers, weaknesses, teams, enemies, arcs, mcu, variants, timeline, power_level, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data,
        )
        get_db().commit()
        flash("Character added to the encyclopedia.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/character_form.html", character=None)


@admin_bp.route("/movies/new", methods=["GET", "POST"])
@login_required
def add_movie():
    if request.method == "POST":
        form = request.form
        get_db().execute(
            """
            INSERT INTO movies
            (title, phase, release_year, synopsis, cast, villain, post_credit, timeline, connections, comic_inspiration, rating, poster_url, trailer_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                form.get("title", ""),
                form.get("phase", "Phase 6"),
                int(form.get("release_year") or 2026),
                form.get("synopsis", ""),
                form.get("cast", ""),
                form.get("villain", ""),
                form.get("post_credit", ""),
                form.get("timeline", ""),
                form.get("connections", ""),
                form.get("comic_inspiration", ""),
                int(form.get("rating") or 0),
                form.get("poster_url", ""),
                form.get("trailer_url", ""),
            ),
        )
        get_db().commit()
        flash("Movie added to the timeline.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/movie_form.html")


@admin_bp.route("/comics/<int:comic_id>/edit", methods=["GET", "POST"])
@login_required
def edit_comic(comic_id):
    db = get_db()
    comic = db.execute("SELECT * FROM comics WHERE id = ?", (comic_id,)).fetchone()
    if not comic:
        flash("Comic not found.", "danger")
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        form = request.form
        db.execute(
            """
            UPDATE comics
            SET title = ?, year = ?, summary = ?, major_deaths = ?, important_battles = ?, adaptations = ?, reading_order = ?, key_characters = ?
            WHERE id = ?
            """,
            (
                form.get("title", ""),
                int(form.get("year") or 1961),
                form.get("summary", ""),
                form.get("major_deaths", ""),
                form.get("important_battles", ""),
                form.get("adaptations", ""),
                form.get("reading_order", ""),
                form.get("key_characters", ""),
                comic_id,
            ),
        )
        db.commit()
        flash("Comic updated.", "success")
        return redirect(url_for("main.comic_detail", comic_id=comic_id))
    return render_template("admin/comic_form.html", comic=dict(comic))


@admin_bp.route("/timeline/new", methods=["GET", "POST"])
@login_required
def add_timeline():
    if request.method == "POST":
        form = request.form
        get_db().execute(
            "INSERT INTO timeline_events (era, title, branch, event_type) VALUES (?, ?, ?, ?)",
            (form.get("era", ""), form.get("title", ""), form.get("branch", "main"), form.get("event_type", "event")),
        )
        get_db().commit()
        flash("Timeline node added.", "success")
        return redirect(url_for("main.timeline"))
    return render_template("admin/timeline_form.html")


def split_lines(value):
    return [item.strip() for item in value.replace("\r", "").split("\n") if item.strip()]


def character_form():
    form = request.form
    image_name = "placeholder.svg"
    uploaded = request.files.get("image_upload")
    if uploaded and uploaded.filename:
        image_name = uploaded.filename.replace(" ", "-").lower()
        uploaded.save(f"static/images/{image_name}")
    elif form.get("image"):
        image_name = form.get("image")

    return (
        form.get("name", ""),
        form.get("alias", ""),
        form.get("category", "Hero"),
        image_name,
        form.get("image_url", ""),
        form.get("tagline", ""),
        form.get("origin", ""),
        json.dumps(split_lines(form.get("powers", ""))),
        json.dumps(split_lines(form.get("weaknesses", ""))),
        json.dumps(split_lines(form.get("teams", ""))),
        json.dumps(split_lines(form.get("enemies", ""))),
        json.dumps(split_lines(form.get("arcs", ""))),
        json.dumps(split_lines(form.get("mcu", ""))),
        json.dumps(split_lines(form.get("variants", ""))),
        form.get("timeline", ""),
        int(form.get("power_level") or 50),
        form.get("bio", ""),
    )
