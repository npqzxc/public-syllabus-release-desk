from __future__ import annotations

import hashlib
from functools import wraps

from flask import g, redirect, request, session, url_for

from .models import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate_user(db_session, username: str, password: str) -> User | None:
    user = db_session.query(User).filter(User.username == username).one_or_none()
    if user is None or user.password_hash != hash_password(password):
        return None
    return user


def login_user(user: User) -> None:
    session["user_id"] = user.id


def logout_user() -> None:
    session.pop("user_id", None)
    session.pop("after_login", None)


def attach_current_user() -> None:
    user_id = session.get("user_id")
    if user_id is None:
        g.current_user = None
        return
    g.current_user = g.db.get(User, user_id)


def require_login(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if getattr(g, "current_user", None) is None:
            destination = request.full_path if request.query_string else request.path
            session["after_login"] = destination.rstrip("?")
            return redirect(url_for("web.login_view"))
        return view_func(*args, **kwargs)

    return wrapper
