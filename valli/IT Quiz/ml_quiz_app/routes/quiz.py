import random
import time
from datetime import date
from hashlib import sha256

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from models.db import get_db
from security import generate_csrf_token, login_required, validate_csrf

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


@quiz_bp.context_processor
def inject_csrf():
    return {"csrf_token": generate_csrf_token}


def shuffled_question(row):
    options = [
        {"key": "option1", "text": row["option1"]},
        {"key": "option2", "text": row["option2"]},
        {"key": "option3", "text": row["option3"]},
        {"key": "option4", "text": row["option4"]},
    ]
    random.shuffle(options)
    return {
        "id": row["id"],
        "category": row["category"],
        "difficulty": row["difficulty"],
        "question": row["question"],
        "options": options,
    }


@quiz_bp.route("/start", methods=["POST"])
@login_required
def start():
    validate_csrf()
    category = request.form.get("category", "All")
    difficulty = request.form.get("difficulty", "All")
    mode = request.form.get("mode", "Standard")

    clauses = []
    params = []
    if category != "All":
        clauses.append("category = ?")
        params.append(category)
    if difficulty != "All":
        clauses.append("difficulty = ?")
        params.append(difficulty)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    db = get_db()
    if mode == "Daily Challenge":
        candidates = db.execute(f"SELECT * FROM questions {where}", params).fetchall()
        today = date.today().isoformat()
        rows = sorted(
            candidates,
            key=lambda row: sha256(f"{today}:{category}:{difficulty}:{row['id']}".encode()).hexdigest(),
        )[:25]
    else:
        rows = db.execute(f"SELECT * FROM questions {where} ORDER BY RANDOM() LIMIT 25", params).fetchall()

    if len(rows) < 25:
        return redirect(url_for("main.dashboard"))

    session["quiz"] = {
        "question_ids": [row["id"] for row in rows],
        "current": 0,
        "answers": {},
        "started_at": int(time.time()),
        "question_started_at": int(time.time()),
        "category": category,
        "difficulty": difficulty,
        "mode": mode,
    }
    return redirect(url_for("quiz.play"))


@quiz_bp.route("/")
@login_required
def play():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("main.dashboard"))
    if quiz["current"] >= len(quiz["question_ids"]):
        return redirect(url_for("quiz.finish"))

    question_id = quiz["question_ids"][quiz["current"]]
    row = get_db().execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    return render_template(
        "quiz.html",
        question=shuffled_question(row),
        current=quiz["current"] + 1,
        total=len(quiz["question_ids"]),
        seconds=30,
    )


@quiz_bp.route("/answer", methods=["POST"])
@login_required
def answer():
    validate_csrf()
    quiz = session.get("quiz")
    if not quiz or quiz["current"] >= len(quiz["question_ids"]):
        return jsonify({"redirect": url_for("main.dashboard")})

    question_id = str(quiz["question_ids"][quiz["current"]])
    elapsed = int(time.time()) - quiz["question_started_at"]
    answer_key = request.form.get("answer")

    # Only accept the first answer for a question and force timeouts after 30 seconds.
    if question_id not in quiz["answers"]:
        quiz["answers"][question_id] = None if elapsed > 30 else answer_key
        quiz["current"] += 1
        quiz["question_started_at"] = int(time.time())
        session["quiz"] = quiz

    if quiz["current"] >= len(quiz["question_ids"]):
        return jsonify({"redirect": url_for("quiz.finish")})
    return jsonify({"redirect": url_for("quiz.play")})


@quiz_bp.route("/finish")
@login_required
def finish():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("main.dashboard"))

    db = get_db()
    rows = db.execute(
        f"SELECT * FROM questions WHERE id IN ({','.join(['?'] * len(quiz['question_ids']))})",
        quiz["question_ids"],
    ).fetchall()
    by_id = {row["id"]: row for row in rows}
    answers = quiz["answers"]
    score = sum(1 for qid, ans in answers.items() if by_id[int(qid)]["correct_answer"] == ans)
    total = len(quiz["question_ids"])
    percentage = round((score / total) * 100, 2)
    completion_time = int(time.time()) - quiz["started_at"]

    cur = db.execute(
        """
        INSERT INTO quiz_results (user_id, score, percentage, completion_time, category, difficulty)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (session["user_id"], score, percentage, completion_time, quiz["category"], quiz["difficulty"]),
    )
    result_id = cur.lastrowid

    detail_rows = []
    for question_id in quiz["question_ids"]:
        row = by_id[question_id]
        user_answer = answers.get(str(question_id))
        is_correct = int(user_answer == row["correct_answer"])
        db.execute(
            "INSERT INTO quiz_answers (result_id, question_id, user_answer, is_correct) VALUES (?, ?, ?, ?)",
            (result_id, question_id, user_answer, is_correct),
        )
        detail_rows.append({"question": row, "user_answer": user_answer, "is_correct": is_correct})

    xp_gain = score * 10
    badge = "Rookie"
    total_xp = db.execute("SELECT xp FROM users WHERE id = ?", (session["user_id"],)).fetchone()["xp"] + xp_gain
    if total_xp >= 2000:
        badge = "ML Architect"
    elif total_xp >= 1000:
        badge = "Neural Navigator"
    elif total_xp >= 500:
        badge = "Data Explorer"
    db.execute("UPDATE users SET xp = ?, badge = ? WHERE id = ?", (total_xp, badge, session["user_id"]))
    db.commit()

    session.pop("quiz", None)
    session["last_result_id"] = result_id
    return render_template(
        "results.html",
        score=score,
        total=total,
        percentage=percentage,
        completion_time=completion_time,
        details=detail_rows,
    )
