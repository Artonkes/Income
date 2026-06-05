from dotenv import load_dotenv
from pathlib import Path
import os

current_dir = Path(__file__).parent

dotenv_path = current_dir.parent/ ".."/".env"

if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    print(f".env is no exist at {dotenv_path}")


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

URL_DATABASE = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"