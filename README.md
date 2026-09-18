# everse-scan

Scan your research software repository and get a structured quality and FAIR compliance report based on EVERSE/RSQKit best practices.

## Badges

![Version](https://img.shields.io/badge/version-0.5.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-99%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

## What is everse-scan?

`everse-scan` is a command-line tool that analyzes research software repositories and generates a structured report on software quality and FAIR compliance. It checks your project against 36 best-practice checks derived from the [RSQKit](https://everse.software/RSQKit/) catalogue maintained by the [EVERSE](https://everse.software/) research software engineering community.

**Who is it for?**

- **Researchers who write code** — make sure your project is citable, reproducible, and follows good practices before publication.
- **Research Software Engineers (RSEs)** — get a quick audit of a repository's engineering quality, CI/CD, testing, and documentation.
- **Funded projects** — check alignment with funder requirements (Horizon Europe, NSF, Wellcome, DFG, ANR, UKRI, Helmholtz).

`everse-scan` is a standalone CLI tool. It does not require an AI assistant to run — it produces deterministic, reproducible reports. But it works great alongside one (see [Using with AI assistants](#using-with-ai-assistants)).

## Key features

- **36 deterministic checks** covering 35+ RSQKit tasks (README, LICENSE, CITATION.cff, codemeta.json, tests, CI/CD, security, and more)
- **7 optional FAIR integrations** via `--use` (howfairis, cffconvert, codemeta validator)
- **Funder compliance detection** — automatically detects your funder and checks alignment with its requirements
- **Adaptive reporting** — switch between `researcher` and `rse` views with `--role`
- **Re-scan with diff** — track progress between scans with `--save` and `--diff`
- **2D prioritization** — action plan sorted by effort x impact, factoring in tier, lifecycle, and role
- **Multi-language detection** — Python, R, C++, Julia, JS/TS, Rust, Go, Java, Ruby
- **Tier & lifecycle awareness** — adapts checks to whether your project is a script, a tool/library, or infrastructure
- **JSON + Markdown output** — machine-readable and human-readable formats

## Quick start

```bash
pip install -e .
everse-scan ./my-repo
```

Or with `uv`:

```bash
uv pip install -e ".[dev]"
everse-scan ./my-repo
```

## Usage

### Basic scan

```bash
# Markdown report to stdout (default)
everse-scan ./my-repo

# JSON output
everse-scan ./my-repo --format json

# Both formats, saved to files
everse-scan ./my-repo --format both -o report
```

### Scan a GitHub repository

```bash
everse-scan https://github.com/org/repo
```

### Role-adaptive reports

```bash
# Researcher view: plain language, credit/citation first
everse-scan ./my-repo --role researcher

# RSE view: technical, engineering-first
everse-scan ./my-repo --role rse
```

### Track progress with re-scan diff

```bash
# 1. Save a baseline
everse-scan ./my-repo --save baseline.json --format json

# 2. After making fixes, compare
everse-scan ./my-repo --diff baseline.json
```

Example diff output:

```
Progress: 7/36 (was 4/36), delta +3

## Improvements
- LICENSE: WARN -> PASS
- CITATION.cff: FAIL -> PASS
- CI/CD: FAIL -> PASS
```

### FAIR integrations

```bash
# Enable all FAIR integrations (+7 checks)
everse-scan ./my-repo --use

# Enable a specific integration
everse-scan ./my-repo --use howfairis
```

### Funder compliance

Funder detection is automatic — everse-scan scans your `.zenodo.json`, `CITATION.cff`, `README.md`, and `pyproject.toml` for funder mentions and grant IDs, then checks alignment with that funder's requirements.

```bash
# Just run a normal scan — funder detection is built-in
everse-scan ./my-repo
```

Supported funders: Horizon Europe, NSF, Wellcome, DFG, ANR, UKRI, Helmholtz.

### Options reference

| Option | Description |
|--------|-------------|
| `--format {json,markdown,both}` | Output format (default: markdown) |
| `--output, -o` | Output file prefix |
| `--role {default,researcher,rse}` | Adapt report to a target role |
| `--save BASELINE` | Save scan results as a baseline JSON file |
| `--diff BASELINE` | Compare current scan with a previous baseline |
| `--use [INTEGRATIONS]` | Enable FAIR integrations (howfairis, cffconvert, codemeta) |
| `--version` | Show version |

## Using with AI assistants

`everse-scan` works in two modes:

### 1. Standalone CLI (no AI required)

Run the scan, get a report, fix issues yourself:

```bash
everse-scan ./my-repo -o report
```

### 2. CLI + AI assistant for remediation

Generate a report, then hand it to an AI coding assistant to help you fix the identified issues. This works with any AI assistant that can read files:

**With opencode:**

```bash
# Generate the report
everse-scan ./my-repo -o report.md

# Then in your opencode session:
# "Read report.md and help me fix the failing checks"
```

everse-scan is also available as an **opencode skill** — it triggers naturally when you ask:

- "Scan my repo"
- "Analyze my code quality"
- "Check if my project follows FAIR practices"
- "Run an EVERSE audit on my repo"

**With Claude Code, Copilot, Cursor, or VS Code AI:**

```bash
# Generate the report
everse-scan ./my-repo -o report.md

# Then ask your assistant:
# "Read report.md and help me fix the issues, starting with the quick wins"
```

**With GitHub Actions (CI/CD):**

```yaml
# .github/workflows/everse-scan.yml
name: everse-scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install everse-scan
      - run: everse-scan . --format markdown -o scan-report
      - uses: actions/upload-artifact@v4
        with:
          name: scan-report
          path: scan-report.md
```

## Checks overview

### Core checks (17)

| # | Check | RSQKit |
|---|---|---|
| 1 | README | [creating_good_readme](https://everse.software/RSQKit/creating_good_readme) |
| 2 | LICENSE | [licensing_software](https://everse.software/RSQKit/licensing_software) |
| 3 | CITATION.cff | [citing_software](https://everse.software/RSQKit/citing_software) |
| 4 | codemeta.json | [complete_software_metadata_codemeta](https://everse.software/RSQKit/complete_software_metadata_codemeta) |
| 5 | Structure | [software_project_structure](https://everse.software/RSQKit/software_project_structure) |
| 6 | Version control | [using_version_control](https://everse.software/RSQKit/using_version_control) |
| 7 | Tests | [testing_software](https://everse.software/RSQKit/testing_software) |
| 8 | Documentation | [software_documentation](https://everse.software/RSQKit/software_documentation) |
| 9 | CI/CD | [ci_cd](https://everse.software/RSQKit/ci_cd) |
| 10 | Packaging | [packaging_software](https://everse.software/RSQKit/packaging_software) |
| 11 | Static analysis | [static_analysis](https://everse.software/RSQKit/static_analysis) |
| 12 | Security | [research_software_security](https://everse.software/RSQKit/research_software_security) |
| 13 | Reproducible environments | [reproducible_software_environments](https://everse.software/RSQKit/reproducible_software_environments) |
| 14 | Code review | [code_review](https://everse.software/RSQKit/code_review) |
| 15 | Software identifiers | [software_identifiers](https://everse.software/RSQKit/software_identifiers) |
| 16 | Releasing | [releasing_software](https://everse.software/RSQKit/releasing_software) |
| 17 | Readable code | [writing_readable_code](https://everse.software/RSQKit/writing_readable_code) |

### Extended checks (19)

| # | Check | Category |
|---|---|---|
| 18 | Authorship | FAIR |
| 19 | ORCID | FAIR |
| 20 | Dependency management | Engineering |
| 21 | Containerization | Engineering |
| 22 | Computational workflows | Engineering |
| 23 | API documentation | Engineering |
| 24 | Changelog | Documentation |
| 25 | Contribution guidelines | Documentation |
| 26 | Code of conduct | Documentation |
| 27 | Issue templates | Documentation |
| 28 | Secret management | Security |
| 29 | Data management plan | Reproducibility |
| 30 | Reproducibility checklist | Reproducibility |
| 31 | Archiving | Sustainability |
| 32 | Future proofing | Sustainability |
| 33 | Software sustainability plan | Sustainability |
| 34 | Environmental sustainability | Sustainability |
| 35 | Software peer review | Quality |
| 36 | Software quality models | Quality |

### FAIR integrations (+7 with `--use`)

| Check | Source |
|-------|--------|
| FAIR: repository | [howfairis](https://github.com/fair-software/howfairis) |
| FAIR: license | howfairis |
| FAIR: registry | howfairis |
| FAIR: citation | howfairis |
| FAIR: checklist | howfairis |
| CITATION.cff validation | [cffconvert](https://github.com/citation-file-format/cffconvert) |
| codemeta.json validation | [codemeta validator](https://codemeta.github.io/) |

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
# Install in dev mode
uv pip install -e ".[dev]"

# Run tests
python3 -m pytest tests/ -v

# Scan everse-scan itself
everse-scan . --format both -o report
```

## Roadmap

| Status | Feature |
|--------|---------|
| Done | Core CLI with 36 deterministic checks |
| Done | Adaptive reports by role (researcher / RSE) |
| Done | Re-scan with diff and baseline tracking |
| Done | FAIR integrations (howfairis, cffconvert, codemeta) |
| Done | Funder compliance detection (7 funders) |
| Planned | PyPI publication |
| Planned | Additional funder profiles |
| Planned | RSQKit knowledge base auto-sync |
| Planned | Additional language support |

## License

MIT
