from __future__ import annotations

import tempfile

from app.server import create_app


def build_test_app():
    temp_dir = tempfile.TemporaryDirectory()
    app = create_app(
        {
            "database_url": f"sqlite:///{temp_dir.name}/coursestudio.sqlite3",
            "testing": True,
            "seed_data": True,
            "secret_key": "test-secret",
        }
    )
    return temp_dir, app
