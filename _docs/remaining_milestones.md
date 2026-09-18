# everse-scan — Progress Status and Remaining Milestones

Last updated: 2026-09-18
Current branch: `feat/cli-python` (M3, to be merged into `main`)

## Git Log

```
fbf63e0 M3: CLI Python V2 core — 17 deterministic checks (feat/cli-python)
c2fb1cd M2: skill improvements — tier, lifecycle, tools, remediation (main)
528f5b3 M1: opencode skill V1 (MVP) — 10 checks, Markdown report (main)
0a75bcd plan: enrich V1/V1.1/V2 + add milestones M1-M6 (main)
c7f0014 initial commit (main)
```

## Branch `feat/cli-python`

M3 was developed on the `feat/cli-python` branch. It must be merged into `main` before continuing with M4.

```bash
git checkout main
git merge feat/cli-python
```

---

## Completed Milestones

### M1 — opencode Skill V1 (MVP) ✅

**Commit**: `528f5b3` (branch `main`)

**Deliverable**: `.opencode/skills/everse-scan/SKILL.md`

**Implemented**:
- opencode skill with natural triggering (rich description)
- 10 V1 checks: README, LICENSE, CITATION.cff, codemeta.json, Structure, Version control, Tests, Documentation, CI/CD, Packaging
- Multi-language detection (Python, R, C++, Julia, JS/TS, Rust, Go, Java, Ruby)
- Local + remote repository support (GitHub clone)
- Markdown report template: executive summary + prioritized action plan + technical details per task + AI spectrum
- AI spectrum assessment (0-10) with detection indicators
- Disclosure of non-covered RSQKit tasks
- Simple remediation menu

### M2 — V1.1: Skill Improvements ✅

**Commit**: `c2fb1cd` (branch `main`)

**Implemented**:
- Tier detection (three-tier model) with heuristics (script / tool-library / infrastructure) + check adaptation (N/A for tier 1)
- Lifecycle detection (early / active dev / maintenance / published) via git log
- RSQKit tools table by language (pytest/ruff/Sphinx for Python, testthat/lintr/pkgdown for R, etc.)
- AI spectrum guidance per level with detailed content (0, 1-3, 4-6, 7-9, 10) + cross-cutting practices + AI intensity considerations
- Quality dimensions: scorecard reproducibility / maintainability / findability / trustworthiness / reusability
- Contextual remediation: pre-fill CITATION.cff / codemeta.json from git log + README + LICENSE, with preview → confirmation → write flow
- Remediation chains: citation chain (→ Zenodo → DOI), CI chain (→ linting → dependabot → PR template), metadata chain (→ .zenodo.json → validation)
- Updated report template with all new sections

### M3 — Python CLI V2: Core ✅

**Commit**: `fbf63e0` (branch `feat/cli-python`)

**Implemented**:
- Functional Python CLI: `everse-scan scan ./repo --format json,markdown,both`
- 17 deterministic checks in Python: 10 V1 + 7 V1.1 (static analysis, security, reproducible envs, code review, software identifiers, releasing, readable code)
- Multi-language detection (`languages/detector.py`) with extension counting + config files + version files
- Tier detection (`context/tier.py`) with heuristics (source file count, packaging, git authors, tags, CI, Docker, docs)
- Lifecycle detection (`context/lifecycle.py`) via git log (commits, recent activity, tags, DOI)
- AI intensity detection (scanner.py) via indicators (.cursorrules, AGENTS.md, .opencode/, AI workflows, README mentions)
- Reporters: structured JSON (`reporters/json.py`) + full Markdown (`reporters/markdown.py`) with executive summary, quality dimensions, action plan, technical details, AI guidance
- Data models (`models.py`): CheckResult, ScanResult, CheckStatus (pass/warn/fail/na)
- Scanner orchestration (`scanner.py`): orchestrates the 17 checks + context + AI
- CLI entry point (`cli.py`) with argparse, GitHub URL support (temporary clone), --format, --output, --version
- `src/everse_scan/` architecture: `cli.py`, `scanner.py`, `checks/` (17 modules), `reporters/`, `languages/`, `context/`
- 15 passing tests with fixtures (`tests/fixtures.py`: sample repo with good practices + minimal repo)
- pyproject.toml with hatchling build, `everse-scan` entry point, pytest config, ruff config
- Auto-scan validated on the repo itself: 4/17 pass, 10 warn, 3 fail

**Architecture created**:
```
src/everse_scan/
├── __init__.py
├── cli.py              # CLI entry point (argparse, --format, --output)
├── scanner.py          # Scan orchestration (17 checks + context + AI)
├── models.py           # CheckResult, ScanResult, CheckStatus
├── checks/             # 17 deterministic check modules
│   ├── readme.py
│   ├── license.py
│   ├── citation.py
│   ├── codemeta.py
│   ├── structure.py
│   ├── version_control.py
│   ├── tests.py
│   ├── documentation.py
│   ├── cicd.py
│   ├── packaging.py
│   ├── static_analysis.py
│   ├── security.py
│   ├── reproducible_envs.py
│   ├── code_review.py
│   ├── software_identifiers.py
│   ├── releasing.py
│   └── readable_code.py
├── reporters/
│   ├── json.py         # Structured JSON output
│   └── markdown.py     # Full Markdown output
├── languages/
│   └── detector.py     # Multi-language detection
└── context/
    ├── tier.py          # Three-tier detection (script/tool/infrastructure)
    └── lifecycle.py     # Lifecycle detection (early/active/maintenance/published)
```

