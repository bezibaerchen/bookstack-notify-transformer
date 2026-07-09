"""
Application entry point.
"""

from bookstack_notify_transformer.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
