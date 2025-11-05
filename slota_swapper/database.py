import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv, find_dotenv


# Load environment variables from nearest .env (project root) or local package .env
dotenv_path = find_dotenv(usecwd=True)
if not dotenv_path:
    pkg_env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(pkg_env_path):
        dotenv_path = pkg_env_path
if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path, override=False)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Explicitly fail early to avoid silent SQLite fallbacks when misconfigured
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. Configure it in .env."
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables() -> None:
    Base.metadata.create_all(bind=engine)


