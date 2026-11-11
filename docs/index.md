# everse-scan documentation

Welcome to the documentation for **everse-scan**, a command-line tool that analyzes
research software repositories and produces a structured report on software quality
and FAIR compliance based on EVERSE/RSQKit best practices.

The [README](../README.md) is the primary reference: it covers installation, usage,
options, FAIR integrations, and the full list of checks. This page summarizes the
essentials and points to the rest.

## Overview

`everse-scan` runs 36 deterministic checks covering 35+ RSQKit tasks (README,
LICENSE, CITATION.cff, codemeta.json, tests, CI/CD, security, and more). It detects
the repository's language, software tier, lifecycle stage, and funder, and produces
a prioritized action plan.

## Quick start

```bash
uv pip install -e ".[dev]"
everse-scan ./my-repo
```

Scan a remote GitHub repository:

```bash
everse-scan https://github.com/org/repo
```

## Common workflows

- Markdown report to stdout (default): `everse-scan ./my-repo`
- JSON output: `everse-scan ./my-repo --format json`
- Track progress between fixes: `everse-scan ./my-repo --save baseline.json` then
  `everse-scan ./my-repo --diff baseline.json`
- Enable FAIR integrations: `everse-scan ./my-repo --use`

See the [README](../README.md) for the full options reference and examples.

## Architecture

```
src/everse_scan/
├── cli.py              # CLI entry point
├── scanner.py          # Scan orchestration
├── models.py           # CheckResult, ScanResult, CheckStatus
├── priorities.py       # 2D prioritization (effort x impact)
├── checks/             # 17 core + 19 extended checks
├── reporters/          # JSON, Markdown, Adaptive, Diff, Funder
├── integrations/       # howfairis, cffconvert, codemeta
├── knowledge/          # RSQKit tasks, funder profiles
├── languages/          # Multi-language detection
└── context/            # Tier, Lifecycle, Funder detection
```

## Development

```bash
uv pip install -e ".[dev]"
python3 -m pytest tests/ -v
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) if present, and the repository
[README](../README.md) for project conventions.
