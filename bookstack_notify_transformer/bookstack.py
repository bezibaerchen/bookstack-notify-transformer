"""
BookStack API helper functions.
"""

from typing import Any

import requests

from .config import config
from .utils import get_nested


class BookStackClient:
    """Simple client for the BookStack REST API."""

    def __init__(self):
        self.session = requests.Session()

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": (
                f"Token {config.bookstack_token_id}:"
                f"{config.bookstack_token_secret}"
            ),
            "Accept": "application/json",
        }

    def get(self, path: str) -> dict[str, Any]:
        if (
            not config.bookstack_url
            or not config.bookstack_token_id
            or not config.bookstack_token_secret
        ):
            raise RuntimeError("BookStack API configuration is incomplete.")

        response = self.session.get(
            f"{config.bookstack_url}{path}",
            headers=self.headers,
            timeout=config.request_timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_page(self, page_id: int | str) -> dict[str, Any]:
        return self.get(f"/api/pages/{page_id}")

    def get_comment(self, comment_id: int | str) -> dict[str, Any]:
        return self.get(f"/api/comments/{comment_id}")

    def get_book(self, book_id: int | str) -> dict[str, Any]:
        return self.get(f"/api/books/{book_id}")


client = BookStackClient()


def build_page_url(page: dict[str, Any]) -> str:
    """Return the public BookStack URL for a page."""

    direct = (
        page.get("url")
        or page.get("html_url")
        or page.get("link")
    )

    if direct:
        return str(direct)

    page_slug = page.get("slug")
    book_slug = (
        get_nested(page, "book.slug")
        or page.get("book_slug")
    )

    if not book_slug:
        book_id = page.get("book_id") or get_nested(page, "book.id")

        if book_id:
            book = client.get_book(book_id)
            book_slug = book.get("slug")

    if config.bookstack_url and page_slug and book_slug:
        return (
            f"{config.bookstack_url}"
            f"/books/{book_slug}"
            f"/page/{page_slug}"
        )

    return ""


def enrich_comment_event(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Resolve additional data for BookStack comment events.
    """

    if payload.get("event") != "comment_create":
        return {}

    related = payload.get("related_item", {})

    enrichment: dict[str, Any] = {}

    if (
        related.get("commentable_type") == "page"
        and related.get("commentable_id")
    ):
        enrichment["page"] = client.get_page(
            related["commentable_id"]
        )

    if related.get("id"):
        enrichment["comment"] = client.get_comment(
            related["id"]
        )

    return enrichment
