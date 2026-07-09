# BookStack Notify Transformer

> Transform BookStack webhooks into rich Apprise notifications by enriching events via the BookStack REST API.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/github/license/bezibaerchen/bookstack-notify-transformer)
![GitHub last commit](https://img.shields.io/github/last-commit/bezibaerchen/bookstack-notify-transformer)

---

## Why?

BookStack provides webhooks for many events, but some webhook payloads intentionally contain only minimal information.

For example, the `comment_create` webhook contains only IDs and metadata, but not:

- the page title
- the page URL
- the actual comment text

This project automatically enriches incoming webhook events by querying the BookStack REST API before forwarding a clean, human-friendly notification to an Apprise API endpoint.

The result is rich notifications that are immediately useful without requiring additional scripting.

---

## Features

- Supports BookStack webhooks
- Automatic REST API enrichment
- Rich notifications via Apprise
- Docker ready
- Lightweight Flask application
- Health endpoint
- Clean Python package structure
- Easy to extend for additional webhook events

---

## Architecture

```
                BookStack
                    │
             Webhook Event
                    │
                    ▼
      BookStack Notify Transformer
                    │
      Enrich via REST API
                    │
                    ▼
               Apprise API
                    │
      ┌─────────────┼─────────────┐
      │             │             │
    Email       Telegram      Discord
      │         Teams         Slack
      └────────── ... 100+ services ...
```

---

## Supported Events

| Event | Status |
|--------|--------|
| comment_create | ✅ |
| page_create | 🚧 |
| page_update | 🚧 |
| page_delete | 🚧 |
| chapter_create | 🚧 |
| chapter_update | 🚧 |
| chapter_delete | 🚧 |
| book_create | 🚧 |
| book_update | 🚧 |
| book_delete | 🚧 |

The initial focus of this project is `comment_create`, since BookStack's webhook payload for comments does not contain the information typically needed for useful notifications.

Additional events will be improved over time.

---

# Quick Start

## Docker Compose

```yaml
services:
  bookstack-notify-transformer:
    image: ghcr.io/bezibaerchen/bookstack-notify-transformer:latest
    restart: unless-stopped

    env_file:
      - .env

    ports:
      - "8080:8080"
```

---

## Environment Variables

| Variable | Description |
|-----------|-------------|
| BOOKSTACK_URL | Base URL of your BookStack instance |
| BOOKSTACK_TOKEN_ID | API Token ID |
| BOOKSTACK_TOKEN_SECRET | API Token Secret |
| APPRISE_URL | Apprise API endpoint |
| LOG_LEVEL | Logging level (default: INFO) |

Example:

```env
BOOKSTACK_URL=https://bookstack.example.com

BOOKSTACK_TOKEN_ID=xxxxxxxxxxxxxxxx

BOOKSTACK_TOKEN_SECRET=xxxxxxxxxxxxxxxx

APPRISE_URL=https://apprise.example.com/notify/bookstack

LOG_LEVEL=INFO
```

---

# BookStack Configuration

Create a new webhook in BookStack.

Example:

```
Webhook URL

http://bookstack-notify-transformer:8080/bookstack
```

Recommended events:

- comment_create

Additional events can also be enabled.

---

# Apprise Configuration

Example:

```yaml
version: 1

urls:
  - mailto://smtp.example.com:25/?from=bookstack@example.com&to=admin@example.com
```

---

# API

## Health

```
GET /health
```

Response

```json
{
  "ok": true,
  "service": "bookstack-notify-transformer",
  "version": "1.0.0"
}
```

---

## Root

```
GET /
```

Returns service information.

---

# Development

Clone the repository

```bash
git clone https://github.com/bezibaerchen/bookstack-notify-transformer.git

cd bookstack-notify-transformer
```

Create a virtual environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run locally

```bash
python app.py
```

Run tests

```bash
pytest
```

---

# Roadmap

- Better support for page events
- Better support for chapter events
- Better support for book events
- Notification templates
- Multiple notification formats
- Additional notification providers
- Unit tests
- GitHub Container Registry
- Automatic Docker image publishing

---

# Contributing

Issues, ideas and pull requests are always welcome.

If you have improvements or additional webhook support, feel free to contribute.

---

# License

MIT License