**Not implemented in M3 (deferred)**:
- `knowledge/rsqkit.yaml`: manual RSQKit knowledge base (tasks, checks, links). The plan called for "manual for M3" but it was not created. RSQKit URLs are currently hardcoded in each check. To be created for M5 (automatic sync).
- Tests for individual checks (only scanner + reporters integration tests exist)

---

## Remaining Milestones

### M4 — CLI V2: Adaptive Report + Re-scan

**Objective**: Adaptive role-based report, progress tracking, 2D prioritization.

**To implement**:
- `--role rse` / `--role researcher` → tone, priorities, report depth adapted to role
  - Researcher: plain language, credit/citation first, executive summary + quick wins
  - RSE: concise technical, engineering first (tests, CI, code review), full details
- `--save baseline.json`: save scan result as a baseline
- `--diff baseline.json`: re-scan and compare with the baseline → before/after delta
  - The diff report should show: before/after score, newly passed checks, regressed checks, updated next steps
  - Format: "7/17 (was 4/17). Improvements: LICENSE ✅, CITATION.cff ✅, CI ✅"
- 2D prioritization: effort × impact matrix (with risk, tier, lifecycle, role factors)
  - Impact factors: security risk, software tier, lifecycle stage, target role, funder requirements
- New files to create:
  - `src/everse_scan/reporters/adaptive.py` — adaptive role-based reporter
  - `src/everse_scan/reporters/diff.py` — progress reporter (re-scan)
- Modify `cli.py` to add `--role`, `--save`, `--diff`
- Tests for diff and adaptive reporter

**Completion criterion**: Baseline scan → fixes → re-scan → progress report shows "7/17 (was 4/17)"

### M5 — CLI V2: FAIR Integrations + Full Coverage

**Objective**: Integrate existing FAIR tools, cover the 35+ RSQKit tasks.

**To implement**:
- [howfairis](https://github.com/fair-software/howfairis) integration: `everse-scan scan ./repo --use howfairis` → 5 FAIR principles
- [cffconvert](https://github.com/citation-file-format/cffconvert) integration: automatic CITATION.cff validation
- [codemeta validator](https://codemeta.github.io/codemetar/) integration: codemeta.json validation
- GitHub security advisories integration: vulnerable dependencies
- Full coverage of 35+ RSQKit tasks: each task has a check (deterministic or heuristic)
- `knowledge/` directory:
  - `knowledge/rsqkit.yaml`: knowledge base (tasks, checks, links, tools by language) — manual then sync
  - `knowledge/sync.py`: automatic sync from [RSQKit GitHub](https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages)
- `integrations/` directory:
  - `integrations/howfairis.py`
  - `integrations/cffconvert.py`
  - `integrations/codemeta.py`
- `--use` flag to enable external integrations

**Completion criterion**: `everse-scan scan ./repo --use howfairis` → cross-referenced CLI + howfairis report, 35+ checks

### M6 — CLI V2: Funder Compliance + Advanced Context

**Objective**: Funder alignment, grant detection, recommendations based on funder.

**To implement**:
- Funder detection (Horizon Europe, NSF, Wellcome) from:
  - README (grant mentions)
  - `.zenodo.json` (grants field)
  - `CITATION.cff` (grants field)
- `knowledge/funders.yaml`: requirements by funder (Horizon Europe: open access + FAIR + DOI, NSF, Wellcome)
- "Funder compliance" section in the report: cross-reference funder requirements vs repository state
  - E.g.: "This project is funded by Horizon Europe. Missing: persistent DOI, explicit open source license."
- Advanced tier: fine-grained detection + suppression of non-relevant checks based on tier
- `context/funder.py`: funder detection

**Completion criterion**: Scan of a Horizon Europe repo → report shows "Missing: persistent DOI, open source license" per HE requirements

---

## How to Resume

1. Merge `feat/cli-python` into `main`:
   ```bash
   git checkout main
   git merge feat/cli-python
   ```
2. Create a branch for M4:
   ```bash
   git checkout -b feat/adaptive-reporting
   ```
3. Implement M4 (adaptive report + re-scan + 2D prioritization)
4. Pause + commit
5. Continue with M5, then M6

## Useful Commands

```bash
# Install in dev mode
uv pip install -e ".[dev]"

# Run tests
python3 -m pytest tests/ -v

# Scan a repository
everse-scan scan ./repo --format both -o report

# Scan a GitHub repository
everse-scan scan https://github.com/org/repo --format markdown
```
