# EVERSE Scan Report

- **Repository**: everse-scan
- **Date**: 2026-11-14
- **Language(s) detected**: Python
- **Software tier**: Tool/Library (tier 2)
- **Lifecycle stage**: Active dev
- **AI Intensity Profile**: Not found
- **Funder**: Horizon Europe (confidence: low)

---

## 1. Executive Summary

### Strengths
- **README**: README found: README.md, quality score 4/4
- **LICENSE**: License file found: LICENSE (MIT)
- **CITATION.cff**: CITATION.cff found with all required fields
- **codemeta.json**: codemeta.json valid with all required fields
- **Structure**: Well-structured project with src/, tests/, and docs/
- **Version control**: Git repository (30 commits, 3 authors, 0 tags)
- **Tests**: Tests found (4 files, framework: pytest)
- **Documentation**: Good documentation coverage
- **Packaging**: Packaging well configured (pyproject.toml)
- **Static analysis**: Static analysis tools configured (ruff)
- **Reproducible environments**: Reproducible environment configured (uv.lock)
- **Authorship**: Authorship information found
- **ORCID**: ORCID references found in: CITATION.cff, codemeta.json
- **Dependency management**: Dependency management configured: Dependabot
- **Archiving**: Archiving indicators found: Zenodo DOI in README
- **Future proofing**: Good future proofing (3/3 indicators)
- **Software quality model**: Quality model reference found in README

### Weaknesses
- **CI/CD**: No CI/CD configuration found
- **Security**: Partial security configuration
- **Code review**: No code review practices found
- **Software identifiers**: Partial software identifiers
- **Releasing**: No releasing practices found
- **Readable code**: Partial formatting config (ruff)
- **Containerization**: No containerization files found
- **API documentation**: No API documentation found (OpenAPI/Swagger or docs/api)
- **Changelog**: No changelog file found
- **Contribution guidelines**: No CONTRIBUTING.md found
- **Code of conduct**: No CODE_OF_CONDUCT.md found
- **Issue templates**: No issue templates found
- **Secret management**: Partial secret management (1 indicator(s))
- **Data management plan**: No data management plan found
- **Reproducibility checklist**: No reproducibility checklist found
- **Software sustainability plan**: No sustainability plan found

### Overall Compliance

| Check | Status |
|-------|--------|
| README | ✅ Pass |
| LICENSE | ✅ Pass |
| CITATION.cff | ✅ Pass |
| codemeta.json | ✅ Pass |
| Structure | ✅ Pass |
| Version control | ✅ Pass |
| Tests | ✅ Pass |
| Documentation | ✅ Pass |
| CI/CD | ❌ Fail |
| Packaging | ✅ Pass |
| Static analysis | ✅ Pass |
| Security | ⚠️ Warn |
| Reproducible environments | ✅ Pass |
| Code review | ⚠️ Warn |
| Software identifiers | ⚠️ Warn |
| Releasing | ⚠️ Warn |
| Readable code | ⚠️ Warn |
| Authorship | ✅ Pass |
| ORCID | ✅ Pass |
| Dependency management | ✅ Pass |
| Containerization | ⚠️ Warn |
| Computational workflows | ⬜ N/A |
| API documentation | ⚠️ Warn |
| Changelog | ⚠️ Warn |
| Contribution guidelines | ⚠️ Warn |
| Code of conduct | ⚠️ Warn |
| Issue templates | ⚠️ Warn |
| Secret management | ⚠️ Warn |
| Data management plan | ⚠️ Warn |
| Reproducibility checklist | ⚠️ Warn |
| Archiving | ✅ Pass |
| Future proofing | ✅ Pass |
| Software sustainability plan | ⚠️ Warn |
| Environmental sustainability | ⬜ N/A |
| Software peer review | ⬜ N/A |
| Software quality model | ✅ Pass |

### Quality Dimensions (RSQKit mapping)

> Source: https://everse.software/RSQKit/all_indicators

| Dimension | Score | Checks involved |
|---|---|---|
| Reproducibility | ❌ | Packaging, Tests, CI/CD |
| Maintainability | ⚠️ | Structure, Documentation, Readable code |
| Findability | ⚠️ | CITATION.cff, codemeta.json, Software identifiers |
| Trustworthiness | ❌ | Tests, CI/CD, Version control, Security |
| Reusability | ✅ | LICENSE, README, Documentation |

### Detected Software Tier
**Tier**: Tool/Library (tier 2)
**Justification**: Packaging=yes, 3 author(s), tests=yes, source files=49

### Detected Lifecycle Stage
**Stage**: Active dev
**Justification**: Regular commits (30 in last 3 months, 30 total), active development

### Non-evaluated Tasks

