# everse-scan

Outil d'analyse de repositories de recherche qui génère un rapport structuré sur la qualité et la conformité du logiciel aux pratiques EVERSE/RSQKit.

> "Scanne mon repo, fais-moi un rapport structuré sur les points à améliorer en suivant les pratiques d'EVERSE dans le RSQKit."

## Statut

**v0.5.0** — CLI Python complet avec 36 checks déterministes (35+ tâches RSQKit), intégrations FAIR optionnelles (+7 checks), détection de funder avec conformité, rapport adaptatif par rôle, re-scan avec diff, priorisation 2D, tier et lifecycle detection, sortie JSON + Markdown. 99 tests.

## Installation

```bash
pip install -e .
```

Ou avec `uv` :

```bash
uv pip install -e ".[dev]"
```

## Usage

### Scan basique

```bash
# Sortie Markdown (défaut)
everse-scan ./repo

# Sortie JSON
everse-scan ./repo --format json

# Les deux formats
everse-scan ./repo --format both -o report
```

### Rapport adaptatif par rôle

```bash
# Vue researcher (langage simple, citation/credit d'abord)
everse-scan ./repo --role researcher

# Vue RSE (technique, engineering d'abord)
everse-scan ./repo --role rse
```

### Re-scan avec diff

```bash
# 1. Sauvegarder un baseline
everse-scan ./repo --save baseline.json --format json

# 2. Après corrections, comparer avec le baseline
everse-scan ./repo --diff baseline.json
```

Exemple de sortie de diff :

```
Progress: 7/36 (was 4/36), delta +3

## Improvements
- LICENSE: WARN -> PASS
- CITATION.cff: FAIL -> PASS
- CI/CD: FAIL -> PASS
```

### Intégrations FAIR

```bash
# Activer howfairis, cffconvert, codemeta validator (+7 checks)
everse-scan ./repo --use

# Ou spécifier une intégration particulière
everse-scan ./repo --use howfairis
```

### Scan d'un repo GitHub

```bash
everse-scan https://github.com/org/repo --format markdown
```

### Options

| Option | Description |
|--------|-------------|
| `--format {json,markdown,both}` | Format de sortie (défaut: markdown) |
| `--output, -o` | Fichier de sortie |
| `--role {default,researcher,rse}` | Adapter le rapport à un rôle |
| `--save BASELINE` | Sauvegarder le scan comme baseline |
| `--diff BASELINE` | Comparer avec un baseline précédent |
| `--use [INTEGRATIONS]` | Activer les intégrations FAIR |
| `--version` | Afficher la version |

### Skill opencode

everse-scan est aussi disponible comme skill opencode. Il se déclenche naturellement :

- "Scanne mon repo"
- "Analyse la qualité de mon code"
- "Vérifie si mon projet respecte les pratiques FAIR"
- "Fais un audit EVERSE de mon repo"

## Ce que fait everse-scan

- Scanne un repo local ou distant (GitHub)
- Détecte les langages (Python, R, C++, Julia, JS/TS, Rust, Go, Java, Ruby)
- Évalue 36 checks déterministes couvrant 35+ tâches RSQKit
- Détecte le tier (script / outil-bibliothèque / infrastructure)
- Détecte le lifecycle (early / active dev / maintenance / published)
- Détecte le funder (Horizon Europe, NSF, Wellcome, DFG, ANR, UKRI, Helmholtz)
- Vérifie la conformité aux exigences du funder détecté
- Évalue la position sur le spectrum AI (0-10)
- Génère un rapport structuré avec résumé exécutif, dimensions de qualité, plan d'action priorisé (effort x impact), détails techniques, guidance AI, conformité funder
- Rapport adaptatif par rôle (researcher / RSE)
- Re-scan avec diff de progression

## Les 36 checks

### Core checks (M3 — 17 checks)

