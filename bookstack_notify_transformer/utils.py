"""
General helper functions.
"""

import re
from html import unescape
from typing import Any


def get_nested(data: dict[str, Any], path: str, default: Any = "") -> Any:
    current: Any = data

    for key in path.split("."):
        if not isinstance(current, dict):
            return default

        current = current.get(key)

        if current is None:
            return default

    return current


def find_first(data: dict[str, Any], paths: list[str]) -> str:
    for path in paths:
        value = get_nested(data, path, "")
        if value:
            return str(value)

    return ""


def strip_html(value: Any) -> str:
    if not value:
        return ""

    text = str(value).strip()

    text = text.replace("<br>", "\n")
    text = text.replace("<br/>", "\n")
    text = text.replace("<br />", "\n")

    text = re.sub(r"</p>\s*<p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)

    return unescape(text).strip()