> ⚠️ This scan evaluates 36 of the 35+ RSQKit tasks. The following tasks are **not** evaluated:
>
> - [Archiving software](https://everse.software/RSQKit/archiving_software)
> - [Future proofing](https://everse.software/RSQKit/future_proofing)
> - [Performance profiling](https://everse.software/RSQKit/performance_profiling_and_optimization)
> - [Environmental sustainability](https://everse.software/RSQKit/improving_environmental_sustainability)
> - [Computational workflows](https://everse.software/RSQKit/computational_workflows)
> - ... (see [complete list](https://everse.software/RSQKit/tasks))

---

## 2. Prioritized Action Plan

> Prioritization by effort × impact. Impact factors in risk, tier, lifecycle, and target role.

### Critical Risks (address first if detected)
- No critical risks detected

### Quick Wins (low effort, high impact)
1. Add a CODEOWNERS file for review accountability (cf. https://everse.software/RSQKit/research_software_security) — **impact: moderate**
1. Add a PR template (.github/pull_request_template.md) (cf. https://everse.software/RSQKit/code_review) — **impact: moderate**
1. Add .zenodo.json to control Zenodo deposition metadata (cf. https://everse.software/RSQKit/software_identifiers) — **impact: moderate**

### Medium Term (moderate effort, moderate impact)
1. Create version tags (git tag v0.1.0) (cf. https://everse.software/RSQKit/releasing_software)
1. Add an .editorconfig for consistent editor settings (cf. https://everse.software/RSQKit/writing_readable_code)
1. Add a Dockerfile for reproducible deployment (cf. https://everse.software/RSQKit/using_containers)
1. Add API documentation (OpenAPI spec or docs/api.md) (cf. https://everse.software/RSQKit/software_documentation)
1. Add a CHANGELOG.md to track version history (cf. https://everse.software/RSQKit/releasing_software)

### Long Term (high effort, structural impact)
1. Create a GitHub Actions workflow for automated testing (cf. https://everse.software/RSQKit/ci_cd)

---

## Funder Compliance

**Detected funder**: Horizon Europe
**Detection confidence**: low

### Requirements for Horizon Europe

| # | Requirement | Related check | Status | Mandatory |
|---|-------------|---------------|--------|-----------|
| 1 | Open source license (OSI-approved) | LICENSE | PASS | Yes |
| 2 | Persistent identifier (DOI) for the software | Software identifiers | WARN | Yes |
| 3 | CITATION.cff for proper attribution | CITATION.cff | PASS | Yes |
| 4 | codemeta.json for machine-readable metadata | codemeta.json | PASS | Yes |
| 5 | Public version control repository | Version control | PASS | Yes |
| 6 | Documentation for users and developers | Documentation | PASS | Yes |
| 7 | Dedicated LICENSE file (not just in pyproject.toml) | LICENSE | PASS | Yes |
| 8 | Archiving in Zenodo or similar | Archiving | PASS | Yes |

**Compliance**: 7/8 (88%) requirements met

### Missing mandatory requirements

- Persistent identifier (DOI) for the software

### Partially met requirements

- Persistent identifier (DOI) for the software

---

## 3. Technical Details by Task

### 3.1 README
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/creating_good_readme

**Findings**:
- Description present
- Installation instructions present
- Usage examples present
- License mentioned
- Badges present

---

### 3.2 LICENSE
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/licensing_software

**Findings**:
- SPDX identifier: MIT
- File: LICENSE

---

### 3.3 CITATION.cff
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/citing_software

**Findings**:
- Found fields: title, authors, date-released, version

---

### 3.4 codemeta.json
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/complete_software_metadata_codemeta

**Findings**:
- All required fields present

---

### 3.5 Structure
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_project_structure

**Findings**:
- Top-level directories: .github, .opencode, _docs, docs, src, tests
- src/ layout: yes
- tests/ directory: yes
- docs/ directory: yes

---

### 3.6 Version control
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/using_version_control

**Findings**:
- Commits: 30
- Authors: 3
- Tags/releases: 0
- .gitignore: present (6/7 common entries)

**Recommendations**:
- Create tags for version releases (git tag v0.1.0)

---

### 3.7 Tests
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/testing_software

**Findings**:
- Test files found: 4
- Test framework: pytest
- Tests directory: yes
- Coverage tool: coverage/pytest-cov

---

### 3.8 Documentation
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_documentation

**Findings**:
- docs/ directory: yes (1 files)
- Doc site configs: none
- Docstrings found: 202
- README: present (10578 chars)

**Recommendations**:
- Set up Sphinx or MkDocs for documentation generation

---

### 3.9 CI/CD
**Status**: ❌ Fail
**RSQKit**: https://everse.software/RSQKit/ci_cd

**Findings**:
- No .github/workflows/, .gitlab-ci.yml, Jenkinsfile, or other CI config found

**Recommendations**:
- Create a GitHub Actions workflow for automated testing

---

### 3.10 Packaging
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/packaging_software

**Findings**:
- pyproject.toml: build-system=True, name=True, version=True, scripts=True

---

### 3.11 Static analysis
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/static_analysis

**Findings**:
- Linting tools configured: ruff

---

### 3.12 Security
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/research_software_security

**Findings**:
- Secrets found: 0
- Dependabot: yes
- CODEOWNERS: no
- Security policy: no

**Recommendations**:
- Add a CODEOWNERS file for review accountability
- Add a SECURITY.md with vulnerability reporting instructions

---

### 3.13 Reproducible environments
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/reproducible_software_environments

**Findings**:
- Lockfiles: uv.lock
- Container files: none
- Nix: no

---

### 3.14 Code review
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/code_review

**Findings**:
- PR template: no
- CODEOWNERS: no
- CONTRIBUTING.md: no
- Issue templates: no

**Recommendations**:
- Add a PR template (.github/pull_request_template.md)
- Add a CODEOWNERS file for review accountability
- Add a CONTRIBUTING.md with contribution guidelines

---

### 3.15 Software identifiers
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_identifiers

**Findings**:
- .zenodo.json: no
- DOI in README: yes
- DOI in CITATION.cff: no

**Recommendations**:
- Add .zenodo.json to control Zenodo deposition metadata

---

### 3.16 Releasing
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/releasing_software

**Findings**:
- Git tags: 0 (none)
- Semantic versioning: no
- CHANGELOG: no
- Release template: no

**Recommendations**:
- Create version tags (git tag v0.1.0)
- Add a CHANGELOG.md to track release changes

---

### 3.17 Readable code
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/writing_readable_code

**Findings**:
- Formatters configured: ruff
- .editorconfig: no

**Recommendations**:
- Add an .editorconfig for consistent editor settings

---

### 3.18 Authorship
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/credit_recognition_research_software

**Findings**:
- CITATION.cff found (authors field)
- codemeta.json found (author field)

---

### 3.19 ORCID
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_metadata

**Findings**:
- ORCID found in CITATION.cff
- ORCID found in codemeta.json

---

### 3.20 Dependency management
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_maintenance

**Findings**:
- .github/dependabot.yml found

---

### 3.21 Containerization
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/using_containers

**Findings**:
- No Dockerfile or docker-compose found

**Recommendations**:
- Add a Dockerfile for reproducible deployment

---

### 3.22 Computational workflows
**Status**: ⬜ N/A
**RSQKit**: https://everse.software/RSQKit/computational_workflows

**Findings**:
- No .smk, .nf, .cwl, .ga files found

---

### 3.23 API documentation
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_documentation

**Findings**:
- No openapi.yaml/json, swagger.yaml/json, or docs/api.md found

**Recommendations**:
- Add API documentation (OpenAPI spec or docs/api.md)

---

### 3.24 Changelog
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/releasing_software

**Findings**:
- No CHANGELOG.md, CHANGES.md, or similar found

**Recommendations**:
- Add a CHANGELOG.md to track version history

---

### 3.25 Contribution guidelines
**Status**: ⚠️ Warn

**Findings**:
- No CONTRIBUTING.md or .github/CONTRIBUTING.md found

**Recommendations**:
- Add CONTRIBUTING.md with guidelines for contributors

---

### 3.26 Code of conduct
**Status**: ⚠️ Warn

**Findings**:
- No CODE_OF_CONDUCT.md found

**Recommendations**:
- Add CODE_OF_CONDUCT.md (see Contributor Covenant)

---

### 3.27 Issue templates
**Status**: ⚠️ Warn

**Findings**:
- No .github/ISSUE_TEMPLATE/ directory or templates

**Recommendations**:
- Add issue templates in .github/ISSUE_TEMPLATE/

---

### 3.28 Secret management
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/research_software_security

**Findings**:
- .env in .gitignore

**Recommendations**:
- Add .env to .gitignore
- Add gitleaks to pre-commit hooks

---

### 3.29 Data management plan
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_management_planning

**Findings**:
- No DMP.md or DATA_MANAGEMENT_PLAN.md found

**Recommendations**:
- Add a data management plan (DMP.md) if your software uses/produces data

---

### 3.30 Reproducibility checklist
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/reproducible_software_environments

**Findings**:
- No REPRODUCIBILITY.md or CHECKLIST.md found

**Recommendations**:
- Add a reproducibility checklist documenting how to reproduce results

---

### 3.31 Archiving
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/archiving_software

**Findings**:
- Zenodo/DOI reference in README

---

### 3.32 Future proofing
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/future_proofing

**Findings**:
- Lockfiles: uv.lock, pdm.lock
- .gitignore present
- Tests directory present

---

### 3.33 Software sustainability plan
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_maintenance

**Findings**:
- No SUSTAINABILITY.md or similar found

**Recommendations**:
- Add a sustainability plan (SUSTAINABILITY.md)

---

### 3.34 Environmental sustainability
**Status**: ⬜ N/A
**RSQKit**: https://everse.software/RSQKit/improving_environmental_sustainability

**Findings**:
- No CI caching, multi-stage Docker, or green computing files

---

### 3.35 Software peer review
**Status**: ⬜ N/A
**RSQKit**: https://everse.software/RSQKit/publishing_software

**Findings**:
- No JOSS paper, rOpenSci badge, or peer review reference

---

### 3.36 Software quality model
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/fair_rs

**Findings**:
- Quality model reference in README

---
