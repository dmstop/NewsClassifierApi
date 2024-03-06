from pathlib import Path

MAX_DB_LENGHT = 10000

DB_DIR = Path(__file__).resolve().parent / "db"

DB_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite+aiosqlite:///{DB_DIR}/test.db"

