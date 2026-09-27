"""
Database engine and session management.

Deliberately simple: a synchronous SQLAlchemy engine pointed at SQLite by
default. For a single-user personal assistant this is more than fast
enough and avoids the complexity of an async database driver. Moving to
PostgreSQL later only means changing `DATABASE_URL` in `.env` and adding
a driver (e.g. `psycopg2-binary`) to requirements.txt — no code here
needs to change.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# SQLite needs this flag because FastAPI can use a different thread per
# request; other databases (PostgreSQL, MySQL) don't need it.
_connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(settings.database_url, connect_args=_connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class every ORM model inherits from."""


def get_db():
    """FastAPI dependency: yields a DB session, always closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables that don't exist yet. Safe to call on every startup."""
    from app.models import conversation, document # noqa: F401  (registers the models)

    Base.metadata.create_all(bind=engine)