DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS shows;
DROP TABLE IF EXISTS comics;
DROP TABLE IF EXISTS timeline_events;
DROP TABLE IF EXISTS powers;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS appearances;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    alias TEXT NOT NULL,
    category TEXT NOT NULL,
    image TEXT,
    image_url TEXT,
    tagline TEXT NOT NULL,
    origin TEXT NOT NULL,
    powers TEXT NOT NULL,
    weaknesses TEXT NOT NULL,
    teams TEXT NOT NULL,
    enemies TEXT NOT NULL,
    arcs TEXT NOT NULL,
    mcu TEXT NOT NULL,
    variants TEXT NOT NULL,
    timeline TEXT NOT NULL,
    power_level INTEGER NOT NULL DEFAULT 50,
    bio TEXT NOT NULL
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    phase TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    synopsis TEXT NOT NULL,
    cast TEXT NOT NULL,
    villain TEXT NOT NULL,
    post_credit TEXT NOT NULL,
    timeline TEXT NOT NULL,
    connections TEXT NOT NULL,
    comic_inspiration TEXT NOT NULL,
    rating INTEGER NOT NULL,
    poster_url TEXT,
    trailer_url TEXT
);

CREATE TABLE shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    platform TEXT NOT NULL,
    seasons INTEGER NOT NULL,
    poster_url TEXT,
    plot TEXT NOT NULL,
    character_arcs TEXT NOT NULL,
    season_breakdown TEXT NOT NULL,
    timeline_relevance TEXT NOT NULL,
    easter_eggs TEXT NOT NULL,
    multiverse_impact TEXT NOT NULL
);

CREATE TABLE comics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    summary TEXT NOT NULL,
    major_deaths TEXT NOT NULL,
    important_battles TEXT NOT NULL,
    adaptations TEXT NOT NULL,
    reading_order TEXT NOT NULL,
    key_characters TEXT NOT NULL
);

CREATE TABLE timeline_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    era TEXT NOT NULL,
    title TEXT NOT NULL,
    branch TEXT NOT NULL,
    event_type TEXT NOT NULL
);

CREATE TABLE powers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE appearances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_name TEXT NOT NULL,
    title TEXT NOT NULL,
    media_type TEXT NOT NULL,
    notes TEXT
);
