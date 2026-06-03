from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from .config import build_settings


class Base(DeclarativeBase):
    pass


def _engine_options(database_url: str) -> dict:
    if database_url.startswith("sqlite"):
        options = {"connect_args": {"check_same_thread": False}}
        if ":memory:" in database_url:
            options["poolclass"] = StaticPool
        return options
    return {}


settings = build_settings()
engine = create_engine(settings.database_url, future=True, **_engine_options(settings.database_url))
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, expire_on_commit=False))


def reset_engine(database_url: str) -> None:
    global engine
    SessionLocal.remove()
    try:
        engine.dispose()
    except Exception:
        pass
    engine = create_engine(database_url, future=True, **_engine_options(database_url))
    SessionLocal.configure(bind=engine)


def init_db() -> None:
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()


def shutdown_session(exception=None) -> None:
    SessionLocal.remove()


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
