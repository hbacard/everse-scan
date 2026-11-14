# everse-scan — Milestones for Repository Improvement

> Generated from `everse-scan-report.md` (2026-11-14).
> Objective: resolve every **failing / warning** check in the report (1 ❌ + 15 ⚠️)
> and improve the failing RSQKit quality dimensions (**Reproducibility**, **Trustworthiness**).
> Scope: report weaknesses only (no roadmap features). Final tag: `v0.5.0`.
>
> Implementation progress is tracked in [`progression.md`](./progression.md).
>
> **Status: ALL MILESTONES COMPLETE (2026-11-14).**
> Result: baseline 17 Pass / 15 Warn / 1 Fail / 3 N/A → **34 Pass / 0 Warn / 0 Fail / 2 N/A** after the `v0.5.0` tag. All 16 previously non-passing checks resolved. Remaining N/A (computational workflows, software peer review) are out of scope by design.

Current baseline (report 2026-11-14): **20/36 Pass, 15 Warn, 1 Fail, 3 N/A**.

| RSQKit dimension | Baseline | Final (M1–M7) |
|---|---|---|
| Reproducibility | ❌ | ✅ |
| Maintainability | ⚠️ | ✅ |
| Findability | ⚠️ | ✅ |
| Trustworthiness | ❌ | ✅ |
| Reusability | ✅ | ✅ |

---

## M1 — Collaboration & code review (quick wins) ✅

**Objective**: Restore Code review, Contribution guidelines, Code of conduct, and Issue templates checks. Low effort, high impact (report Quick Wins).

| Item | Detail |
|---|---|
| **Deliverables** | `.github/CODEOWNERS`, `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` |
| **Checks fixed** | Code review, Contribution guidelines, Code of conduct, Issue templates |
| **RSQKit** | https://everse.software/RSQKit/code_review |
| **Completion criterion** | Re-scan → these 4 checks return **Pass** |

---

## M2 — Releasing & software identifiers ✅

**Objective**: Track version history, control the Zenodo deposit, and add a software identifier. Also moves Horizon Europe funder compliance toward 8/8.

| Item | Detail |
|---|---|
| **Deliverables** | `CHANGELOG.md` (Keep a Changelog, seeded from git history), `.zenodo.json` (project/authors metadata + placeholder `grants`), DOI `identifiers` field added to `CITATION.cff` and `codemeta.json` (backfilled by the v0.5.0 release in M7) |
| **Checks fixed** | Changelog, Releasing, Software identifiers, Funder compliance (DOI) |
| **RSQKit** | https://everse.software/RSQKit/releasing_software, https://everse.software/RSQKit/software_identifiers |
| **Completion criterion** | Re-scan → Changelog + Software identifiers **Pass**; funder compliance → 8/8 |

---

## M3 — CI/CD pipeline (structural ❌) ✅

**Objective**: Automated testing on every push/PR. The largest structural item (report Long Term) and the only ❌ check; also restores the **Reproducibility** and **Trustworthiness** dimensions.

| Item | Detail |
|---|---|
| **Deliverables** | `.github/workflows/ci.yml` — test (pytest + coverage), lint (ruff check + format), build/install check, Python 3.12–3.13 matrix, upload coverage artifact; `pytest.ini_options` coverage config |
| **Checks fixed** | CI/CD (plus Reproducibility, Trustworthiness dimensions) |
| **RSQKit** | https://everse.software/RSQKit/ci_cd |
| **Completion criterion** | Workflow green; re-scan → CI/CD **Pass** |

---

## M4 — Security & secret management ✅

**Objective**: Formalize vulnerability reporting and add secret detection to the development workflow.

| Item | Detail |
|---|---|
| **Deliverables** | `SECURITY.md` (supported versions, reporting policy), `.pre-commit-config.yaml` with **gitleaks** + ruff (check/format) hooks |
| **Checks fixed** | Security, Secret management |
| **RSQKit** | https://everse.software/RSQKit/research_software_security |
| **Completion criterion** | Re-scan → Security + Secret management **Pass** |

---

## M5 — Reproducibility, containers & sustainability docs ✅

**Objective**: Reproducible deployment via container, plus the reproducibility / data / sustainability documentation required at tier 2.

| Item | Detail |
|---|---|
| **Deliverables** | `Dockerfile`, `.dockerignore`, `REPRODUCIBILITY.md`, `DMP.md`, `SUSTAINABILITY.md` |
| **Checks fixed** | Containerization, Data management plan, Reproducibility checklist, Software sustainability plan |
| **RSQKit** | https://everse.software/RSQKit/using_containers, https://everse.software/RSQKit/reproducible_software_environments, https://everse.software/RSQKit/software_management_planning, https://everse.software/RSQKit/software_maintenance |
| **Completion criterion** | Re-scan → all four checks **Pass** |

---

## M6 — Developer experience & documentation ✅

**Objective**: Consistent editor settings and API/usage documentation.

| Item | Detail |
|---|---|
| **Deliverables** | `.editorconfig`, `docs/api.md` (CLI reference + programmatic/API overview) |
| **Checks fixed** | Readable code, API documentation |
| **RSQKit** | https://everse.software/RSQKit/writing_readable_code, https://everse.software/RSQKit/software_documentation |
| **Completion criterion** | Re-scan → Readable code + API documentation **Pass** |

---

## M7 — Verification & release (final) ✅

**Objective**: Confirm every previously-failing check now passes, release v0.5.0, and backfill the DOI.

| Item | Detail |
|---|---|
| **Deliverables** | Baseline re-scan + `--diff` report (`everse-scan . --save baseline.json` then re-scan), README badges updated (tests count, CI status), `docs/index.md` updated, git tag `v0.5.0` + GitHub release (triggers Zenodo DOI → backfill `CITATION.cff` / `codemeta.json` `identifier`), `progression.md` / `milestone.md` marked complete |
| **Checks fixed** | All 16 previously non-passing |
| **RSQKit** | https://everse.software/RSQKit/releasing_software |
| **Completion criterion** | Final re-scan → **36/36 Pass** (or only N/A remains); diff shows all 16 warnings/failures resolved |

---

## Out of scope (this cycle)

- N/A tasks (computational workflows, environmental sustainability, software peer review)
- Roadmap features (PyPI publication, RSQKit knowledge-base auto-sync, additional languages)
- `ai-intensity.yaml` profile (self-assessment — a user action, not a repo fix)
