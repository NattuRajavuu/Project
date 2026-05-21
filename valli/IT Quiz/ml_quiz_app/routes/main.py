from flask import Blueprint, render_template, session

from models.db import get_db
from security import generate_csrf_token, login_required

main_bp = Blueprint("main", __name__)


@main_bp.context_processor
def inject_csrf():
    return {"csrf_token": generate_csrf_token}


@main_bp.route("/")
def index():
    stats = get_db().execute(
        "SELECT COUNT(*) AS total, COUNT(DISTINCT category) AS categories FROM questions"
    ).fetchone()
    return render_template("index.html", stats=stats)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    categories = db.execute("SELECT DISTINCT category FROM questions ORDER BY category").fetchall()
    attempts = db.execute(
        "SELECT * FROM quiz_results WHERE user_id = ? ORDER BY date DESC LIMIT 5",
        (session["user_id"],),
    ).fetchall()
    best = db.execute(
        "SELECT MAX(score) AS score, MIN(completion_time) AS time FROM quiz_results WHERE user_id = ?",
        (session["user_id"],),
    ).fetchone()
    return render_template(
        "dashboard.html", user=user, categories=categories, attempts=attempts, best=best
    )


@main_bp.route("/leaderboard")
def leaderboard():
    rows = get_db().execute(
        """
        SELECT users.username, users.badge, quiz_results.score, quiz_results.percentage,
               quiz_results.completion_time, quiz_results.category, quiz_results.difficulty,
               quiz_results.date
        FROM quiz_results
        JOIN users ON users.id = quiz_results.user_id
        ORDER BY quiz_results.score DESC, quiz_results.completion_time ASC, quiz_results.date ASC
        LIMIT 50
        """
    ).fetchall()
    return render_template("leaderboard.html", rows=rows)