| # | Check | RSQKit |
|---|---|---|
| 1 | README | [creating_good_readme](https://everse.software/RSQKit/creating_good_readme) |
| 2 | LICENSE | [licensing_software](https://everse.software/RSQKit/licensing_software) |
| 3 | CITATION.cff | [citing_software](https://everse.software/RSQKit/citing_software) |
| 4 | codemeta.json | [complete_software_metadata_codemeta](https://everse.software/RSQKit/complete_software_metadata_codemeta) |
| 5 | Structure | [software_project_structure](https://everse.software/RSQKit/software_project_structure) |
| 6 | Version control | [using_version_control](https://everse.software/RSQKit/using_version_control) |
| 7 | Tests | [testing_software](https://everse.software/RSQKit/testing_software) |
| 8 | Documentation | [software_documentation](https://everse.software/RSQKit/software_documentation) |
| 9 | CI/CD | [ci_cd](https://everse.software/RSQKit/ci_cd) |
| 10 | Packaging | [packaging_software](https://everse.software/RSQKit/packaging_software) |
| 11 | Static analysis | [static_analysis](https://everse.software/RSQKit/static_analysis) |
| 12 | Security | [research_software_security](https://everse.software/RSQKit/research_software_security) |
| 13 | Reproducible environments | [reproducible_software_environments](https://everse.software/RSQKit/reproducible_software_environments) |
| 14 | Code review | [code_review](https://everse.software/RSQKit/code_review) |
| 15 | Software identifiers | [software_identifiers](https://everse.software/RSQKit/software_identifiers) |
| 16 | Releasing | [releasing_software](https://everse.software/RSQKit/releasing_software) |
| 17 | Readable code | [writing_readable_code](https://everse.software/RSQKit/writing_readable_code) |

### Extended checks (M5 — 19 checks)

| # | Check | Catégorie |
|---|---|---|
| 18 | Authorship | FAIR |
| 19 | ORCID | FAIR |
| 20 | Dependency management | Engineering |
| 21 | Containerization | Engineering |
| 22 | Computational workflows | Engineering |
| 23 | API documentation | Engineering |
| 24 | Changelog | Documentation |
| 25 | Contribution guidelines | Documentation |
| 26 | Code of conduct | Documentation |
| 27 | Issue templates | Documentation |
| 28 | Secret management | Security |
| 29 | Data management plan | Reproducibility |
| 30 | Reproducibility checklist | Reproducibility |
| 31 | Archiving | Sustainability |
| 32 | Future proofing | Sustainability |
| 33 | Software sustainability plan | Sustainability |
| 34 | Environmental sustainability | Sustainability |
| 35 | Software peer review | Quality |
| 36 | Software quality models | Quality |

### FAIR integrations (M5 — +7 checks with `--use`)

| Check | Source |
|-------|--------|
| FAIR: repository | [howfairis](https://github.com/fair-software/howfairis) |
| FAIR: license | howfairis |
| FAIR: registry | howfairis |
| FAIR: citation | howfairis |
| FAIR: checklist | howfairis |
| CITATION.cff validation | [cffconvert](https://github.com/citation-file-format/cffconvert) |
| codemeta.json validation | [codemeta validator](https://codemeta.github.io/) |

## Architecture

```
src/everse_scan/
├── cli.py              # CLI entry point (argparse)
├── scanner.py          # Orchestration du scan
├── models.py           # CheckResult, ScanResult, CheckStatus
├── priorities.py        # Priorisation 2D (effort x impact)
├── checks/             # 17 core checks + 19 extended checks
│   ├── readme.py
│   ├── license.py
│   ├── ...
│   └── extended.py      # 19 checks étendus (M5)
├── reporters/          # JSON, Markdown, Adaptive, Diff, Funder
│   ├── json.py
│   ├── markdown.py
│   ├── adaptive.py      # Rapport par rôle (--role)
│   ├── diff.py          # Re-scan avec diff (--save/--diff)
│   └── funder.py        # Conformité funder
├── integrations/       # howfairis, cffconvert, codemeta
├── knowledge/          # rsqkit.py (35+ tasks), funders.py (funder profiles)
├── languages/          # Détection multi-langage
└── context/            # Tier, Lifecycle, Funder detection
    ├── tier.py
    ├── lifecycle.py
    └── funder.py
```

## Développement

```bash
# Installer en mode dev
uv pip install -e ".[dev]"

# Lancer les tests
python3 -m pytest tests/ -v

# Lancer un scan sur le repo lui-même
everse-scan . --format both -o report
```

## Roadmap

| Milestone | Statut | Description |
|---|---|---|
| **M1** | Done | Skill opencode V1 (MVP) — 10 checks, rapport Markdown |
| **M2** | Done | V1.1 — Tier, lifecycle, outils par langage, remédiation contextuelle |
| **M3** | Done | CLI Python V2 — 17 checks déterministes, JSON + Markdown |
| **M4** | Done | Rapport adaptatif par rôle, re-scan avec diff, priorisation 2D |
| **M5** | Done | Intégrations FAIR (howfairis, cffconvert, codemeta), 35+ tâches RSQKit |
| **M6** | Done | Funder compliance, détection de grants, conformité funder |

Voir [_docs/plan.md](_docs/plan.md) pour le plan complet.

## Licence

MIT
