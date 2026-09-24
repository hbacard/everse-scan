# Plan: everse-scan

## Vision

`everse-scan` is a research repository analysis tool that generates a structured report on software quality and FAIR compliance with EVERSE/RSQKit practices. The goal is to help Research Software Engineers and researchers who code improve their projects according to community standards.

> "Scan my repo, give me a structured report on areas to improve following EVERSE practices in RSQKit."

---

## Roadmap

### V1 — opencode Skill/Agent

| Aspect | Decision |
|---|---|
| **Form** | opencode skill (direct analysis from the conversational AI session) |
| **Scope** | Core FAIR + basic quality (10 checks) |
| **Report format** | Structured Markdown (`everse-scan-report.md`) |
| **Methodology** | AI analysis: file reading (Read, Glob, Grep) + contextual interpretation |
| **Report structure** | Executive summary + prioritized action plan + technical details per task with RSQKit links |
| **Invocation** | Natural triggering (skill description) |
| **RSQKit source** | Knowledge embedded in SKILL.md |
| **Audience** | Research Software Engineers + Researchers who code |
| **Remediation** | Diagnosis + interactive invitation to generation |
| **Repositories** | Local + remote (GitHub URLs) |
| **Languages** | Multi-language (Python, R, C++, Julia, etc.) |
| **AI intensity** | Reads `ai-intensity.yaml` profile (created by the separate AI Intensity Q&A skill). If absent, notes "No AI intensity profile found" with RSQKit link. |

### V2 — CLI + Hybrid Skill

| Aspect | Decision |
|---|---|
| **Form** | Python CLI (deterministic checks) + opencode skill (AI enrichment) |
| **Scope** | Modular / à la carte (`--focus fair,security,ci-cd`) |
| **Methodology** | Deterministic Bash/Python checks + hybrid AI |
| **RSQKit source** | Local YAML knowledge base + optional sync from [GitHub RSQKit](https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages) |
| **Report** | Adaptive (executive summary for PI/researcher + technical details for RSE) |
| **Invocation** | Explicit command, contextual, with arguments |
| **Task scope** | All RSQKit tasks (35+) |
| **Remediation** | Phased: diagnosis → templates → generation with user approval |

---

## V1 — Detailed Specifications

### 1. opencode Skill

#### 1.1 Description (natural triggering)

The skill triggers when the user requests a repository analysis, software quality, FAIR compliance, etc. Example trigger phrases:

- "Scan my repo"
- "Analyze my code quality"
- "Check if my project follows FAIR practices"
- "Run an EVERSE audit on my repo"
- "everse-scan"

#### 1.2 Embedded RSQKit Reference

The SKILL.md embeds for each of the 10 checks:

- **Task name** and link to the corresponding RSQKit page
- **Evaluation criteria** (what to look for in the repository)
- **Compliance levels** (pass / warn / fail)
- **Typical recommendations** by status

### 2. The 10 V1 Checks

| # | Check | RSQKit page | What to look for |
|---|---|---|---|
| 1 | **README** | `/creating_good_readme` | Presence of README.md, content quality (description, installation, usage, license), badges |
| 2 | **LICENSE** | `/licensing_software` | Presence of a LICENSE file, license type (SPDX), compatibility |
| 3 | **Citation** | `/citing_software` | Presence of CITATION.cff, validity, required fields |
| 4 | **CodeMeta** | `/complete_software_metadata_codemeta` | Presence of codemeta.json, structure, required fields |
| 5 | **Project structure** | `/software_project_structure` | Directory organization (src/, tests/, docs/, etc.), conventions |
| 6 | **Version control** | `/using_version_control` | Use of git, .gitignore, number of commits, branches, tags/releases |
| 7 | **Tests** | `/testing_software` | Presence of tests (tests/, pytest, unittest, etc.), framework, coverage |
| 8 | **Documentation** | `/software_documentation` | Presence of docs/, docstrings, README, doc site |
| 9 | **CI/CD** | `/ci_cd` | Presence of .github/workflows/, .gitlab-ci.yml, Jenkinsfile, etc. |
| 10 | **Packaging** | `/packaging_software` | pyproject.toml, setup.py, Dockerfile, package.json, etc. |

#### 2.1 RSQKit Tasks Not Covered in V1 — Mandatory Disclosure

The V1 report **must include a disclosure section** listing the non-evaluated RSQKit tasks, with links. A "pass" must not give false confidence.

