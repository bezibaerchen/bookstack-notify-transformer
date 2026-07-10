# Contributing to bookstack-notify-transformer

Thank you for your interest in contributing to `bookstack-notify-transformer`.

Contributions are welcome, including bug reports, documentation improvements, feature suggestions, tests, and code changes.

## Before You Start

Before opening a pull request:

1. Check whether a related issue already exists.
2. For larger changes, open an issue first and describe the proposed solution.
3. Keep changes focused on a single problem or feature.
4. Do not include secrets, passwords, tokens, internal URLs, or personal data.

## Reporting Bugs

Please use the bug report template and include:

- The application version or Docker image tag
- The BookStack version, if relevant
- The deployment method
- Relevant configuration with secrets removed
- Steps to reproduce the problem
- Expected and actual behavior
- Relevant log output

Please format logs and configuration as code blocks.

## Suggesting Features

Feature requests are welcome.

Please describe:

- The problem you are trying to solve
- The proposed behavior
- An example use case
- Possible alternatives
- Whether the change affects existing configurations

## Development Setup

Clone the repository:

```bash
git clone https://github.com/bezibaerchen/bookstack-notify-transformer.git
cd bookstack-notify-transformer
```

Create a local environment file:

```bash
cp .env.example .env
```

Review the values in `.env` before starting the application.

Build and start the container:

```bash
docker compose up --build
```

To run it in the background:

```bash
docker compose up --build -d
```

To inspect the logs:

```bash
docker compose logs -f
```

To stop the environment:

```bash
docker compose down
```

## Code Guidelines

Please follow these guidelines:

- Keep the implementation simple and focused.
- Avoid introducing unnecessary dependencies.
- Use clear names for functions, variables, and configuration options.
- Add comments only where the behavior is not self-explanatory.
- Handle invalid input gracefully.
- Do not expose secrets or complete webhook payloads in logs.
- Preserve backward compatibility where reasonably possible.

## Documentation

Update the documentation when your change introduces or modifies:

- Environment variables
- Webhook endpoints
- Supported BookStack events
- Apprise configuration
- Docker configuration
- Notification formatting
- Security-related behavior

New environment variables should also be added to `.env.example`.

## Commits

Use concise and descriptive commit messages.

Examples:

```text
Fix handling of missing webhook fields
Add support for page update events
Update Docker Compose example
Improve validation of Apprise URLs
```

## Pull Requests

A pull request should:

- Describe what was changed
- Explain why the change is needed
- Reference related issues
- Mention any breaking changes
- Include testing information
- Update documentation where necessary

Maintainers may request changes before merging.

## Security Issues

Do not report security vulnerabilities in a public issue.

Please follow the instructions in [SECURITY.md](SECURITY.md).

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.
