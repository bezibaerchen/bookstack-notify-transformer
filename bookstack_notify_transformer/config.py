"""
Application configuration.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    bookstack_url: str
    bookstack_token_id: str
    bookstack_token_secret: str

    apprise_url: str

    log_level: str

    request_timeout: int = 10


config = Config(
    bookstack_url=os.getenv("BOOKSTACK_URL", "").rstrip("/"),
    bookstack_token_id=os.getenv("BOOKSTACK_TOKEN_ID", "").strip(),
    bookstack_token_secret=os.getenv("BOOKSTACK_TOKEN_SECRET", "").strip(),

    apprise_url=os.getenv("APPRISE_URL", "").strip(),

    log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
)
