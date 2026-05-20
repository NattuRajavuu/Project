from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "marvelverse.db"
SECRET_KEY = "change-this-secret-key-before-deploying"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "avengers"
