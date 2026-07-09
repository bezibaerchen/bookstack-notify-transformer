"""
Notification formatting.
"""

from typing import Any

from .bookstack import build_page_url, enrich_comment_event
from .utils import find_first, get_nested, strip_html


EVENT_TITLES = {
    "comment_create": "💬 New comment in BookStack",

    "page_create": "📄 New BookStack page created",
    "page_update": "✏️ BookStack page updated",
    "page_delete": "🗑️ BookStack page deleted",

    "chapter_create": "📁 New BookStack chapter created",
    "chapter_update": "✏️ BookStack chapter updated",
    "chapter_delete": "🗑️ BookStack chapter deleted",

    "book_create": "📚 New BookStack book created",
    "book_update": "✏️ BookStack book updated",
    "book_delete": "🗑️ BookStack book deleted",
}


def find_item_name(payload: dict[str, Any]) -> str:
    return (
        find_first(
            payload,
            [
                "related_item.name",
                "page.name",
                "book.name",
                "chapter.name",
                "entity.name",
                "name",
            ],
        )
        or "Unknown"
    )


def find_url(payload: dict[str, Any]) -> str:
    return find_first(
        payload,
        [
            "url",
            "related_item.url",
            "page.url",
            "book.url",
            "chapter.url",
            "entity.url",
        ],
    )


def find_comment_text(payload: dict[str, Any]) -> str:
    return find_first(
        payload,
        [
            "comment.html",
            "comment.text",
            "comment.content",
            "related_item.html",
            "related_item.text",
            "related_item.content",
        ],
    )


def build_message(payload: dict[str, Any]) -> tuple[str, str]:
    event = payload.get("event", "unknown_event")
    title = EVENT_TITLES.get(event, "📚 BookStack notification")

    enrichment = enrich_comment_event(payload)
    page_from_api = enrichment.get("page", {})
    comment_from_api = enrichment.get("comment", {})

    if event == "comment_create" and page_from_api:
        item_name = page_from_api.get("name", "Unknown")
        url = build_page_url(page_from_api)
    else:
        item_name = find_item_name(payload)
        url = find_url(payload)

    user_name = get_nested(payload, "triggered_by.name", "Unknown")
    summary = get_nested(payload, "related_item.current_revision.summary", "")

    comment = (
        comment_from_api.get("html")
        or comment_from_api.get("text")
        or comment_from_api.get("content")
        or find_comment_text(payload)
    )
    comment = strip_html(comment)

    if event == "comment_create":
        body = (
            f'A new comment was created for page "{item_name}".\n\n'
            f"Commented by: {user_name}"
        )

        if comment:
            body += f"\n\nComment:\n{comment}"

    elif event == "page_create":
        body = f'Page "{item_name}" was created.\n\nCreated by: {user_name}'

    elif event == "page_update":
        body = f'Page "{item_name}" was updated.\n\nUpdated by: {user_name}'

        if summary:
            body += f"\n\nRevision summary:\n{summary}"

    elif event == "page_delete":
        body = f'Page "{item_name}" was deleted.\n\nDeleted by: {user_name}'

    elif event == "chapter_create":
        body = f'Chapter "{item_name}" was created.\n\nCreated by: {user_name}'

    elif event == "chapter_update":
        body = f'Chapter "{item_name}" was updated.\n\nUpdated by: {user_name}'

        if summary:
            body += f"\n\nRevision summary:\n{summary}"

    elif event == "chapter_delete":
        body = f'Chapter "{item_name}" was deleted.\n\nDeleted by: {user_name}'

    elif event == "book_create":
        body = f'Book "{item_name}" was created.\n\nCreated by: {user_name}'

    elif event == "book_update":
        body = f'Book "{item_name}" was updated.\n\nUpdated by: {user_name}'

        if summary:
            body += f"\n\nRevision summary:\n{summary}"

    elif event == "book_delete":
        body = f'Book "{item_name}" was deleted.\n\nDeleted by: {user_name}'

    else:
        body = (
            f"BookStack event: {event}\n\n"
            f"Item: {item_name}\n\n"
            f"User: {user_name}"
        )

    if url:
        body += f"\n\nOpen page:\n{url}"

    return title, body
