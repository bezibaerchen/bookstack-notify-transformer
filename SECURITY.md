# Security Policy

## Supported Versions

Security fixes are generally provided for the latest released version of `bookstack-notify-transformer`.

| Version | Supported |
|---|---|
| Latest release | Yes |
| Older releases | No |
| Development versions | Best effort |

Users are encouraged to use a specific released version instead of an unversioned development build.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.

Use GitHub's private vulnerability reporting feature:

1. Open the repository's **Security** tab.
2. Select **Advisories**.
3. Select **Report a vulnerability**.
4. Provide the requested information.

Please include:

- A description of the vulnerability
- Affected versions
- Steps to reproduce the issue
- Potential impact
- Relevant logs or configuration with secrets removed
- A suggested fix, if available

## Sensitive Information

Do not include any of the following unless strictly necessary:

- Passwords
- API tokens
- Webhook secrets
- SMTP credentials
- Internal hostnames
- Private IP addresses
- Personal data
- Complete production configuration files

Replace sensitive values with placeholders.

## Response Process

The maintainer will attempt to:

1. Confirm receipt of the report.
2. Review and reproduce the issue.
3. Determine the severity and affected versions.
4. Prepare a fix where necessary.
5. Publish a new release.
6. Disclose the vulnerability after a fix is available.

Response times cannot be guaranteed, as this is a community-maintained project.

## Security Recommendations

Users are responsible for securely operating their deployment.

Recommended precautions include:

- Do not expose the service directly to the public internet unless necessary.
- Use a reverse proxy with HTTPS.
- Restrict access to the webhook endpoint where possible.
- Store secrets outside the repository.
- Use strong and unique credentials.
- Keep the Docker host and container images updated.
- Review logs before sharing them publicly.
- Pin production deployments to a released image tag.
