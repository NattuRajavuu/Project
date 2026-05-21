DROP TABLE IF EXISTS quiz_answers;
DROP TABLE IF EXISTS quiz_results;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    xp INTEGER NOT NULL DEFAULT 0,
    badge TEXT NOT NULL DEFAULT 'Rookie'
);

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    question TEXT NOT NULL UNIQUE,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_answer TEXT NOT NULL CHECK (correct_answer IN ('option1', 'option2', 'option3', 'option4')),
    explanation TEXT NOT NULL,
    difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard'))
);

CREATE TABLE quiz_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    percentage REAL NOT NULL,
    completion_time INTEGER NOT NULL,
    date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    category TEXT NOT NULL DEFAULT 'All',
    difficulty TEXT NOT NULL DEFAULT 'All',
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE quiz_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer TEXT,
    is_correct INTEGER NOT NULL,
    FOREIGN KEY (result_id) REFERENCES quiz_results (id),
    FOREIGN KEY (question_id) REFERENCES questions (id)
);

