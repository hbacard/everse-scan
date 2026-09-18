# everse-scan

Outil d'analyse de repositories de recherche qui génère un rapport structuré sur la qualité et la conformité du logiciel aux pratiques EVERSE/RSQKit.

> "Scanne mon repo, fais-moi un rapport structuré sur les points à améliorer en suivant les pratiques d'EVERSE dans le RSQKit."

## Statut

**V2 (M3)** — CLI Python fonctionnel avec 17 checks déterministes, détection multi-langage, tier et lifecycle, sortie JSON + Markdown. Skill opencode également disponible.

## Installation

```bash
pip install -e .
```

Ou avec `uv` :

```bash
uv pip install -e ".[dev]"
```

## Usage

### CLI

```bash
# Scan local avec sortie Markdown (défaut)
everse-scan ./repo

# Scan avec sortie JSON
everse-scan ./repo --format json

# Les deux formats, sauvegardés dans des fichiers
everse-scan ./repo --format both -o report

# Scan d'un repo GitHub
everse-scan https://github.com/org/repo --format markdown
```

Options :
- `--format {json,markdown,both}` — format de sortie (défaut : markdown)
- `--output, -o` — fichier de sortie (défaut : stdout pour JSON, `everse-scan-report.md` pour Markdown)
- `--version` — afficher la version

### Skill opencode

everse-scan est aussi disponible comme skill opencode. Il se déclenche naturellement quand vous demandez une analyse de repo :

- "Scanne mon repo"
- "Analyse la qualité de mon code"
- "Vérifie si mon projet respecte les pratiques FAIR"
- "Fais un audit EVERSE de mon repo"

## Ce que fait everse-scan

- Scanne un repo local ou distant (GitHub)
- Détecte les langages présents (Python, R, C++, Julia, JS/TS, Rust, Go, Java, Ruby)
- Évalue 17 checks déterministes selon les pratiques RSQKit
- Détecte le tier du logiciel (script / outil-bibliothèque / infrastructure)
- Détecte le lifecycle (early / active dev / maintenance / published)
- Évalue la position sur le spectrum AI du RSQKit (0-10)
- Génère un rapport structuré (JSON et/ou Markdown) avec résumé exécutif, dimensions de qualité, plan d'action priorisé, détails techniques, guidance AI

## Les 17 checks

| # | Check | Catégorie | RSQKit |
|---|---|---|---|
| 1 | README | V1 | [creating_good_readme](https://everse.software/RSQKit/creating_good_readme) |
| 2 | LICENSE | V1 | [licensing_software](https://everse.software/RSQKit/licensing_software) |
| 3 | CITATION.cff | V1 | [citing_software](https://everse.software/RSQKit/citing_software) |
| 4 | codemeta.json | V1 | [complete_software_metadata_codemeta](https://everse.software/RSQKit/complete_software_metadata_codemeta) |
| 5 | Structure du projet | V1 | [software_project_structure](https://everse.software/RSQKit/software_project_structure) |
| 6 | Version control | V1 | [using_version_control](https://everse.software/RSQKit/using_version_control) |
| 7 | Tests | V1 | [testing_software](https://everse.software/RSQKit/testing_software) |
| 8 | Documentation | V1 | [software_documentation](https://everse.software/RSQKit/software_documentation) |
| 9 | CI/CD | V1 | [ci_cd](https://everse.software/RSQKit/ci_cd) |
| 10 | Packaging | V1 | [packaging_software](https://everse.software/RSQKit/packaging_software) |
| 11 | Static analysis | V1.1 | [static_analysis](https://everse.software/RSQKit/static_analysis) |
| 12 | Security | V1.1 | [security](https://everse.software/RSQKit/security) |
| 13 | Reproducible environments | V1.1 | [reproducible_envs](https://everse.software/RSQKit/reproducible_envs) |
| 14 | Code review | V1.1 | [code_review](https://everse.software/RSQKit/code_review) |
| 15 | Software identifiers | V1.1 | [software_identifiers](https://everse.software/RSQKit/software_identifiers) |
| 16 | Releasing | V1.1 | [releasing](https://everse.software/RSQKit/releasing) |
| 17 | Readable code | V1.1 | [readable_code](https://everse.software/RSQKit/readable_code) |

## Architecture

```
src/everse_scan/
├── cli.py              # Entry point CLI (argparse)
├── scanner.py          # Orchestration du scan (17 checks + contexte + AI)
├── models.py           # CheckResult, ScanResult, CheckStatus
├── checks/             # 17 modules de checks déterministes
├── reporters/          # Sortie JSON + Markdown
├── languages/          # Détection multi-langage
└── context/            # Tier detection + Lifecycle detection
```

## Roadmap

| Milestone | Statut | Description |
|---|---|---|
| **M1** | ✅ | Skill opencode V1 (MVP) — 10 checks, rapport Markdown |
| **M2** | ✅ | V1.1 — Détection du tier, lifecycle, outils par langage, remédiation contextuelle |
| **M3** | ✅ | CLI Python V2 — 17 checks déterministes, sortie JSON + Markdown, tier + lifecycle |
| **M4** | À faire | Rapport adaptatif par rôle, re-scan avec diff, priorisation 2D |
| **M5** | À faire | Intégrations FAIR (howfairis, cffconvert, codemeta validator) |
| **M6** | À faire | Funder compliance, détection de grants |

Voir [_docs/plan.md](_docs/plan.md) pour le plan complet et [_docs/remaining_milestones.md](_docs/remaining_milestones.md) pour l'état détaillé.

## Licence

MIT
