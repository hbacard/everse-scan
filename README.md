# everse-scan

Outil d'analyse de repositories de recherche qui génère un rapport structuré sur la qualité et la conformité du logiciel aux pratiques EVERSE/RSQKit.

> "Scanne mon repo, fais-moi un rapport structuré sur les points à améliorer en suivant les pratiques d'EVERSE dans le RSQKit."

## Statut

**V1 (MVP)** — Skill opencode fonctionnel avec 10 checks et rapport Markdown structuré.

## Ce que fait everse-scan

- Scanne un repo local ou distant (GitHub)
- Détecte le langage principal (Python, R, C++, Julia, JS/TS, et plus)
- Évalue 10 checks clés selon les pratiques RSQKit
- Évalue la position sur le spectrum AI du RSQKit (0-10)
- Génère un rapport Markdown structuré (résumé exécutif + plan d'action + détails techniques)
- Propose un menu de remédiation interactif

## Les 10 checks

| # | Check | RSQKit |
|---|---|---|
| 1 | README | [creating_good_readme](https://everse.software/RSQKit/creating_good_readme) |
| 2 | LICENSE | [licensing_software](https://everse.software/RSQKit/licensing_software) |
| 3 | CITATION.cff | [citing_software](https://everse.software/RSQKit/citing_software) |
| 4 | codemeta.json | [complete_software_metadata_codemeta](https://everse.software/RSQKit/complete_software_metadata_codemeta) |
| 5 | Structure du projet | [software_project_structure](https://everse.software/RSQKit/software_project_structure) |
| 6 | Version control | [using_version_control](https://everse.software/RSQKit/using_version_control) |
| 7 | Tests | [testing_software](https://everse.software/RSQKit/testing_software) |
| 8 | Documentation | [software_documentation](https://everse.software/RSQKit/software_documentation) |
| 9 | CI/CD | [ci_cd](https://everse.software/RSQKit/ci_cd) |
| 10 | Packaging | [packaging_software](https://everse.software/RSQKit/packaging_software) |

## Usage

En tant que skill opencode, everse-scan se déclenche naturellement quand vous demandez une analyse de repo :

- "Scanne mon repo"
- "Analyse la qualité de mon code"
- "Vérifie si mon projet respecte les pratiques FAIR"
- "Fais un audit EVERSE de mon repo"
- "everse-scan"

## Roadmap

| Milestone | Description |
|---|---|
| **M1** | Skill opencode V1 (MVP) — 10 checks, rapport Markdown |
| **M2** | V1.1 — Détection du tier, outils par langage, remédiation contextuelle |
| **M3** | CLI Python V2 — Checks déterministes, sortie JSON + Markdown |
| **M4** | CLI V2 — Rapport adaptatif par rôle, re-scan |
| **M5** | CLI V2 — Intégrations FAIR (howfairis, cffconvert) |
| **M6** | CLI V2 — Funder compliance |

Voir [_docs/plan.md](_docs/plan.md) pour le plan complet.

## Licence

MIT
