import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()


def criar_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)


if __name__ == "__main__":
    engine = criar_engine()
    with engine.connect() as conn:
        print(conn.execute(text("SELECT version()")).scalar())