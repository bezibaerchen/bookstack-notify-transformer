# BookStack Notify Transformer

> Transform BookStack webhooks into rich Apprise notifications by enriching events through the BookStack REST API.

[![CI and Docker](https://github.com/bezibaerchen/bookstack-notify-transformer/actions/workflows/docker.yml/badge.svg)](https://github.com/bezibaerchen/bookstack-notify-transformer/actions/workflows/docker.yml)
[![Latest Release](https://img.shields.io/github/v/release/bezibaerchen/bookstack-notify-transformer)](https://github.com/bezibaerchen/bookstack-notify-transformer/releases)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://github.com/bezibaerchen/bookstack-notify-transformer/pkgs/container/bookstack-notify-transformer)
[![License](https://img.shields.io/github/license/bezibaerchen/bookstack-notify-transformer)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/bezibaerchen/bookstack-notify-transformer)](https://github.com/bezibaerchen/bookstack-notify-transformer/commits/main)

---

## Why?

BookStack provides webhooks for many events, but some webhook payloads intentionally contain only minimal information.

For example, the `comment_create` webhook contains IDs and metadata, but not necessarily all information required for a useful notification, such as:

- the page title
- the page URL
- the actual comment text

BookStack Notify Transformer receives the webhook, retrieves additional information from the BookStack REST API and forwards a clean, human-friendly notification to an Apprise API endpoint.

This makes webhook notifications immediately useful without requiring additional scripts or custom automation.

---

## Features

- BookStack webhook receiver
- Automatic enrichment through the BookStack REST API
- Rich notifications through Apprise
- Support for email, Telegram, Discord, Microsoft Teams, Slack and many other services
- Lightweight Flask application
- Docker and Docker Compose support
- Health-check endpoint
- Structured Python package
- Automated tests
- Automated container builds through GitHub Actions
- Published container images through GitHub Container Registry
- Easy to extend for additional webhook events

---

## Architecture

```text
                BookStack
                    │
             Webhook event
                    │
                    ▼
      BookStack Notify Transformer
                    │
        BookStack REST API lookup
                    │
                    ▼
               Apprise API
                    │
      ┌─────────────┼─────────────┐
      │             │             │
    Email       Telegram       Discord
                  Teams          Slack
      └────────── many other services ──────────┘
```

---

## Supported Events

| Event | Status |
|---|---|
| `comment_create` | ✅ Supported |
| `page_create` | 🚧 Planned |
| `page_update` | 🚧 Planned |
| `page_delete` | 🚧 Planned |
| `chapter_create` | 🚧 Planned |
| `chapter_update` | 🚧 Planned |
| `chapter_delete` | 🚧 Planned |
| `book_create` | 🚧 Planned |
| `book_update` | 🚧 Planned |
| `book_delete` | 🚧 Planned |

The initial focus is `comment_create`, because comment webhook payloads do not contain all information typically required for a useful notification.

Support for additional events will be expanded over time.

---

## Quick Start

### Docker Compose

Create a `docker-compose.yml` file:

```yaml
services:
  bookstack-notify-transformer:
    image: ghcr.io/bezibaerchen/bookstack-notify-transformer:latest
    container_name: bookstack-notify-transformer
    restart: unless-stopped

    env_file:
      - .env

    ports:
      - "8080:8080"
```

Create a `.env` file:

```env
BOOKSTACK_URL=https://bookstack.example.com
BOOKSTACK_TOKEN_ID=xxxxxxxxxxxxxxxx
BOOKSTACK_TOKEN_SECRET=xxxxxxxxxxxxxxxx
APPRISE_URL=https://apprise.example.com/notify/bookstack
LOG_LEVEL=INFO
```

Start the container:

```bash
docker compose up -d
```

Check its status:

```bash
docker compose ps
```

View the logs:

```bash
docker compose logs -f
```

Test the health endpoint:

```bash
curl http://localhost:8080/health
```

To stop the service:

```bash
docker compose down
```

---

## Container Images

Container images are published to the GitHub Container Registry:

```text
ghcr.io/bezibaerchen/bookstack-notify-transformer
```

Use the latest published image:

```yaml
image: ghcr.io/bezibaerchen/bookstack-notify-transformer:latest
```

For production deployments, pinning the image to a specific release tag is recommended:

```yaml
image: ghcr.io/bezibaerchen/bookstack-notify-transformer:0.1.1
```

Available packages and versions can be found in the repository's GitHub Packages section.

---

## Environment Variables

| Variable | Required | Description |
|---|---:|---|
| `BOOKSTACK_URL` | Yes | Base URL of the BookStack instance |
| `BOOKSTACK_TOKEN_ID` | Yes | BookStack API token ID |
| `BOOKSTACK_TOKEN_SECRET` | Yes | BookStack API token secret |
| `APPRISE_URL` | Yes | Apprise API notification endpoint |
| `LOG_LEVEL` | No | Logging level, defaults to `INFO` |

Example:

```env
BOOKSTACK_URL=https://bookstack.example.com
BOOKSTACK_TOKEN_ID=xxxxxxxxxxxxxxxx
BOOKSTACK_TOKEN_SECRET=xxxxxxxxxxxxxxxx
APPRISE_URL=https://apprise.example.com/notify/bookstack
LOG_LEVEL=INFO
```

Do not commit your `.env` file or expose API tokens, webhook secrets or internal URLs in public issues and logs.

---

## BookStack Configuration

Create a new webhook in BookStack and point it to the transformer endpoint.

Example when both services use the same Docker network:

```text
http://bookstack-notify-transformer:8080/bookstack
```

Example through a reverse proxy:

```text
https://notify-transformer.example.com/bookstack
```

Enable the following event:

```text
comment_create
```

Additional BookStack events may be enabled, but only events listed as supported are guaranteed to produce fully enriched notifications.

The transformer must be reachable from the BookStack instance. Avoid exposing it directly to the public internet unless required. Prefer a reverse proxy with HTTPS and appropriate access restrictions.

---

## Apprise Configuration

The transformer sends notifications to an existing Apprise API endpoint.

Example Apprise configuration:

```yaml
version: 1

urls:
  - mailto://smtp.example.com:25/?from=bookstack@example.com&to=admin@example.com
```

Apprise can forward notifications to email, Telegram, Discord, Microsoft Teams, Slack and many other supported services.

---

## API Endpoints

### Webhook Endpoint

```http
POST /bookstack
```

Receives webhook events from BookStack.

### Health Endpoint

```http
GET /health
```

Example response:

```json
{
  "ok": true,
  "service": "bookstack-notify-transformer",
  "version": "0.1.1"
}
```

### Service Information

```http
GET /
```

Returns basic information about the running service.

---

## Development

Clone the repository:

```bash
git clone https://github.com/bezibaerchen/bookstack-notify-transformer.git
cd bookstack-notify-transformer
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the application locally:

```bash
python app.py
```

Run the test suite:

```bash
pytest
```

Build the container locally:

```bash
docker build -t bookstack-notify-transformer:local .
```

Run the local container:

```bash
docker run --rm \
  --env-file .env \
  -p 8080:8080 \
  bookstack-notify-transformer:local
```

---

## Roadmap

Planned improvements include:

- Enriched page event notifications
- Enriched chapter event notifications
- Enriched book event notifications
- Customizable notification templates
- Multiple notification formats
- Improved validation and error handling
- Additional automated tests
- More configuration examples
- Support for further BookStack webhook events

Feature requests and contributions are welcome.

---

## Contributing

Issues, ideas and pull requests are welcome.

Before contributing, please read the [contributing guidelines](CONTRIBUTING.md).

For larger changes, consider opening an issue first so the proposed implementation can be discussed.

---

## Security

Do not report security vulnerabilities through public GitHub issues.

Please follow the instructions in the [security policy](SECURITY.md) and use GitHub's private vulnerability reporting feature.

---

## Code of Conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

This project is licensed under the [MIT License](LICENSE).
