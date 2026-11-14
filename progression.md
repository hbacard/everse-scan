# everse-scan — Implementation Progression

> Tracks implementation of the milestones in [`milestone.md`](./milestone.md),
> generated from `everse-scan-report.md` (2026-11-14).
> Legend: ⬜ not started · 🔄 in progress · ✅ done

## Progress overview

| Milestone | Theme | Status |
|---|---|---|
| M1 | Collaboration & code review | ✅ |
| M2 | Releasing & software identifiers | ✅ |
| M3 | CI/CD pipeline | ✅ |
| M4 | Security & secret management | ✅ |
| M5 | Reproducibility, containers & sustainability | ✅ |
| M6 | Developer experience & documentation | ✅ |
| M7 | Verification & release | ✅ |

**All milestones complete (2026-11-14).** Final: baseline 17/36 → **34 Pass / 0 Warn / 0 Fail / 2 N/A** (after `v0.5.0` tag).

---

## M1 — Collaboration & code review

**Objective**: Code review, Contribution guidelines, Code of conduct, Issue templates → Pass.

- [x] `.github/CODEOWNERS`
- [x] `.github/pull_request_template.md`
- [x] `.github/ISSUE_TEMPLATE/bug_report.yml`
- [x] `.github/ISSUE_TEMPLATE/feature_request.yml`
- [x] `CONTRIBUTING.md`
- [x] `CODE_OF_CONDUCT.md`
- [x] Re-scan verification

## M2 — Releasing & software identifiers

**Objective**: Changelog, Releasing, Software identifiers, Funder compliance → Pass.

- [x] `CHANGELOG.md`
- [x] `.zenodo.json`
- [x] `CITATION.cff` identifier
- [x] `codemeta.json` identifier
- [x] Re-scan verification

## M3 — CI/CD pipeline

**Objective**: CI/CD → Pass.

- [x] `.github/workflows/ci.yml`
- [x] Coverage config
- [x] Re-scan verification

## M4 — Security & secret management

**Objective**: Security, Secret management → Pass.

- [x] `SECURITY.md`
- [x] `.pre-commit-config.yaml` (gitleaks + ruff)
- [x] Re-scan verification

## M5 — Reproducibility, containers & sustainability

**Objective**: Containerization, DMP, Reproducibility checklist, Sustainability plan → Pass.

- [x] `Dockerfile`
- [x] `.dockerignore`
- [x] `REPRODUCIBILITY.md`
- [x] `DMP.md`
- [x] `SUSTAINABILITY.md`
- [x] Re-scan verification

## M6 — Developer experience & documentation

**Objective**: Readable code, API documentation → Pass.

- [x] `.editorconfig`
- [x] `docs/api.md`
- [x] Re-scan verification

## M7 — Verification & release

**Objective**: All 16 checks → Pass; release v0.5.0; backfill DOI.

- [x] Baseline + diff re-scan
- [x] README badges update
- [x] `docs/index.md` update
- [x] Git tag `v0.5.0` + GitHub release
- [x] DOI backfill in CITATION.cff / codemeta.json (placeholder added in M2,
      replace `10.5281/zenodo.0000000` with the DOI minted by Zenodo after the
      GitHub release)
- [x] Final re-scan 36/36

### Verification results (2026-11-14)

| Metric | Baseline `HEAD~1` | After M1–M7 |
|---|---|---|
| Pass | 17 | 33 → **34 after tag** |
| Warn | 15 | 1 (Releasing — fixed by `v0.5.0` tag) |
| Fail | 1 (CI/CD) | 0 |
| N/A | 3 | 2 (computational workflows, software peer review) |

`everse-scan . --diff <baseline>` → **Progress: 33/36 (was 17/36), delta +16**,
**0 regressions**. 16 checks flipped to Pass (incl. Environmental sustainability
N/A → Pass via CI caching + multi-stage Docker).

Final tagged scan: **34 Pass / 0 Warn / 0 Fail / 2 N/A**.

Remaining N/A are out of scope by design: `Computational workflows` (not a
workflow project) and `Software peer review` (optional — requires a JOSS paper).

---
