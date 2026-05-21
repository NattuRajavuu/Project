CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price REAL NOT NULL,
  rating REAL NOT NULL,
  tag TEXT,
  image TEXT,
  description TEXT,
  colors TEXT
);

CREATE TABLE IF NOT EXISTS faqs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic TEXT,
  question TEXT,
  answer TEXT,
  keywords TEXT
);

CREATE TABLE IF NOT EXISTS intents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  intent TEXT,
  trigger_keywords TEXT,
  response TEXT
);

CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  status TEXT,
  tracking TEXT,
  items TEXT,
  total REAL,
  created_at TEXT
);

CREATE TABLE IF NOT EXISTS chat_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_message TEXT,
  bot_response TEXT,
  intent TEXT,
  created_at TEXT
);
