import os

from dotenv import load_dotenv

load_dotenv()


DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}"
    f"/{DB_NAME}"
)