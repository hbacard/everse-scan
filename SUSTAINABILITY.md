# Software Sustainability Plan

Long-term plan for keeping `everse-scan` useful, maintainable, and funded.

## 1. Maintenance model

- **Governance**: single-maintainer project with an open contribution model
  (see `CONTRIBUTING.md`); code owners in `.github/CODEOWNERS`.
- **Versioning**: Semantic Versioning; releases tagged and published (GitHub
  releases → Zenodo).
- **Dependencies**: deliberately minimal (`PyYAML`); Dependabot keeps them
  updated; CI validates every change.

## 2. Funding & ownership

- Currently maintained by the author (CNRS/IJCLab) in the EVERSE/RSQKit
  ecosystem context.
- **Funding**: Horizon Europe (EVERSE project context); grant IDs to be
  recorded in `.zenodo.json` when available.
- Initial commit: 2026-09-17. No external dependencies on proprietary services
  to run the tool itself.

## 3. Community & knowledge transfer

- `README.md` — user documentation.
- `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md` — onboarding contributors.
- `CHANGELOG.md` — release history.
- Issue/PR templates — structured feedback loops.
- Documentation (`docs/`) including `docs/api.md` — reference material.

## 4. Future-proofing

- Pinned dependencies via lockfiles (`uv.lock`, `pdm.lock`).
- Continuous integration covering tests, linting, and packaging on the
  supported Python versions (3.12–3.13).
- Three-tier + lifecycle awareness keeps the tool relevant as projects evolve.

## 5. Risks & mitigation

| Risk | Mitigation |
|---|---|
| Maintainer unavailability | Clear docs + contribution guide; low bus factor accepted for a focused CLI |
| RSQKit references drift | Check URLs at release; planned knowledge-base auto-sync |
| Dependency rot | Minimal deps + Dependabot + CI |

## 6. Exit / handover plan

- Final release: archive the repository on Zenodo, ensure `CITATION.cff` and
  `codemeta.json` are complete, and transfer ownership or archive publicly so
  the tool remains citable and usable.

## 7. Metrics

- Active commits (≥ 1/month while in active dev).
- Open issues/PRs triaged within 30 days.
- Dependency updates merged/acknowledged quarterly.
