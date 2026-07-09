"""
Notification delivery.
"""

import requests

from .config import config


class NotificationError(Exception):
    """Raised when a notification could not be delivered."""


class AppriseNotifier:
    """Send notifications to an Apprise API endpoint."""

    def __init__(self):
        self.session = requests.Session()

    def send(self, title: str, body: str) -> requests.Response:
        if not config.apprise_url:
            raise NotificationError("APPRISE_URL is not configured.")

        response = self.session.post(
            config.apprise_url,
            json={
                "title": title,
                "body": body,
            },
            timeout=config.request_timeout,
        )

        response.raise_for_status()

        return response


notifier = AppriseNotifier()
