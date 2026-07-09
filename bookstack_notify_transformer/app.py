"""
Flask application.
"""

import json
import logging

from flask import Flask, jsonify, request
from requests.exceptions import HTTPError, RequestException

from . import __version__
from .config import config
from .formatter import build_message
from .notifier import NotificationError, notifier


def create_app() -> Flask:
    """Create the Flask application."""

    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "bookstack-notify-transformer",
                "version": __version__,
                "status": "ok",
                "endpoints": {
                    "webhook": "/bookstack",
                    "health": "/health",
                },
            }
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "ok": True,
                "service": "bookstack-notify-transformer",
                "version": __version__,
            }
        )

    @app.post("/bookstack")
    def bookstack():

        payload = request.get_json(force=True, silent=True) or {}

        app.logger.info(
            "Received BookStack webhook:\n%s",
            json.dumps(payload, indent=2, ensure_ascii=False),
        )

        try:
            title, body = build_message(payload)

            response = notifier.send(title, body)

            app.logger.info(
                "Successfully processed event '%s'",
                payload.get("event", "unknown"),
            )

            return (
                jsonify(
                    {
                        "ok": True,
                        "event": payload.get("event"),
                        "title": title,
                        "status_code": response.status_code,
                    }
                ),
                response.status_code,
            )

        except NotificationError as exc:
            app.logger.error(str(exc))

            return (
                jsonify(
                    {
                        "ok": False,
                        "error": str(exc),
                    }
                ),
                500,
            )

        except HTTPError as exc:
            app.logger.exception("Remote service returned an error.")

            return (
                jsonify(
                    {
                        "ok": False,
                        "error": str(exc),
                    }
                ),
                502,
            )

        except RequestException as exc:
            app.logger.exception("Network error while processing webhook.")

            return (
                jsonify(
                    {
                        "ok": False,
                        "error": str(exc),
                    }
                ),
                502,
            )

        except Exception:
            app.logger.exception("Unhandled exception while processing webhook.")

            return (
                jsonify(
                    {
                        "ok": False,
                        "error": "Internal server error",
                    }
                ),
                500,
            )

    return app


app = create_app()
