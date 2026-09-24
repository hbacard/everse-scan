---
name: everse-scan
description: >-
  Scans a code repository (local or remote GitHub) and generates a structured report
  on software quality and FAIR compliance with EVERSE/RSQKit practices. Evaluates 10
  key checks (README, LICENSE, CITATION.cff, codemeta.json, structure, version control,
  tests, documentation, CI/CD, packaging), detects the language and software tier,
  assesses the lifecycle stage, reads the AI intensity profile
  (ai-intensity.yaml), quality dimensions, and proposes
  contextual remediation actions. Triggers on requests like "scan my repo", "analyze
  my code quality", "check FAIR practices", "EVERSE audit", "everse-scan", or any
  request to analyze the quality/compliance of a research software repository.
---

# EVERSE Scan

Research repository analysis tool that generates a structured report on software quality and FAIR compliance with EVERSE/RSQKit practices.

> "Scan my repo, give me a structured report on areas to improve following EVERSE practices in RSQKit."

## Target Audience

Research Software Engineers (RSEs) and researchers who code.

---

## Workflow

### Step 1 — Identify the target

Determine what to scan:

1. **Local repository**: path provided by the user or current directory (`.`)
2. **Remote GitHub repository**: URL in the format `https://github.com/org/repo`

If the user provides a GitHub URL, clone temporarily:

```bash
git clone --depth 1 https://github.com/org/repo /tmp/everse-scan-<repo-name>
```

Then analyze the cloned repo as a local repository. Clean up the temporary directory after analysis.

If no path/URL is provided and no repository is obvious from the context, **ask before proceeding**.

### Step 2 — Multi-language detection

Detect the primary language(s) of the repository by analyzing:

**Configuration files** (via Glob):
- `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt` → **Python**
- `package.json`, `tsconfig.json` → **JavaScript/TypeScript**
- `Cargo.toml` → **Rust**
- `DESCRIPTION`, `NAMESPACE` → **R**
- `Project.toml` → **Julia**
- `CMakeLists.txt`, `Makefile` → **C/C++**
- `go.mod` → **Go**
- `pom.xml`, `build.gradle` → **Java**
- `Gemfile` → **Ruby**

**Version files** (via Glob):
- `.python-version` → Python
- `.ruby-version` → Ruby
- `.tool-versions`, `.node-version` → JS/TS

**Source file extensions** (via Glob, count occurrences):
- `.py` → Python, `.js`/`.ts`/`.jsx`/`.tsx` → JS/TS, `.R`/`.r` → R, `.jl` → Julia, `.c`/`.cpp`/`.h`/`.hpp` → C/C++, `.rs` → Rust, `.go` → Go, `.java` → Java, `.rb` → Ruby

The report indicates the primary language (most files) and any secondary languages detected.

### Step 3 — Tier detection (three-tier model)