> ⚠️ This scan evaluates 10 of the 35+ RSQKit tasks. The following tasks are **not** evaluated:
> - [Static analysis](https://everse.software/RSQKit/static_analysis)
> - [Software security](https://everse.software/RSQKit/research_software_security)
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments)
> - [Code review](https://everse.software/RSQKit/code_review)
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers)
> - [Releasing software](https://everse.software/RSQKit/releasing_software)
> - [Writing readable code](https://everse.software/RSQKit/writing_readable_code)
> - [Archiving software](https://everse.software/RSQKit/archiving_software)
> - [Future proofing](https://everse.software/RSQKit/future_proofing)
> - [Performance profiling](https://everse.software/RSQKit/performance_profiling_and_optimization)
> - [Environmental sustainability](https://everse.software/RSQKit/improving_environmental_sustainability)
> - [Computational workflows](https://everse.software/RSQKit/computational_workflows)
> - ... (see [complete list](https://everse.software/RSQKit/tasks))

#### 2.2 High-impact Missing Checks (V1.1/V2 Candidates)

Several RSQKit tasks are mechanically detectable with high impact. To add as soon as possible:

| # | Check | RSQKit page | What to look for | Why it matters |
|---|---|---|---|---|
| 11 | **Static analysis** | `/static_analysis` | Linter/formatter configs (ruff, eslint, mypy, prettier, rustfmt) | Code quality, bug detection, low effort |
| 12 | **Security** | `/research_software_security` | Hardcoded secrets, dependabot, pip-audit/safety, CODEOWNERS | Direct risk, not just quality |
| 13 | **Reproducible envs** | `/reproducible_software_environments` | Lockfiles (requirements.txt pinned, poetry.lock, conda-lock), Dockerfile, Nix | Funder requirement, reproducibility |
| 14 | **Code review** | `/code_review` | PR templates (.github/pull_request_template.md), CODEOWNERS, branch protection | Collaboration, shared quality |
| 15 | **Software identifiers** | `/software_identifiers` | DOI, .zenodo.json, Zenodo badges in README | Citability, findability |
| 16 | **Releasing** | `/releasing_software` | Git tags, GitHub releases, CHANGELOG.md, semantic versioning | Traceability, reproducibility |
| 17 | **Readable code** | `/writing_readable_code` | Formatting configs (black, isort, prettier), conventions | Maintainability |

### 3. Multi-language Detection

The skill detects the primary language of the repository by analyzing:

- Configuration files (`pyproject.toml` → Python, `package.json` → JS/TS, `Cargo.toml` → Rust, `DESCRIPTION` → R, `Project.toml` → Julia, `CMakeLists.txt` → C/C++, etc.)
- Source file extensions
- Presence of `.python-version`, `.ruby-version`, `.tool-versions`, etc.

Checks adapt to the detected language (e.g., for Python → pytest, for R → testthat, for C++ → CTest, etc.).

### 3.1 Software Tier Detection (RSQKit three-tier model)

RSQKit defines a [three-tier model](https://everse.software/RSQKit/three_tier_view): **scripts** → **tools/prototypes** → **infrastructure**. A throwaway analysis script and a published HPC framework do not need the same practices. The skill detects the tier via heuristics and **adapts the relevant checks**:

| Tier | Detection heuristics | Relevant checks | Removed/attenuated checks |
|---|---|---|---|
| **Script** (tier 1) | < 10 source files, no packaging, no tests, 1 git author, no releases | Version control, LICENSE, README, .gitignore | codemeta.json, CI testing matrices, containers, future-proofing |
| **Tool/Library** (tier 2) | Packaging present (pyproject.toml, package.json), > 1 author, tests present or recommended, structured README | All 10 V1 checks + citation, metadata, releasing | Infrastructure-level only |
| **Infrastructure** (tier 3) | Multi-package, complex CI, Docker, extensive docs, numerous contributors, tagged releases | All checks + security, reproducible envs, performance, future-proofing, environmental sustainability | None — full evaluation |

The report displays the detected tier and justifies the ignored checks:
> "This repository is detected as **script (tier 1)**. CI testing matrices, codemeta.json and containers checks are not relevant at this level. See the [RSQKit three-tier model](https://everse.software/RSQKit/three_tier_view)."

### 4. Remote Repository Support

- **Local repository**: the skill analyzes the current directory or a provided path
- **Remote GitHub repository**: the skill temporarily clones the repo (via `git clone` to a temporary directory) then analyzes it as a local repository
- **URL detection**: `https://github.com/org/repo` → clone + scan

### 5. AI Usage Determination (RSQKit)

> **Key principle**: The RSQKit spectrum is **not a maturity scale**. Higher intensity does not mean better practice, higher skill, or better quality. The right level depends on the task, review capacity, material sensitivity, and safe access.
>
> *"Use the lowest intensity you can justify."* — RSQKit

#### 5.1 Design decision: determine, don't evaluate

The RSQKit AI spectrum (0-10) is designed as a **self-assessment framework**. The questions it poses — *"Where do you sit? Where do you want to be? Where should you be?"* — can only be answered by the user, not by scanning repository files.

**Previous approach (removed)**: Scan repo files for AI artifacts (`.cursorrules`, `AGENTS.md`, `.opencode/`, etc.) and assign an intensity level. This was:
- **Gameable** — anyone can remove AI artifacts from their repo
- **Unreliable** — file presence doesn't indicate actual usage intensity
- **Prescriptive** — the tool was making value judgments ("good starting point", "risks: over-reliance", "add guardrails")

**New approach**: A separate **AI Intensity Q&A skill** conducts an interactive assessment with the user. The results are stored in `ai-intensity.yaml` (following AI Declaration Format conventions). `everse-scan` reads this profile if present and includes it **neutrally** in the report. If absent, the report notes "No AI intensity profile found" with a link to the RSQKit AI pages.

#### 5.2 The AI Intensity Q&A Skill (separate skill)

A standalone opencode skill that triggers when the user asks to determine their AI intensity, assess their AI usage, or figure out what AI level is appropriate for their project.

**Four assessment dimensions** (mapped to RSQKit questions):

| Dimension | RSQKit question | What the Q&A explores |
|---|---|---|
| **Current usage** | "Where do you sit?" | What AI tools do you currently use? (ChatGPT, Copilot, Claude Code, Cursor, autonomous agents, etc.) → maps to spectrum level |
| **Desired intensity** | "Where do you want to be?" | What level of AI autonomy do you want? (conversational help, IDE suggestions, repo-aware, agentic, autonomous) → desired level |
| **Authorized intensity** | "Where should you be?" | What level of AI is allowed/authorized in your context? (project policy, institutional rules, funder requirements, data sensitivity) → authorized level |
| **Review capacity** | (affects sustainability) | How much review capacity do you have? What are you comfortable reviewing? (affects what intensity is sustainable) |

The Q&A walks the user through each dimension with concrete questions and examples from the RSQKit spectrum descriptions. It does **not** recommend a level — it helps the user **determine** their own level by presenting the RSQKit considerations neutrally.

#### 5.3 Profile file: `ai-intensity.yaml`

Stored in the repository root. Follows AI Declaration Format conventions (YAML, schema-validatable, human-edited). Separate from `aidecl.yaml` (which records provenance — what AI was used). `ai-intensity.yaml` records preferences — what AI level is desired/authorized.

```yaml
# AI Intensity Profile
# Generated by the AI Intensity Q&A skill
# This is NOT an evaluation — it is a self-determination by the project's users.
# See: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage

schema_version: "1.0.0"

project:
  name: my-research-project
  repository: https://github.com/org/repo

# Self-determined intensity levels (0-10, RSQKit spectrum)
intensity:
  current: 4          # Where the user currently sits
  desired: 6          # Where the user wants to be
  authorized: 7       # What is allowed/authorized in their context
  sustainable: 5      # What is sustainable given review capacity

# The determining factors (free text, from the Q&A)
determination:
  current_usage: >-
    Using Copilot for autocomplete and occasional Claude conversations for
    debugging. No repo-aware tools yet.
  desired_intensity: >-
    Would like to try repository-aware assistance for refactoring and test
    generation, but not ready for agentic workflows.
  authorized_intensity: >-
    No institutional restrictions. Funder (Horizon Europe) requires AI
    usage disclosure but does not limit intensity.
  review_capacity: >-
    Solo developer, limited time. Can review small patches carefully but
    cannot handle large autonomous diffs.

# RSQKit spectrum reference (embedded for the scan to display)
spectrum_reference:
  url: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
  considerations_url: https://everse.software/RSQKit/ai_intensity_considerations
  note: >-
    It is not a maturity scale. Higher intensity does not mean better practice.
    Use the lowest intensity you can justify.

declaration:
  date: "2026-09-24"
  determined_by: Jane Researcher
  next_review: "2027-03-24"
  notes: >-
    Initial self-assessment via AI Intensity Q&A skill.
```

#### 5.4 How everse-scan uses the profile

`everse-scan` does **not** conduct the Q&A. It simply reads `ai-intensity.yaml` if present:

- **Profile found**: Include the self-determined levels and the RSQKit considerations **neutrally** in the report. No evaluation, no "recommendations to move up/down". Present the levels as the user's own determination.
- **Profile absent**: Note "No AI intensity profile found" with a link to the RSQKit AI spectrum page and a suggestion to run the AI Intensity Q&A skill. Do **not** attempt to detect or infer AI usage from repo files.

#### 5.5 Reporting principles (non-prescriptive)

The report section for AI intensity follows these rules:

1. **Describe, don't prescribe** — present what the user determined, not what the tool thinks they should do
2. **Link, don't lecture** — point to the relevant RSQKit page for each spectrum level, let the user read the guidance themselves
3. **Quote, don't interpret** — use RSQKit's own language ("It is not a maturity scale. Higher intensity does not mean better practice.")
4. **Questions, not answers** — present RSQKit's own questions ("Where does your project sit? Where should it sit?") as prompts for the user, not as tool outputs
5. **No level is better** — never imply that higher or lower intensity is preferable

### 6. Markdown Report Structure

```markdown
# EVERSE Scan Report

**Repository**: [repo name]
**Date**: [date]
**Language(s) detected**: [languages]
**AI Intensity Profile**: [Found — ai-intensity.yaml / Not found]

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
| README | ✅ Pass |
| LICENSE | ⚠️ Warn |
| CITATION.cff | ❌ Fail |
| ... | ... |

### Quality Dimensions (RSQKit mapping)
> Source: https://everse.software/RSQKit/all_indicators

| Dimension | Score | Checks involved |
|---|---|---|
| Reproducibility | ⚠️ | Packaging, Tests, CI/CD, Reproducible envs |
| Maintainability | ✅ | Structure, Documentation, Readable code |
| Findability | ❌ | CITATION.cff, codemeta.json, Software identifiers |
| Trustworthiness | ⚠️ | Tests, CI/CD, Code review, Security |
| Reusability | ⚠️ | LICENSE, README, Documentation, Metadata |

### Non-evaluated Tasks
> ⚠️ This scan evaluates 10 of the 35+ RSQKit tasks. The following tasks are **not** evaluated:
> - [Static analysis](https://everse.software/RSQKit/static_analysis)
> - [Software security](https://everse.software/RSQKit/research_software_security)
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments)
> - [Code review](https://everse.software/RSQKit/code_review)
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers)
> - ... (see [complete list](https://everse.software/RSQKit/tasks))

### Detected Software Tier
**Tier**: [Script / Tool-Library / Infrastructure]
**Justification**: [heuristics that led to this classification]

---

## 2. Prioritized Action Plan

> Prioritization 2D: effort × impact. Impact factors in risk, tier, and role.

### Quick Wins (low effort, high impact)
1. Add a LICENSE file (cf. https://everse.software/RSQKit/licensing_software) — **impact: critical** (no license = non-reusable)
2. Create a minimal CITATION.cff (cf. https://everse.software/RSQKit/citing_software) — **impact: high** (academic credit)
...

### Critical Risks (address first if detected)
1. 🔴 Hardcoded secret in the repository — **impact: critical** (security)
2. 🔴 No version control — **impact: critical** (everything else depends on it)
...

### Medium Term (moderate effort, moderate impact)
1. Set up basic CI/CD (cf. https://everse.software/RSQKit/ci_cd)
2. Add unit tests — RSQKit recommends **pytest** for Python (cf. https://everse.software/RSQKit/testing_software)
...

### Long Term (high effort, structural impact)
1. Restructure the project according to conventions (cf. https://everse.software/RSQKit/software_project_structure)
2. Create comprehensive documentation (cf. https://everse.software/RSQKit/software_documentation)
...

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
- [tool 2] — [why]
- See: https://everse.software/RSQKit/[page]#tools

> 💡 I can generate an improved README template if you'd like.

---

### 3.2 LICENSE
...

---

## 4. AI Usage Determination

**Profile**: [Found — ai-intensity.yaml present / Not found]

### If profile found:

**Self-determined intensity levels** (RSQKit spectrum 0-10):

| Dimension | Level | User's notes |
|---|---|---|
| Current usage | X / 10 | [summary from profile] |
| Desired | X / 10 | [summary from profile] |
| Authorized | X / 10 | [summary from profile] |
| Sustainable | X / 10 | [summary from profile] |

> **RSQKit**: "It is not a maturity scale. Higher intensity does not mean better practice. It does not mean higher skill. It does not mean better quality."
> — [Spectrum of Intensity of AI Usage](https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage)

**RSQKit considerations** (questions for the user, not tool recommendations):
- Where does your project sit? Where should it sit?
- Where do you sit? Where do you want to be? Where should you be?
- Move up when greater intensity solves a real problem.
- Move down when a simpler practice provides the same benefit.
- Source: https://everse.software/RSQKit/ai_intensity_considerations

### If profile absent:

> No AI intensity profile (`ai-intensity.yaml`) found in this repository.
>
> The RSQKit AI spectrum is a **self-assessment framework** — it cannot be
> determined by scanning repository files. To determine your AI intensity,
> run the **AI Intensity Q&A skill**.
>
> See: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
```

### 7. Interactive Remediation — Contextual Generation

Remediation does not generate **blank templates**. Each generated file is **pre-filled from the actual repository content**:

#### 7.1 Contextual Generation (pre-fill from repository data)

| File to generate | Data source for pre-fill |
|---|---|
| `CITATION.cff` | Authors via `git log --format='%aN <%aE>'`, title from README H1, license from LICENSE → SPDX, repo URL from `git remote -v`, version from latest tag |
| `codemeta.json` | Same as CITATION.cff + dependencies from pyproject.toml/package.json, language from detector, keywords from README |
| `README.md` | Project name from repo directory, description from existing README (if partial), installation section from detected deps, license section from LICENSE |
| `.github/workflows/test.yml` | Runner based on language (pytest for Python, `npm test` for JS, CTest for C++), Python version from `.python-version` or `pyproject.toml` |
| `.gitignore` | Template based on detected language (Python → `__pycache__/`, `.venv/`, `*.pyc`, etc.) |

#### 7.2 Generation Flow (trust + transparency)

1. **Preview** the content to be generated (before writing)
2. Ask for **explicit confirmation** from the user
3. **Write** the file
4. **Display** what was created/modified
5. Propose the **next step** in the remediation chain

#### 7.3 Remediation Chains (not just one-shot)

Generating a file is often only the first step. The skill proposes **chains**:

**Citation chain**:
```
1. Generate CITATION.cff (pre-filled from git + README + LICENSE)
   → 2. Connect the repository to Zenodo (GitHub integration)
   → 3. Create a release (tag) to trigger the Zenodo DOI
   → 4. Add the DOI badge in the README
   → 5. Add the DOI in codemeta.json "identifier"
```

**CI chain**:
```
1. Generate .github/workflows/test.yml (adapted to detected language)
   → 2. Add a linting job (ruff for Python, eslint for JS)
   → 3. Add Dependabot (.github/dependabot.yml)
   → 4. Add a PR template (.github/pull_request_template.md)
   → 5. Enable branch protection (instructions, not automated)
```

**Metadata chain**:
```
1. Generate codemeta.json (pre-filled from deps + language + authors)
   → 2. Validate with the codemeta validator (link)
   → 3. Add .zenodo.json to control the Zenodo deposit
   → 4. Verify consistency CITATION.cff ↔ codemeta.json
```

#### 7.4 Interactive Menu

At the end of the report, the skill proposes:

```
I can help you fix the identified issues:

📋 Files to generate (pre-filled from your repository):
  1. LICENSE (MIT detected from pyproject.toml)
  2. CITATION.cff (authors: 3 found via git log)
  3. codemeta.json (deps: 5 from pyproject.toml)
  4. .github/workflows/test.yml (pytest for Python 3.12)
  5. .gitignore (Python template)

🔗 Available remediation chains:
  A. Citation chain → CITATION.cff → Zenodo → DOI → README badge
  B. CI chain → workflow → linting → dependabot → PR template
  C. Metadata chain → codemeta.json → .zenodo.json → validation

Tell me what you'd like to do (number, letter, or "all").
```

---

## V1 Skill Architecture

```
.opencode/skills/everse-scan/
├── SKILL.md              # Skill instructions + embedded RSQKit reference
└── (no external dependencies in V1)
```

The SKILL.md will contain:
1. **Description** (for natural triggering)
2. **Workflow** (analysis steps)
3. **10 checks reference** (criteria, levels, recommendations)
4. **Report template** (Markdown structure)
5. **AI intensity profile reader** (reads `ai-intensity.yaml` if present, presents neutrally)
6. **Interactive remediation instructions** (contextual generation + chains)

---

## AI Intensity Q&A Skill (separate skill)

A standalone opencode skill, separate from `everse-scan`. It conducts an interactive self-assessment of the user's AI usage intensity according to the RSQKit spectrum (0-10) and saves the result to `ai-intensity.yaml`.

### Architecture

```
.opencode/skills/ai-intensity/
├── SKILL.md              # Q&A workflow + RSQKit spectrum reference
└── (no external dependencies)
```

### Description (natural triggering)

Triggers when the user asks to determine, assess, or figure out their AI usage intensity:

- "What AI intensity level should I use?"
- "Determine my AI intensity"
- "What level of AI is appropriate for my project?"
- "Am I using too much AI?"
- "ai-intensity"

### Q&A Workflow

The skill walks the user through **four dimensions**, one question at a time. Each question presents the relevant RSQKit spectrum descriptions to help the user self-assess. The skill **never assigns a level** — it helps the user **determine their own**.

#### Dimension 1: Current Usage ("Where do you sit?")

> "What AI tools do you currently use in your research software work?"

Present the spectrum levels (0-10) with RSQKit descriptions as reference. The user picks the level that matches their current practice.

| Level | RSQKit description (shown to user) |
|---|---|
| 0 | No Gen-AI usage — work without generative AI assistance |
| 1 | Conversational interaction — explanations, design trade-offs, conceptual help |
| 2 | Conversational artefact creation — small reviewable outputs in chat |
| 3 | Conversational creation with zip files — providing selected files for context |
| 4 | IDE autocomplete and inline suggestions — AI suggests code while editing |
| 5 | Editor-integrated local assistant — bounded edits inside the editor |
| 6 | Repository-aware assistance — AI can search and reason across the repo |
| 7 | Constrained local tool-using agents — agent edits files, runs commands, iterates |
| 8 | Managed or cloud coding agents — hosted agent works asynchronously |
| 9 | CI/PR/repository agents — agents integrated into shared project workflows |
| 10 | Open-ended autonomous agents — broad tool-using systems with persistence |

Source: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage

#### Dimension 2: Desired Intensity ("Where do you want to be?")

> "What level of AI autonomy do you want to work toward?"

Same spectrum presented. The skill asks follow-up questions to understand motivation:
- What tasks would benefit from more AI?
- What's holding you back from higher intensity?
- What would need to change for you to be comfortable at a higher level?

#### Dimension 3: Authorized Intensity ("Where should you be?")

> "What level of AI is allowed or authorized in your context?"

Explores external constraints:
- Does your project have an AI usage policy?
- Does your institution or funder have restrictions?
- Is there sensitive data that limits what can be shared with AI tools?
- Are there ethical or environmental considerations?

#### Dimension 4: Review Capacity (sustainability)

> "How much review capacity do you have? What are you comfortable reviewing?"

Explores the sustainability of the chosen intensity:
- Are you solo or on a team?
- How much time can you dedicate to reviewing AI-generated work?
- What types of changes are you comfortable reviewing?
- What would overwhelm your review capacity?

### Output: `ai-intensity.yaml`

See Section 5.3 for the file format. The skill generates this file after the Q&A, presents it to the user for review, and writes it only after explicit confirmation.

### Principles

1. **Self-determination** — the user decides, the skill facilitates
2. **Neutrality** — no level is presented as better than another
3. **RSQKit fidelity** — use RSQKit's own descriptions, don't paraphrase
4. **No detection** — never infer AI usage from repository files
5. **Persistence** — the profile is committed to the repo so collaborators and agents can respect it

---

## V1.1 — Quick Improvements (opencode skill, no CLI)

These improvements remain within the opencode skill scope (no external dependency) but significantly increase value:

### 1. RSQKit Tool Recommendations per Check

Each check in the report includes the **tools recommended by RSQKit for the detected language**, not just "add tests":

| Check | Python | R | JS/TS | C++ | Julia |
|---|---|---|---|---|---|
| Tests | pytest, hypothesis | testthat | jest, vitest | CTest, Google Test | Test.jl |
| Linting | ruff, mypy | lintr | eslint, prettier | clang-tidy | JuliaFormatter.jl |
| CI | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions |
| Packaging | pyproject.toml, hatch | devtools | npm publish | CMake, Conan | Pkg.jl |
| Docs | Sphinx, MkDocs | pkgdown | JSDoc, Docusaurus | Doxygen | Documenter.jl |

Source: https://everse.software/RSQKit/all_tools_and_resources

### 2. Tier Detection (three-tier model)

Already specified in section 3.1. Implementation in the skill via heuristics:
- Count source files (Glob)
- Check for packaging presence (Glob for pyproject.toml, package.json, etc.)
- Count authors via `git log --format='%aN' | sort -u | wc -l`
- Check for releases/tags presence via `git tag`

### 3. AI Intensity Profile Reader

Already specified in section 5.4. The skill reads `ai-intensity.yaml` (created by the separate AI Intensity Q&A skill) and presents it neutrally. No detection from repo files.

### 4. Remediation Chains

Already specified in section 7.3. Implementation: the skill proposes chains and guides step by step.

### 5. Embedded RSQKit Tool Tables

The SKILL.md embeds a reference table of RSQKit tools by language (condensed extract from https://everse.software/RSQKit/all_tools_and_resources). Allows the report to recommend the exact tool rather than generic advice.

### 6. Lifecycle Stage Detection

Heuristic detection of the repository's [lifecycle stage](https://everse.software/RSQKit/life_cycle):

| Stage | Heuristics | Prioritized recommendations |
|---|---|---|
| **Early** | < 10 commits, no tags, 1 author | Structure, LICENSE, .gitignore, README |
| **Active dev** | Regular commits, no CI | Tests, CI, documentation |
| **Maintenance** | Releases present, few recent commits | Future-proofing, dependency update, archiving |
| **Published** | DOI present, minimal activity | Verify citation is up to date, complete metadata |

---

## V2 — Specifications (overview)

### Python CLI

```bash
# Installation
pip install everse-scan

# Basic usage
everse-scan scan ./my-repo
everse-scan scan https://github.com/org/repo

# Modular usage
everse-scan scan ./my-repo --focus fair,security,ci-cd
everse-scan scan ./my-repo --format json,markdown
everse-scan scan ./my-repo --role rse  # adaptive report
everse-scan scan ./my-repo --tier auto  # automatic tier detection
everse-scan scan ./my-repo --funder horizon-europe  # funder alignment
everse-scan diff ./my-repo --baseline last-report.json  # re-scan + delta
```

### V2 — New Features

#### 1. 2D Prioritization (effort × impact)

The V2 report uses a 2D matrix instead of a simple list by effort:

```
          Impact →
           Low      Moderate   High     Critical
Effort   ┌─────────┬──────────┬─────────┬──────────┐
Low      │  skip   │  later   │ DO NOW  │ URGENT   │
         ├─────────┼──────────┼─────────┼──────────┤
Medium   │  skip   │  later   │ quick   │ priority │
         ├─────────┼──────────┼─────────┼──────────┤
High     │  skip   │  plan    │  plan   │ critical │
         └─────────┴──────────┴─────────┴──────────┘
```

Impact factors:
- **Security risk** (hardcoded secret = critical)
- **Software tier** (script: no codemeta; infrastructure: security mandatory)
- **Lifecycle stage** (pre-publication: citation urgent; maintenance: future-proofing)
- **Target role** (researcher: credit first; RSE: engineering first)
- **Funder requirements** (Horizon Europe: open access + FAIR mandatory)

#### 2. Lifecycle Stage Detection

Based on the [RSQKit lifecycle model](https://everse.software/RSQKit/life_cycle):
- Analyze git log (commit frequency, last activity)
- Detect releases/tags
- Detect DOI/publication
- Adapt recommendations to the stage

#### 3. Adaptive Role-based Reporting

| | Researcher who codes | RSE |
|---|---|---|
| **Tone** | Plain language, explanations | Technical, concise |
| **Priority** | Credit/citation first (LICENSE, CITATION.cff, DOI) | Engineering first (tests, CI, code review) |
| **Depth** | Executive summary + quick wins | Full technical details |
| **Examples** | Similar research software stories | Tool comparisons, CI matrix patterns |

#### 4. Re-scan and Progress Tracking

```bash
# First scan
everse-scan scan ./my-repo --save baseline.json

# After fixes
everse-scan scan ./my-repo --diff baseline.json
# → "7/10 checks pass (was 4/10). Improvements: LICENSE ✅, CITATION.cff ✅, CI ✅"
```

The diff report includes:
- Before/after score
- Newly passed checks
- Regressed checks (if applicable)
- Updated recommended next steps

#### 5. Integration with Existing FAIR Tools

Rather than duplicating checks, the CLI can integrate and orchestrate existing tools:

| Tool | What it checks | Integration |
|---|---|---|
| [howfairis](https://github.com/fair-software/howfairis) | FAIR principles (5 aspects) | `everse-scan scan --use howfairis` |
| [FAIR software checklist](https://fair-software.eu/) | FAIR checklist | Integrate results in the report |
| [cffconvert](https://github.com/citation-file-format/cffconvert) | CITATION.cff validation | Automatic check |
| [codemeta validator](https://codemeta.github.io/codemetar/) | codemeta.json validation | Automatic check |
| [GitHub security advisories](https://docs.github.com/en/code-security) | Vulnerable dependencies | Automatic check |

Benefits:
- Reduces false positives (proven tools)
- Credibility (not just "the AI says so")
- Less development effort

#### 6. Full Coverage of 35+ RSQKit Tasks

The V2 CLI embeds a local knowledge base (`rsqkit.yaml`) synchronized from the [RSQKit GitHub](https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages). Each RSQKit task has a corresponding check (deterministic or heuristic).

#### 7. Funder Alignment

Funder detection (Horizon Europe, NSF, Wellcome, etc.) from:
- README (grant mentions)
- `.zenodo.json` (grants field)
- `CITATION.cff` (grants field)

The report cross-references funder requirements with the repository state:
> "This project is funded by Horizon Europe. Requirements: open access code, FAIR, persistent DOI. **Missing**: no DOI, no explicit open source license."

### V2 Architecture

```
everse-scan/
├── pyproject.toml
├── src/
│   └── everse_scan/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point
│       ├── scanner.py          # Scan orchestration
│       ├── checks/             # Check modules by category
│       │   ├── fair.py
│       │   ├── cicd.py
│       │   ├── testing.py
│       │   ├── documentation.py
│       │   ├── security.py
│       │   ├── reproducibility.py
│       │   └── ...
│       ├── reporters/          # Report generators
│       │   ├── markdown.py
│       │   ├── json.py
│       │   ├── adaptive.py     # Adaptive by role (researcher/RSE)
│       │   └── diff.py         # Progress report (re-scan)
│       ├── knowledge/          # RSQKit knowledge base
│       │   ├── rsqkit.yaml     # Tasks, checks, links, tools by language
│       │   ├── sync.py         # Sync from RSQKit GitHub
│       │   └── funders.yaml    # Requirements by funder (Horizon Europe, NSF, etc.)
│       ├── languages/          # Multi-language detection
│       │   ├── detector.py
│       │   └── ...
│       ├── context/            # Contextual repository analysis
│       │   ├── tier.py         # Three-tier detection (script/tool/infrastructure)
│       │   ├── lifecycle.py    # Stage detection (early/active/maintenance/published)
│       │   └── funder.py       # Funder detection
│       └── integrations/       # External FAIR tools
│           ├── howfairis.py
│           ├── cffconvert.py
│           └── codemeta.py
├── .opencode/
│   └── skills/
│       └── everse-scan/
│           └── SKILL.md        # Skill that uses the CLI + enriches with AI
└── tests/
```

---

## RSQKit References

- **Home page**: https://everse.software/RSQKit/
- **Tasks**: https://everse.software/RSQKit/tasks
- **AI Guidance**: https://everse.software/RSQKit/ai
- **Spectrum of AI Intensity**: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- **Cross Cutting Practices**: https://everse.software/RSQKit/cross_cutting_practices
- **AI Intensity Considerations**: https://everse.software/RSQKit/ai_intensity_considerations
- **Three-tier model**: https://everse.software/RSQKit/three_tier_view
- **Lifecycle**: https://everse.software/RSQKit/life_cycle
- **Quality dimensions**: https://everse.software/RSQKit/quality_dimensions
- **All tools**: https://everse.software/RSQKit/all_tools_and_resources
- **Indicators**: https://everse.software/RSQKit/all_indicators
- **Research software stories**: https://everse.software/RSQKit/research_software_stories
- **GitHub source**: https://github.com/EVERSE-ResearchSoftware/RSQKit
- **RSQKit pages**: https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages

## External FAIR Tools (V2 Integration)

- **howfairis**: https://github.com/fair-software/howfairis
- **cffconvert**: https://github.com/citation-file-format/cffconvert
- **codemeta validator**: https://codemeta.github.io/codemetar/
- **FAIR software checklist**: https://fair-software.eu/

---

## Milestones

### M1 — opencode Skill V1 (MVP)

**Objective**: Functional opencode skill, 10 checks, structured Markdown report.

| Item | Detail |
|---|---|
| **Deliverable** | `.opencode/skills/everse-scan/SKILL.md` |
| **Checks** | 10 V1 checks (README, LICENSE, CITATION.cff, codemeta.json, tests, CI/CD, structure, docs, packaging, version control) |
| **Detection** | Multi-language (Python, R, C++, Julia, JS/TS) |
| **Report** | Markdown: executive summary + action plan + technical details + AI intensity profile (if present) |
| **Remediation** | Simple interactive menu (list of files to generate) |
| **Repositories** | Local + remote (GitHub URLs) |
| **Completion criterion** | Scan of a real Python repo → complete report generated in one session |

### M2 — V1.1: Skill Improvements (added value)

**Objective**: Enrich the V1 skill without moving to the CLI. Make the report truly actionable.

| Item | Detail |
|---|---|
| **Tier detection** | Heuristics script / tool-library / infrastructure |
| **RSQKit tools per check** | Embedded table (pytest, ruff, Sphinx, etc. by language) |
| **AI intensity** | Reads `ai-intensity.yaml` profile (from the AI Intensity Q&A skill). Presents neutrally. No detection from repo files. |
| **Contextual remediation** | Pre-fill CITATION.cff / codemeta.json from git log + README + LICENSE |
| **Remediation chains** | Citation chain, CI chain, metadata chain |
| **Lifecycle detection** | Early / active dev / maintenance / published |
| **Quality dimensions** | Scorecard reproducibility / maintainability / findability / trustworthiness |
| **Non-covered tasks** | Explicit disclosure of the 25+ non-evaluated RSQKit tasks |
| **Completion criterion** | Scan of a Python + R repo → report with detected tier, recommended tools, proposed chains, pre-filled CITATION.cff. AI intensity section reads profile if present. |

### M2b — AI Intensity Q&A Skill (separate skill)

**Objective**: Standalone opencode skill for self-determination of AI usage intensity per RSQKit spectrum.

| Item | Detail |
|---|---|
| **Deliverable** | `.opencode/skills/ai-intensity/SKILL.md` |
| **Q&A dimensions** | Current usage, desired intensity, authorized intensity, review capacity |
| **Output** | `ai-intensity.yaml` (AI Declaration Format conventions, separate from `aidecl.yaml`) |
| **Spectrum** | RSQKit 0-10 with full descriptions per level |
| **Principles** | Self-determination, neutrality, no detection from repo files |
| **Completion criterion** | User runs the Q&A → `ai-intensity.yaml` generated → `everse-scan` reads it and includes it neutrally in the report |

### M3 — Python CLI V2: Core

**Objective**: Functional Python CLI, deterministic checks, JSON + Markdown output.

| Item | Detail |
|---|---|
| **Deliverable** | `pip install everse-scan` |
| **Checks** | 10 V1 checks ported to deterministic Python + 7 V1.1 checks (static analysis, security, reproducible envs, code review, software identifiers, releasing, readable code) |
| **Detection** | Multi-language + tier + lifecycle |
| **Output** | `--format json,markdown` |
| **Architecture** | `src/everse_scan/` with `cli.py`, `scanner.py`, `checks/`, `reporters/`, `languages/` |
| **Knowledge base** | `rsqkit.yaml` (tasks, checks, links) — manual for M3 |
| **Completion criterion** | `everse-scan scan ./repo --format json` → valid JSON + readable Markdown, 17 checks |

### M4 — CLI V2: Adaptive Report + Re-scan

**Objective**: Adaptive role-based report, progress tracking, 2D prioritization.

| Item | Detail |
|---|---|
| **Role** | `--role rse` / `--role researcher` → tone, priorities, depth adapted |
| **Re-scan** | `--save baseline.json` + `--diff baseline.json` → before/after delta |
| **2D prioritization** | Effort × impact matrix (with risk, tier, lifecycle, role factors) |
| **Adaptive reporter** | `reporters/adaptive.py` + `reporters/diff.py` |
| **Completion criterion** | Baseline scan → fixes → re-scan → progress report shows "7/17 (was 4/17)" |

### M5 — CLI V2: FAIR Integrations + Full Coverage

**Objective**: Integrate existing FAIR tools, cover the 35+ RSQKit tasks.

| Item | Detail |
|---|---|
| **Integrations** | howfairis, cffconvert, codemeta validator, GitHub security advisories |
| **RSQKit coverage** | 35+ tasks → each task has a check (deterministic or heuristic) |
| **RSQKit sync** | `knowledge/sync.py` — automatic sync from RSQKit GitHub |
| **Completion criterion** | `everse-scan scan ./repo --use howfairis` → cross-referenced CLI + howfairis report, 35+ checks |

### M6 — CLI V2: Funder Compliance + Advanced Context

**Objective**: Funder alignment, grant detection, recommendations based on funder.

| Item | Detail |
|---|---|
| **Funder detection** | Horizon Europe, NSF, Wellcome (from README, .zenodo.json, CITATION.cff) |
| **Funder requirements** | `knowledge/funders.yaml` — requirements by funder |
| **Funder report** | "Funder compliance" section: funder requirements vs repository state |
| **Advanced tier** | Fine-grained detection + suppression of non-relevant checks |
| **Completion criterion** | Scan of a Horizon Europe repo → report shows "Missing: persistent DOI, open source license" per HE requirements |
