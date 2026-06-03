from __future__ import annotations

import os
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("VENDOR_HUB_HOST", "0.0.0.0")
    port: int = int(os.getenv("VENDOR_HUB_PORT", "8000"))
    secret_key: str = os.getenv("VENDOR_HUB_SECRET_KEY", "course-studio-dev-secret")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://coursestudio:coursestudio@127.0.0.1:5432/coursestudio",
    )
    seed_data: bool = os.getenv("VENDOR_HUB_SEED_DATA", "1") != "0"
    testing: bool = False


def build_settings(overrides: dict | None = None) -> Settings:
    settings = Settings()
    if overrides:
        settings = replace(settings, **overrides)
    return settings
