---
title: everse-scan API reference
---

# everse-scan — API reference

This document covers the command-line interface and the programmatic use of the
`everse_scan` Python package. It complements the usage guide in the
[README](../README.md#usage).

## 1. Command-line interface (CLI)

Installed binary: `everse-scan`.

```
usage: everse-scan [-h] [--format {json,markdown,both}] [-o PREFIX]
                   [--role {default,researcher,rse}] [--save BASELINE]
                   [--diff BASELINE] [--use [INTEGRATIONS ...]] [--version]
                   TARGET
```

### Positional argument

| Argument | Description |
|---|---|
| `TARGET` | Path to a local repository or a GitHub/GitLab URL (`https://github.com/org/repo`, `https://gitlab.example.org/group/repo`) |

### Options

| Option | Description |
|---|---|
| `--format {json,markdown,both}` | Output format (default: `markdown`) |
| `-o, --output PREFIX` | Write output to `PREFIX.json` / `PREFIX.md` instead of stdout |
| `--role {default,researcher,rse}` | Adapt the report to a target role |
| `--save BASELINE` | Save the scan result as a JSON baseline for later diffing |
| `--diff BASELINE` | Re-scan and compare against a previous baseline |
| `--use [INTEGRATIONS ...]` | Enable FAIR integrations: `howfairis`, `cffconvert`, `codemeta` (no args → all) |
| `--version` | Show the version and exit |
| `-h, --help` | Show help and exit |

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Scan completed successfully |

### Examples

```bash
# Markdown report for a local repo
everse-scan ./my-repo

# GitHub repository scan, JSON output to file
everse-scan https://github.com/org/repo --format json -o scan

# GitLab repository scan (self-hosted, e.g. gitlab.in2p3.fr)
everse-scan https://gitlab.in2p3.fr/sens/CLASS --format markdown -o scan

# RSE-adapted report with all FAIR integrations
everse-scan ./my-repo --role rse --use

# Baselines for progress tracking
everse-scan ./my-repo --save baseline.json --format json
everse-scan ./my-repo --diff baseline.json
```

## 2. Python API

The package exposes a small programmatic surface through `everse_scan`.

### `everse_scan.scanner.scan_repo(repo_path, ...)`

Result of a full scan: `ScanResult` (see below).

```python
from everse_scan.scanner import scan_repo

result = scan_repo("./my-repo")
print(result.checks)  # list[CheckResult]
print(result.overall)  # aggregate status
```

### Data models (`everse_scan.models`)

- `CheckStatus` — enum: `PASS`, `WARN`, `FAIL`, `NA`.
- `CheckResult` — one check's outcome: `name`, `status`, `message`,
  `details`, `recommendations`, `rsqkit_url`, `category`.
- `ScanResult` — full report: checks list, context (tier, lifecycle, funder),
  and aggregate status.

### Reporters (`everse_scan.reporters`)

- `markdown.generate_markdown(result) -> str`
- `json.generate_json(result) -> str`
- `adaptive.generate_adaptive_markdown(result, role) -> str`
- `diff.compute_diff(baseline, current) -> DiffResult`,
  `diff.generate_diff_markdown(baseline, current) -> str`,
  `diff.save_baseline(result, path)`, `diff.load_baseline(path)`
- `funder.generate_funder_section(result, funder) -> str`

### Checks (`everse_scan.checks`)

Each check module exposes `check_<name>(repo_path) -> CheckResult`
(e.g. `from everse_scan.checks.cicd import check_cicd`). `extended.py` contains
the 19 extended checks.

## 3. Configuration

Runtime configuration is read from standard files:

- `pyproject.toml` — package metadata, `ruff`, `pytest`, `hatchling` settings
- `.editorconfig` — editor conventions
- `.pre-commit-config.yaml` — pre-commit hooks (incl. gitleaks)
- `.github/dependabot.yml` — dependency updates
- `.zenodo.json` — Zenodo deposition metadata

There is no runtime config file for the scan itself; behaviour is controlled by
the CLI options above.