The RSQKit defines a [three-tier model](https://everse.software/RSQKit/three_tier_view): **scripts** → **tools/prototypes** → **infrastructure**. A throwaway analysis script and a published HPC framework do not need the same practices. Detect the tier using heuristics (see the **Tier Detection** section below) and **adapt the relevant checks**.

### Step 4 — Lifecycle detection

Detect the [lifecycle stage](https://everse.software/RSQKit/life_cycle) of the repository (early / active dev / maintenance / published) using heuristics (see the **Lifecycle Detection** section below). The lifecycle stage influences which recommendations are prioritized.

### Step 5 — Run the 10 checks

For each check, use available tools (Glob, Grep, Read, Bash) to examine the repository. See the **10 Checks Reference** section below for detailed criteria. Adapt checks based on the detected tier (some checks are removed or attenuated for scripts).

For each check, determine a status:
- **PASS**: the check is satisfied
- **WARN**: partially satisfied, improvements needed
- **FAIL**: not satisfied or absent

### Step 6 — AI Usage Determination

Read the repository's `ai-intensity.yaml` file if present. This is a **self-assessment
profile** produced by the AI Intensity Q&A skill — it is NOT determined by scanning
repository files. The scan simply reads and displays it. See the **AI Usage Determination**
section below.

### Step 7 — Evaluate quality dimensions

Calculate a scorecard per quality dimension (see the **Quality Dimensions** section below). The dimensions are: reproducibility, maintainability, findability, trustworthiness, reusability.

### Step 8 — Generate the report

Generate the report by strictly following the **Report Template** structure below. The report is written in Markdown and saved to `everse-scan-report.md` at the root of the analyzed repository (or displayed if the user prefers).

### Step 9 — Remediation menu

At the end of the report, propose an interactive menu listing files to generate (pre-filled from the repository) and available remediation chains. See the **Contextual Remediation and Chains** section below.

---

## 10 Checks Reference

### Check 1 — README

**RSQKit**: https://everse.software/RSQKit/creating_good_readme

**What to look for**:
- Presence of `README.md` or `README.rst` at the root
- Content quality: project description, installation instructions, usage examples, license mention
- Presence of badges (CI, coverage, license, DOI)

**Evaluation criteria**:
- **PASS**: README present with description, installation, usage, and license mention
- **WARN**: README present but missing key sections (installation, usage, or license)
- **FAIL**: No README found

**Typical recommendations**:
- If FAIL: create a minimal README.md (project name, brief description, installation, usage, license)
- If WARN: complete the missing sections

**Recommended RSQKit tools** (by language):
- See the **RSQKit Tools by Language** table — "Docs" row

---

### Check 2 — LICENSE

**RSQKit**: https://everse.software/RSQKit/licensing_software

**What to look for**:
- Presence of a `LICENSE`, `LICENSE.md`, `LICENCE`, `COPYING` file at the root
- Identifiable license type (SPDX identifier)
- License mention in `pyproject.toml`, `package.json`, or other packaging file

**Evaluation criteria**:
- **PASS**: LICENSE file present with recognized license (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, etc.)
- **WARN**: License mentioned in a config file but no dedicated LICENSE file, or non-standard license
- **FAIL**: No license information

**Typical recommendations**:
- No license = legally non-reusable. This is a **critical risk**.
- If FAIL: add a LICENSE file (recommend MIT or Apache-2.0 for research software, unless funder constraints apply)

---

### Check 3 — CITATION.cff

**RSQKit**: https://everse.software/RSQKit/citing_software

**What to look for**:
- Presence of `CITATION.cff` at the root
- Validity of required fields: `title`, `authors`, `date-released`, `version`, `preferred-citation`
- Consistency with git authors

**Evaluation criteria**:
- **PASS**: CITATION.cff present with required fields completed
- **WARN**: CITATION.cff present but fields missing or incomplete
- **FAIL**: No CITATION.cff file

**Typical recommendations**:
- If FAIL: create a minimal CITATION.cff — pre-fillable from `git log` + README + LICENSE (see **Contextual Remediation**)
- If WARN: complete the missing fields

---

### Check 4 — codemeta.json

**RSQKit**: https://everse.software/RSQKit/complete_software_metadata_codemeta

**What to look for**:
- Presence of `codemeta.json` at the root
- Valid structure (parseable JSON)
- Required fields: `@context`, `@type`, `name`, `author`, `description`, `license`, `codeRepository`
- Presence of `programmingLanguage`, `softwareVersion`, `developmentStatus`

**Evaluation criteria**:
- **PASS**: codemeta.json present with required fields and valid structure
- **WARN**: codemeta.json present but fields missing or incomplete structure
- **FAIL**: No codemeta.json

**Typical recommendations**:
- If FAIL: create a codemeta.json — pre-fillable from CITATION.cff + pyproject.toml/package.json + dependencies (see **Contextual Remediation**)
- If WARN: complete the missing fields

---

### Check 5 — Project Structure

**RSQKit**: https://everse.software/RSQKit/software_project_structure

**What to look for** (via Glob on the root):
- Directory organization: presence of `src/`, `tests/`, `docs/`, `examples/`
- Separation of code/source vs configuration vs documentation
- Language-specific conventions:
  - Python: `src/` layout (`src/package_name/`), separate `tests/`
  - JS/TS: `src/` + `dist/`, `test/` or `__tests__/`
  - R: `R/`, `tests/testthat/`, `vignettes/`, `man/`
  - C++: `src/` + `include/`, `tests/`
  - Julia: `src/`, `test/`, `docs/`

**Evaluation criteria**:
- **PASS**: Clear structure with code/tests/docs separation following language conventions
- **WARN**: Partially organized structure (e.g., tests present but no `src/`, or docs mixed with code)
- **FAIL**: Flat structure, everything at the root, no organization

**Typical recommendations**:
- If FAIL/WARN: reorganize following the detected language's conventions
- Refer to the RSQKit page for specific conventions

---

### Check 6 — Version Control

**RSQKit**: https://everse.software/RSQKit/using_version_control

**What to look for** (via Bash):
- Presence of `.git/` (git repository)
- Presence of `.gitignore` and its quality (ignores build artifacts, venvs, etc.)
- Number of commits (`git rev-list --count HEAD`)
- Number of authors (`git log --format='%aN' | sort -u | wc -l`)
- Presence of tags/releases (`git tag`)
- Branches (`git branch -a`)

**Evaluation criteria**:
- **PASS**: Git repository with appropriate `.gitignore`, regular commits, tags/releases present
- **WARN**: Git repository but `.gitignore` missing or incomplete, or no tags/releases
- **FAIL**: No git repository

**Typical recommendations**:
- If FAIL: initialize git (`git init`), create a `.gitignore` adapted to the language
- If WARN: complete the `.gitignore`, create tags for versions

---

### Check 7 — Tests

**RSQKit**: https://everse.software/RSQKit/testing_software

**What to look for** (based on detected language):
- **Python**: `tests/` directory, `test_*.py` or `*_test.py` files, `pytest` config in `pyproject.toml` or `setup.cfg`, presence of `conftest.py`
- **R**: `tests/testthat/` directory, `test-*.R` or `testthat.R` files
- **JS/TS**: `test/` or `__tests__/` directory, `*.test.js` or `*.spec.js` files, config in `package.json` (`jest`, `vitest`, `mocha`)
- **C++**: `CMakeLists.txt` with `enable_testing()`, `test_*.cpp` files, usage of Google Test / Catch2
- **Julia**: `test/` directory, `runtests.jl` file, usage of `Test.jl`

**Coverage presence**:
- Python: `coverage`, `pytest-cov` in dependencies
- JS/TS: `nyc`, `c8`, or `collectCoverage` config in jest
- General: presence of coverage badges in the README

**Evaluation criteria**:
- **PASS**: Tests present with configured framework, multiple test files
- **WARN**: Tests present but minimal (single file, no clear framework), or framework mentioned but few tests
- **FAIL**: No tests found

**Typical recommendations**:
- If FAIL: create a `tests/` directory with a first test — use the recommended framework (see **Tools Table** — "Tests" row)
- If WARN: expand test coverage

---

### Check 8 — Documentation

**RSQKit**: https://everse.software/RSQKit/software_documentation

**What to look for**:
- Presence of a `docs/` directory with content (not empty)
- Docstrings in source code (via Grep: `"""`, `/**`, `#'`, `//`)
- README as minimal documentation (cross-referenced with Check 1)
- Documentation site: `mkdocs.yml`, `conf.py` (Sphinx), `.readthedocs.yaml`, `docusaurus.config.js`, `_pkgdown.yml`
- GitHub Wiki (via API or mention in README)

**Evaluation criteria**:
- **PASS**: Dedicated documentation (docs/ + doc site) with docstrings in code
- **WARN**: Documentation limited to README only, or docstrings present but no dedicated docs/
- **FAIL**: No documentation (not even a structured README)

**Typical recommendations**:
- If FAIL/WARN: create a `docs/` directory, add docstrings to public code
- For Python: recommend Sphinx or MkDocs; for R: pkgdown; for JS: Docusaurus (see **Tools Table** — "Docs" row)

---

### Check 9 — CI/CD

**RSQKit**: https://everse.software/RSQKit/ci_cd

**What to look for** (via Glob):
- **GitHub Actions**: `.github/workflows/*.yml`
- **GitLab CI**: `.gitlab-ci.yml`
- **Jenkins**: `Jenkinsfile`
- **CircleCI**: `.circleci/config.yml`
- **Travis**: `.travis.yml`
- **Azure Pipelines**: `azure-pipelines.yml`

**CI quality**:
- Presence of test jobs
- Presence of linting/formatting jobs
- Version matrix (e.g., Python 3.11, 3.12, 3.13)
- Presence of Dependabot (`.github/dependabot.yml`)

**Evaluation criteria**:
- **PASS**: CI/CD configured with test and linting jobs
- **WARN**: CI/CD present but minimal (single job, no linting, no matrix)
- **FAIL**: No CI/CD configuration

**Typical recommendations**:
- If FAIL: create a basic GitHub Actions workflow (test based on detected language — see **Tools Table** — "CI" row)
- If WARN: add linting (see **Tools Table** — "Linting" row), expand the version matrix

---

### Check 10 — Packaging

**RSQKit**: https://everse.software/RSQKit/packaging_software

**What to look for** (based on detected language):
- **Python**: `pyproject.toml` (recommended), `setup.py`, `setup.cfg`, presence of `[build-system]`, entry points `[project.scripts]`
- **JS/TS**: `package.json` with `name`, `version`, `main`/`exports`, `bin`
- **R**: `DESCRIPTION` with `Package`, `Version`, `Imports`
- **Julia**: `Project.toml` with `name`, `version`, `deps`
- **C++**: `CMakeLists.txt` with `install()`, `CPack`, or `Conan` (`conanfile.py`/`conanfile.txt`)
- **Rust**: `Cargo.toml` with `[package]`
- **Docker**: `Dockerfile` or `docker-compose.yml` (container packaging)

**Evaluation criteria**:
- **PASS**: Packaging correctly configured with complete metadata (name, version, dependencies, entry points)
- **WARN**: Basic packaging present (e.g., minimal `setup.py` without `pyproject.toml`, or `package.json` without `version`)
- **FAIL**: No packaging configuration

**Typical recommendations**:
- If FAIL: create a packaging file based on the language (see **Tools Table** — "Packaging" row)
- If WARN: migrate to modern standards (pyproject.toml for Python)

---

## RSQKit Tools by Language

Source: https://everse.software/RSQKit/all_tools_and_resources

The report recommends the exact tool for the detected language rather than generic advice.

| Check / Category | Python | R | JS/TS | C++ | Julia |
|---|---|---|---|---|---|
| **Tests** | pytest, hypothesis | testthat | jest, vitest | CTest, Google Test | Test.jl |
| **Linting** | ruff, mypy | lintr | eslint, prettier | clang-tidy | JuliaFormatter.jl |
| **Formatting** | ruff format, black | styler | prettier | clang-format | JuliaFormatter.jl |
| **CI** | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions |
| **Packaging** | pyproject.toml, hatch, uv | devtools | npm publish | CMake, Conan | Pkg.jl |
| **Docs** | Sphinx, MkDocs | pkgdown | JSDoc, Docusaurus | Doxygen | Documenter.jl |
| **Coverage** | pytest-cov, coverage | covr | nyc, c8 | gcov, lcov | Coverage.jl |
| **Security** | pip-audit, safety | oysteR | npm audit | trivy | Pkg.jl audit |
| **Repro envs** | uv.lock, poetry.lock, pip-tools | renv | package-lock.json | conan.lock | Manifest.toml |

---

## Tier Detection (three-tier model)

Source: https://everse.software/RSQKit/three_tier_view

The RSQKit defines a three-tier model. A throwaway analysis script and a published HPC framework do not need the same practices. Detect the tier using the heuristics below and **adapt the relevant checks**.

### Detection Heuristics

To detect the tier, gather the following signals (via Glob, Bash):

- **Number of source files** (via Glob: `**/*.py`, `**/*.js`, etc., excluding `.venv`, `node_modules`, `.git`, `__pycache__`, `dist`, `build`)
- **Presence of packaging** (via Glob: `pyproject.toml`, `package.json`, `Cargo.toml`, `DESCRIPTION`, `Project.toml`, `CMakeLists.txt`)
- **Number of git authors** (via Bash: `git log --format='%aN' | sort -u | wc -l`)
- **Presence of tests** (via Glob: `tests/`, `test/`, `test_*.py`, etc.)
- **Presence of releases/tags** (via Bash: `git tag`)
- **Presence of CI** (via Glob: `.github/workflows/`, `.gitlab-ci.yml`, etc.)
- **Presence of Dockerfile** (via Glob: `Dockerfile`)
- **Presence of extensive docs** (via Glob: `docs/` with multiple files)

### Classification

| Tier | Heuristics | Relevant checks | Removed/attenuated checks |
|---|---|---|---|
| **Script** (tier 1) | < 10 source files, no packaging, no tests, 1 git author, no releases | Version control, LICENSE, README, .gitignore | codemeta.json, CI testing matrices, containers, packaging |
| **Tool/Library** (tier 2) | Packaging present (pyproject.toml, package.json, etc.), > 1 author, tests present or recommended, structured README | All 10 checks + recommendation for citation, metadata, releasing | Infrastructure-level only |
| **Infrastructure** (tier 3) | Multi-package, complex CI, Docker, extensive docs, numerous contributors, tagged releases | All 10 checks + recommendation for security, reproducible envs, performance, future-proofing | None — full evaluation |

### Report Display

The report displays the detected tier and justifies the ignored checks:

> "This repository is detected as **script (tier 1)**. CI testing matrices, codemeta.json and containers checks are not relevant at this level. See the [RSQKit three-tier model](https://everse.software/RSQKit/three_tier_view)."

For a repository detected as tier 1 (script):
- codemeta.json, CI/CD matrices, packaging and containers checks are marked **N/A** instead of FAIL
- A note explains why they are not relevant
- Recommendations focus on: LICENSE, README, .gitignore, version control

For a repository detected as tier 2 (tool/library):
- All 10 checks are evaluated
- Additional recommendations: citation (CITATION.cff), metadata (codemeta.json), releasing (tags)

For a repository detected as tier 3 (infrastructure):
- All 10 checks are evaluated
- Additional recommendations: security, reproducible envs, performance, future-proofing (RSQKit links to these uncovered tasks)

---

## Lifecycle Detection

Source: https://everse.software/RSQKit/life_cycle

Detect the repository's stage to adapt prioritized recommendations.

### Detection Heuristics

- **Commits**: `git rev-list --count HEAD` (total number)
- **Last activity**: `git log -1 --format=%cd --date=short` (last commit date)
- **Releases/tags**: `git tag` (presence and count)
- **DOI**: presence of `.zenodo.json`, or DOI badge in README (via Grep)
- **Recent commit frequency**: `git log --since='3 months ago' --oneline | wc -l`

### Classification

| Stage | Heuristics | Prioritized recommendations |
|---|---|---|
| **Early** | < 10 commits, no tags, 1 author | Structure, LICENSE, .gitignore, README |
| **Active dev** | Regular commits (> 5 in the last 3 months), no CI or minimal CI | Tests, CI, documentation |
| **Maintenance** | Releases/tags present, few recent commits (< 5 in the last 3 months) | Future-proofing, dependency updates, archiving |
| **Published** | DOI present, minimal activity | Verify citation is up to date, complete metadata (codemeta.json) |

### Report Display

The report displays the detected stage and uses it to prioritize the action plan recommendations:

> "Detected lifecycle stage: **Active dev**. Prioritized recommendations: tests, CI, documentation."

---

## Quality Dimensions

Source: https://everse.software/RSQKit/all_indicators

The report includes a scorecard per quality dimension. Each dimension is evaluated by cross-referencing the results of relevant checks.

| Dimension | Checks involved | Evaluation |
|---|---|---|
| **Reproducibility** | Packaging, Tests, CI/CD | ✅ if Packaging + CI/CD PASS; ⚠️ if partial; ❌ if Packaging or CI/CD FAIL |
| **Maintainability** | Structure, Documentation | ✅ if Structure + Documentation PASS; ⚠️ if partial; ❌ if FAIL |
| **Findability** | CITATION.cff, codemeta.json | ✅ if CITATION.cff + codemeta.json PASS; ⚠️ if partial; ❌ if FAIL |
| **Trustworthiness** | Tests, CI/CD, Version control | ✅ if Tests + CI/CD PASS; ⚠️ if partial; ❌ if FAIL |
| **Reusability** | LICENSE, README, Documentation | ✅ if LICENSE + README PASS; ⚠️ if partial; ❌ if LICENSE FAIL |

The scorecard is displayed in the report as a table with an overall grade per dimension (✅/⚠️/❌).

---

## Non-covered RSQKit Tasks (Disclosure)

> ⚠️ This scan evaluates **10 of the 35+ RSQKit tasks**. The following tasks are **not** evaluated:
>
> - [Static analysis](https://everse.software/RSQKit/static_analysis) — linters, formatters
> - [Software security](https://everse.software/RSQKit/research_software_security) — secrets, vulnerabilities
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments) — lockfiles, containers
> - [Code review](https://everse.software/RSQKit/code_review) — PR templates, CODEOWNERS
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers) — DOI, Zenodo
> - [Releasing software](https://everse.software/RSQKit/releasing_software) — CHANGELOG, semantic versioning
> - [Writing readable code](https://everse.software/RSQKit/writing_readable_code) — formatting conventions
> - [Archiving software](https://everse.software/RSQKit/archiving_software)
> - [Future proofing](https://everse.software/RSQKit/future_proofing)
> - [Performance profiling](https://everse.software/RSQKit/performance_profiling_and_optimization)
> - [Environmental sustainability](https://everse.software/RSQKit/improving_environmental_sustainability)
> - [Computational workflows](https://everse.software/RSQKit/computational_workflows)
> - ... (see [complete list](https://everse.software/RSQKit/tasks))

A "pass" on the 10 checks does not mean the repository follows all best practices. It means the 10 evaluated checks are satisfied.

---

## AI Usage Determination

The RSQKit defines a [spectrum of AI usage intensity](https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage)
from 0 to 10. **This spectrum is a self-assessment framework** — it cannot be
determined by scanning repository files. The scan reads a self-determined profile
from `ai-intensity.yaml` (produced by the AI Intensity Q&A skill) and displays it
neutrally in the report.

### How It Works

1. The user runs the **AI Intensity Q&A skill** (separate from everse-scan)
2. The skill asks interactive questions and produces `ai-intensity.yaml`
3. everse-scan reads `ai-intensity.yaml` at scan time and includes the profile in the report
4. If no `ai-intensity.yaml` is found, the report displays "Not found" and points the
   user to the AI Intensity Q&A skill

### The `ai-intensity.yaml` File

The file contains self-determined intensity levels (0-10 on the RSQKit spectrum):

| Field | Description |
|---|---|
| `intensity.current` | Where the user currently sits on the spectrum |
| `intensity.desired` | Where the user wants to be |
| `intensity.authorized` | What is allowed/authorized in their context |
| `intensity.sustainable` | What is sustainable given review capacity |
| `determination.*` | Free-text notes explaining each level (from the Q&A) |
| `declaration.*` | Who determined it, when, and next review date |

### What the Report Displays

When the profile is found:
- A table with the four levels (current, desired, authorized, sustainable) and the
  user's notes for each
- The RSQKit quote: "It is not a maturity scale. Higher intensity does not mean better
  practice."
- The determination date and who determined it
- RSQKit considerations (questions for the user, not tool recommendations)

When the profile is **not found**:
- A clear message: "No AI intensity profile (`ai-intensity.yaml`) found in this repository."
- An explanation that the spectrum is a self-assessment framework that cannot be
  determined by scanning files
- A pointer to the AI Intensity Q&A skill
- Link to the RSQKit spectrum page

### RSQKit References

- **Spectrum of Intensity of AI Usage**: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- **AI Intensity Considerations**: https://everse.software/RSQKit/ai_intensity_considerations

---

## Contextual Remediation (pre-fill)

Remediation does not generate **blank templates**. Each generated file is **pre-filled from the actual repository content**.

### Data Sources for Pre-fill

| File to generate | Pre-fill data source | Commands/tools |
|---|---|---|
| `CITATION.cff` | Authors via `git log --format='%aN <%aE>'`, title from README H1, license from LICENSE → SPDX, repo URL from `git remote -v`, version from latest tag | Bash (git log, git remote, git tag) + Read (README) + Read (LICENSE) |
| `codemeta.json` | Same as CITATION.cff + dependencies from pyproject.toml/package.json, language from detector, keywords from README | Bash (git) + Read (pyproject.toml/package.json) + Read (README) |
| `README.md` | Project name from repo directory, description from existing README (if partial), installation section from detected deps, license section from LICENSE | Read (existing README) + Read (LICENSE) + Glob (deps) |
| `.github/workflows/test.yml` | Runner based on language (pytest for Python, `npm test` for JS, CTest for C++), Python version from `.python-version` or `pyproject.toml` | Read (pyproject.toml) + Glob (.python-version) |
| `.gitignore` | Template based on detected language (Python → `__pycache__/`, `.venv/`, `*.pyc`, etc.) | Glob (detected language) |

### Generation Flow (trust + transparency)

1. **Preview** the content to be generated (before writing) — display the content to the user
2. Ask for **explicit confirmation** from the user
3. **Write** the file
4. **Display** what was created/modified
5. Propose the **next step** in the remediation chain (see below)

---

## Remediation Chains

Generating a file is often only the first step. Propose **chains** that sequence remediation actions in a logical order.

### Citation Chain

```
1. Generate CITATION.cff (pre-filled from git + README + LICENSE)
   → 2. Connect the repository to Zenodo (GitHub integration)
   → 3. Create a release (tag) to trigger the Zenodo DOI
   → 4. Add the DOI badge in the README
   → 5. Add the DOI in codemeta.json "identifier"
```

### CI Chain

```
1. Generate .github/workflows/test.yml (adapted to detected language)
   → 2. Add a linting job (ruff for Python, eslint for JS)
   → 3. Add Dependabot (.github/dependabot.yml)
   → 4. Add a PR template (.github/pull_request_template.md)
   → 5. Enable branch protection (instructions, not automated)
```

### Metadata Chain

```
1. Generate codemeta.json (pre-filled from deps + language + authors)
   → 2. Validate with the codemeta validator (link: https://codemeta.github.io/codemetar/)
   → 3. Add .zenodo.json to control the Zenodo deposit
   → 4. Verify consistency CITATION.cff ↔ codemeta.json
```

---

## Report Template

Generate the report by **strictly** following this structure. The report is saved to `everse-scan-report.md`.

```markdown
# EVERSE Scan Report

**Repository**: [repo name]
**Date**: [scan date]
**Language(s) detected**: [detected languages, primary first]
**Software tier**: [Script / Tool-Library / Infrastructure]
**Lifecycle stage**: [Early / Active dev / Maintenance / Published]
**AI Intensity Profile**: [Found / Not found]

---

## 1. Executive Summary

### Strengths
- [check]: [positive summary]
- ...

### Weaknesses
- [check]: [issue summary]
- ...

### Overall Compliance

| Check | Status |
|-------|--------|
| README | ✅ Pass / ⚠️ Warn / ❌ Fail |
| LICENSE | ... |
| CITATION.cff | ... |
| codemeta.json | ... |
| Structure | ... |
| Version control | ... |
| Tests | ... |
| Documentation | ... |
| CI/CD | ... |
| Packaging | ... |

### Quality Dimensions (RSQKit mapping)
> Source: https://everse.software/RSQKit/all_indicators

| Dimension | Score | Checks involved |
|---|---|---|
| Reproducibility | ✅ / ⚠️ / ❌ | Packaging, Tests, CI/CD |
| Maintainability | ✅ / ⚠️ / ❌ | Structure, Documentation |
| Findability | ✅ / ⚠️ / ❌ | CITATION.cff, codemeta.json |
| Trustworthiness | ✅ / ⚠️ / ❌ | Tests, CI/CD, Version control |
| Reusability | ✅ / ⚠️ / ❌ | LICENSE, README, Documentation |

### Detected Software Tier
**Tier**: [Script / Tool-Library / Infrastructure]
**Justification**: [heuristics that led to this classification]
**Adjusted checks**: [list of checks marked N/A and why]

### Detected Lifecycle Stage
**Stage**: [Early / Active dev / Maintenance / Published]
**Justification**: [heuristics that led to this classification]

### Non-evaluated Tasks

> ⚠️ This scan evaluates 10 of the 35+ RSQKit tasks. The following tasks are **not** evaluated:
> - [Static analysis](https://everse.software/RSQKit/static_analysis)
> - [Software security](https://everse.software/RSQKit/research_software_security)
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments)
> - [Code review](https://everse.software/RSQKit/code_review)
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers)
> - ... (see [complete list](https://everse.software/RSQKit/tasks))

---

## 2. Prioritized Action Plan

> Prioritization by effort × impact. Impact factors in risk, tier, lifecycle, and target role.

### Critical Risks (address first if detected)
1. 🔴 [critical issue, e.g.: no LICENSE] — **impact: critical** ([reason])
2. ...

### Quick Wins (low effort, high impact)
1. [action, e.g.: Add a minimal CITATION.cff] (cf. [RSQKit link]) — **impact: high**
2. ...

### Medium Term (moderate effort, moderate impact)
1. [action] (cf. [RSQKit link])
2. ...

### Long Term (high effort, structural impact)
1. [action] (cf. [RSQKit link])
2. ...

---

## 3. Technical Details by Task

### 3.1 README
**Status**: ✅ Pass / ⚠️ Warn / ❌ Fail
**RSQKit**: https://everse.software/RSQKit/creating_good_readme

**Findings**:
- [precise detail of what was found/missing]

**Recommendations**:
- [specific recommended action]

**Recommended RSQKit tools** (for [detected language]):
- [tool 1] — [why]
- See: https://everse.software/RSQKit/[page]#tools

> 💡 I can generate an improved README template if you'd like.

---

### 3.2 LICENSE
**Status**: ...
**RSQKit**: https://everse.software/RSQKit/licensing_software

**Findings**:
- ...

**Recommendations**:
- ...

---

[... repeat for each check: CITATION.cff, codemeta.json, Structure, Version control, Tests, Documentation, CI/CD, Packaging ...]

---

## 4. AI Usage Determination

**Profile**: [Found — `ai-intensity.yaml` present / Not found]

[If found, display:]
**Self-determined intensity levels** (RSQKit spectrum 0-10):

| Dimension | Level | User's notes |
|---|---|---|
| Current usage | X / 10 | [user's notes] |
| Desired | X / 10 | [user's notes] |
| Authorized | X / 10 | [user's notes] |
| Sustainable | X / 10 | [user's notes] |

> **RSQKit**: "It is not a maturity scale. Higher intensity does not mean better
> practice. It does not mean higher skill. It does not mean better quality."
> — [Spectrum of Intensity of AI Usage](https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage)

*Determined by*: [name] on [date]

**RSQKit considerations** (questions for the user, not tool recommendations):
- Where does your project sit? Where should it sit?
- Where do you sit? Where do you want to be? Where should you be?
- Move up when greater intensity solves a real problem.
- Move down when a simpler practice provides the same benefit.
- Source: https://everse.software/RSQKit/ai_intensity_considerations

[If not found, display:]
> No AI intensity profile (`ai-intensity.yaml`) found in this repository.
>
> The RSQKit AI spectrum is a **self-assessment framework** — it cannot be
> determined by scanning repository files. To determine your AI intensity,
> run the **AI Intensity Q&A skill**.
>
> See: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage

---

## 5. Remediation

I can help you fix the identified issues. Here is what I can do:

📋 Files to generate (pre-filled from your repository):
  1. LICENSE ([suggested license type])
  2. CITATION.cff (authors: [N] found via git log)
  3. codemeta.json (deps: [N] from [packaging file], language: [language])
  4. .github/workflows/test.yml ([test framework] for [detected language])
  5. .gitignore (template [detected language])
  6. README.md ([if missing or incomplete])

🔗 Available remediation chains:
  A. Citation chain → CITATION.cff → Zenodo → DOI → README badge
  B. CI chain → workflow → linting → dependabot → PR template
  C. Metadata chain → codemeta.json → .zenodo.json → validation

Tell me what you'd like to do (number, letter, or "all").
```

---

## Remediation Rules

- Only propose files relevant to checks that have FAIL or WARN status
- Only propose chains relevant to the detected tier and lifecycle
  - Tier 1 (script): no metadata chain, no CI chain (not relevant)
  - Tier 2 (tool): all relevant chains
  - Tier 3 (infrastructure): all chains + security/reproducible envs recommendations
- Do not generate without explicit user confirmation
- Always preview content before writing (display the file that will be created)
- After generating a file, propose the next step in the chain
- Pre-fill with repository data (git authors, project name, detected language, dependencies, license)
- If the user says "all", generate files one by one with preview + confirmation for each

---

## RSQKit References

- **Home page**: https://everse.software/RSQKit/
- **Tasks**: https://everse.software/RSQKit/tasks
- **Spectrum of AI Intensity**: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- **AI Intensity Considerations**: https://everse.software/RSQKit/ai_intensity_considerations
- **Three-tier model**: https://everse.software/RSQKit/three_tier_view
- **Lifecycle**: https://everse.software/RSQKit/life_cycle
- **Quality dimensions**: https://everse.software/RSQKit/quality_dimensions
- **All indicators**: https://everse.software/RSQKit/all_indicators
- **All tools and resources**: https://everse.software/RSQKit/all_tools_and_resources
- **GitHub source**: https://github.com/EVERSE-ResearchSoftware/RSQKit
