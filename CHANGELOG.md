# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Community & collaboration files: `CODEOWNERS`, pull request template, issue
  templates, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
- Continuous integration workflow (`.github/workflows/ci.yml`) running tests,
  linting, and build checks on Python 3.12–3.13.
- Security & secret management: `SECURITY.md` and a pre-commit configuration
  with gitleaks.
- Reproducibility & sustainability documentation: `Dockerfile`,
  `REPRODUCIBILITY.md`, `DMP.md`, `SUSTAINABILITY.md`.
- Developer experience: `.editorconfig`, `docs/api.md`.
- Metadata: `.zenodo.json`, DOI identifier in `CITATION.cff` and `codemeta.json`.

### Changed

- GitLab-hosted repositories are now fully supported, not just GitHub ones:
  - CI/CD: `.gitlab-ci.yml` content is analyzed for test/lint/matrix jobs, and
    Renovate is recognized as the GitLab dependency-update bot.
  - Remote URL scans use a full clone, so commit counts and release tags are
    accurate for GitHub and GitLab.
  - Collaboration & security: GitLab merge-request and issue templates
    (`.gitlab/merge_request_templates/`, `.gitlab/issue_templates/`) and
    CODEOWNERS (root/`docs/`/`.gitlab/`) are detected.
  - Layout conventions: `doc/`, `documentation/`, `documentations/` count as a
    docs directory; C++/CMake layouts (`source/`, `GTest/`, `example`) are
    recognized; `.cxx`/`.cc` test files detected with Google Test/CTest.
  - Generated/build/IDE output (`doxygen/`, `cmake-build-*`, `.idea`) is
    excluded from language, structure, test, security and docstring scans, so a
    C++ project with doxygen HTML is no longer misdetected as JavaScript.
  - `CeCILL` (and `CeCILL-B`) license text is now recognized in `LICENCE.txt`.
- Scan report reflects these fixes: verified on a real GitLab C++ repository
  (1598 commits) with language detection, license, tests and structure corrected.

## [0.5.0] - 2026-11-11

### Added

- `CITATION.cff` and `codemeta.json` with complete metadata and ORCID.
- Dependabot configuration for `pip` and `github-actions` dependencies.

### Changed

- License switched to MIT to match `pyproject.toml` and the README.
- README restructured as product-style documentation (pdm/uv install options,
  roles, diff example, development section, detailed architecture).
- All French content translated to English.
- Python badge updated to the supported range (3.12–3.13).

### Fixed

- Citation check parser (`CITATION.cff` fields).
- Report header fields rendered as markdown list items.
- Undefined name in one check; code formatted with ruff.

## [0.1.0] - 2026-09-18

### Added (development milestones, seeded from git history)

- **M1** — opencode skill V1: 10 determinizable checks, multi-language detection,
  Markdown report, AI intensity profile reader.
- **M2** — skill improvements: three-tier detection, lifecycle detection,
  per-language tool recommendations, quality dimensions, contextual remediation
  chains.
- **M3** — Python CLI core: 17 deterministic checks, multi-language + tier +
  lifecycle detection, JSON + Markdown reporters, `src/everse_scan/` architecture.
- **M4** — adaptive role-based reports (`--role`), re-scan with baseline diff
  (`--save`/`--diff`), 2D effort × impact prioritization.
- **M5** — FAIR integrations (howfairis, cffconvert, codemeta validator), 19
  extended checks (35+ RSQKit tasks), `--use` flag, RSQKit knowledge base.
- **M6** — funder compliance: funder detection (Horizon Europe, NSF, Wellcome,
  DFG, ANR, UKRI, Helmholtz), requirement profiles, funder compliance section.
