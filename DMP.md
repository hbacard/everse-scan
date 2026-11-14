# Data Management Plan (DMP)

Scope: the data that `everse-scan` **reads**, **produces**, and **stores**.

## 1. Data description

| Data | Format | Purpose |
|---|---|---|
| Input: target repositories | Source code (many languages) | Analysed by the 36 checks |
| Output: scan reports | Markdown / JSON | Quality & FAIR compliance results |
| Baseline files | JSON | Re-scan diffing (`--save` / `--diff`) |

`everse-scan` processes the repository **in place**; scan results are produced
on request and are not stored implicitly.

## 2. Data origin & collection

- **Input** is read from a local repository path or a temporary clone of a
  remote GitHub URL (deleted after the scan unless `--save` is used).
- **No data is collected or transmitted** by the tool; all checks run locally
  and deterministic outputs are written to user-specified files.

## 3. Storage & preservation

- Reports are transient artefacts owned by the user.
- The only durable, versioned "data" is the source code itself, archived via
  the project's Zenodo deposit (see `SUSTAINABILITY.md`).
- Temporary clones live in the system temp directory and are removed after use.

## 4. Access & sharing

- No personal or sensitive data is involved.
- Output reports can be shared openly as evidence of FAIR compliance (e.g.
  with collaborators or funders). The target repository's own license governs
  any redistribution of its content, not this tool's.

## 5. Security & privacy

- `everse-scan` never sends repository contents to a network service.
- External integrations (`--use howfairis`, `--use cffconvert`) run as local
  CLI tools; user discretion applies.
- See `SECURITY.md` for the project's security posture.

## 6. Retention & disposal

- Users control retention of generated reports/baselines.
- Project-internal convention: keep baseline JSON alongside the corresponding
  report for the duration of the improvement cycle.

## 7. Responsibilities

- Maintainers: keep the corpus of check logic and metadata current.
- Users: manage the outputs they generate.
