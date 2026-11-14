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
| M7 | Verification & release | 🔄 |

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

- [ ] Baseline + diff re-scan
- [ ] README badges update
- [ ] `docs/index.md` update
- [ ] Git tag `v0.5.0` + GitHub release
- [ ] DOI backfill in CITATION.cff / codemeta.json
- [ ] Final re-scan 36/36

---
