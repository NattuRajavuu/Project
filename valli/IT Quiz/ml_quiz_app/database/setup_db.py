import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "database.db"
SCHEMA_PATH = ROOT / "database" / "schema.sql"
QUESTIONS_PATH = ROOT / "questions" / "ml_questions.json"


def setup_database():
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
        conn.executemany(
            """
            INSERT INTO questions (
                category, question, option1, option2, option3, option4,
                correct_answer, explanation, difficulty
            )
            VALUES (
                :category, :question, :option1, :option2, :option3, :option4,
                :correct_answer, :explanation, :difficulty
            )
            """,
            questions,
        )
        conn.commit()
    print(f"Database ready: {DB_PATH}")
    print(f"Seeded questions: {len(questions)}")


if __name__ == "__main__":
    setup_database()
