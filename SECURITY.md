# Security Policy

## Supported Versions

Security fixes are released for the latest version and backported to the most
recent minor version where feasible.

| Version | Supported |
|---------|-----------|
| 0.5.x   | ✅ |
| < 0.5   | ❌ |

## Reporting a Vulnerability

We take security issues seriously. Please **do not** open a public issue for a
security vulnerability.

**Email**: hugo.bacard@ijclab.in2p3.fr

Please include:

- The affected version(s) (`everse-scan --version`)
- A description of the vulnerability and its impact
- Steps to reproduce, or a minimal proof of concept
- Any suggested fix, if you have one

You should receive an acknowledgement within 5 business days. We will coordinate
a fix and a disclosure timeline once the issue is confirmed.

## Security practices

- **Secret scanning**: gitleaks is configured in the pre-commit hooks
  (`.pre-commit-config.yaml`) and runs on every commit.
- **Dependency updates**: Dependabot keeps dependencies up to date
  (`.github/dependabot.yml`).
- **Code review**: all changes go through pull requests with reviewers assigned
  via `.github/CODEOWNERS`.
- **Responsible disclosure**: this policy, and the coordinate-fix-then-disclose
  workflow, is our primary channel for reports.
