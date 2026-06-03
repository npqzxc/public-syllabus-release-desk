from __future__ import annotations

from flask import Flask, g

from .auth import attach_current_user
from .config import build_settings
from .db import get_session, init_db, reset_engine, shutdown_session
from .routes.api import api_bp
from .routes.web import web_bp
from .seed import ensure_seed_data


def create_app(overrides: dict | None = None) -> Flask:
    settings = build_settings(overrides)
    reset_engine(settings.database_url)
    init_db()
    if settings.seed_data:
        ensure_seed_data()

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.update(
        SECRET_KEY=settings.secret_key,
        TESTING=settings.testing,
    )

    @app.before_request
    def _bind_session():
        g.db = get_session()
        attach_current_user()

    @app.teardown_appcontext
    def _remove_session(exception=None):
        shutdown_session(exception)

    @app.context_processor
    def inject_user():
        return {"current_user": getattr(g, "current_user", None)}

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    return app


def main() -> None:
    settings = build_settings()
    app = create_app()
    app.run(host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
