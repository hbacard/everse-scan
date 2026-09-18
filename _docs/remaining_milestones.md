# everse-scan — État d'avancement et milestones restantes

Dernière mise à jour : 2026-09-18
Branche courante : `feat/cli-python` (M3, à merger dans `main`)

## Git log

```
fbf63e0 M3: CLI Python V2 core — 17 checks déterministes (feat/cli-python)
c2fb1cd M2: enrichissements du skill — tier, lifecycle, outils, remédiation (main)
528f5b3 M1: skill opencode V1 (MVP) — 10 checks, rapport Markdown (main)
0a75bcd plan: enrichir V1/V1.1/V2 + ajouter milestones M1-M6 (main)
c7f0014 initial commit (main)
```

## Branche `feat/cli-python`

M3 a été développé sur la branche `feat/cli-python`. Elle doit être mergée dans `main` avant de continuer avec M4.

```bash
git checkout main
git merge feat/cli-python
```

---

## Milestones terminées

### M1 — Skill opencode V1 (MVP) ✅

**Commit** : `528f5b3` (branche `main`)

**Livrable** : `.opencode/skills/everse-scan/SKILL.md`

**Implémenté** :
- Skill opencode avec déclenchement naturel (description riche)
- 10 checks V1 : README, LICENSE, CITATION.cff, codemeta.json, Structure, Version control, Tests, Documentation, CI/CD, Packaging
- Détection multi-langage (Python, R, C++, Julia, JS/TS, Rust, Go, Java, Ruby)
- Support repos local + distant (clone GitHub)
- Template de rapport Markdown : résumé exécutif + plan d'action priorisé + détails techniques par tâche + AI spectrum
- Évaluation AI spectrum (0-10) avec indicateurs de détection
- Divulgation des tâches RSQKit non couvertes
- Menu de remédiation simple

### M2 — V1.1 : Améliorations du skill ✅

**Commit** : `c2fb1cd` (branche `main`)

**Implémenté** :
- Détection du tier (three-tier model) avec heuristiques (script / outil-bibliothèque / infrastructure) + adaptation des checks (N/A pour tier 1)
- Détection du lifecycle (early / active dev / maintenance / published) via git log
- Table des outils RSQKit par langage (pytest/ruff/Sphinx pour Python, testthat/lintr/pkgdown pour R, etc.)
- Guidance AI spectrum par niveau avec contenu détaillé (0, 1-3, 4-6, 7-9, 10) + cross-cutting practices + AI intensity considerations
- Dimensions de qualité : scorecard reproductibilité / maintenabilité / findability / trustworthiness / réutilisabilité
- Remédiation contextuelle : pré-fill CITATION.cff / codemeta.json depuis git log + README + LICENSE, avec flux prévisualisation → confirmation → écriture
- Chaînes de remédiation : chaîne citation (→ Zenodo → DOI), chaîne CI (→ linting → dependabot → PR template), chaîne metadata (→ .zenodo.json → validation)
- Template de rapport mis à jour avec toutes les nouvelles sections

### M3 — CLI Python V2 : Core ✅

**Commit** : `fbf63e0` (branche `feat/cli-python`)

**Implémenté** :
- CLI Python fonctionnel : `everse-scan scan ./repo --format json,markdown,both`
- 17 checks déterministes en Python : 10 V1 + 7 V1.1 (static analysis, security, reproducible envs, code review, software identifiers, releasing, readable code)
- Détection multi-langage (`languages/detector.py`) avec comptage par extension + fichiers de config + fichiers de version
- Tier detection (`context/tier.py`) avec heuristiques (nombre fichiers sources, packaging, auteurs git, tags, CI, Docker, docs)
- Lifecycle detection (`context/lifecycle.py`) via git log (commits, activité récente, tags, DOI)
- AI intensity detection (scanner.py) via indicateurs (.cursorrules, AGENTS.md, .opencode/, workflows AI, mentions README)
- Reporters : JSON structuré (`reporters/json.py`) + Markdown complet (`reporters/markdown.py`) avec résumé exécutif, dimensions de qualité, plan d'action, détails techniques, AI guidance
- Modèles de données (`models.py`) : CheckResult, ScanResult, CheckStatus (pass/warn/fail/na)
- Scanner orchestration (`scanner.py`) : orchestre les 17 checks + contexte + AI
- CLI entry point (`cli.py`) avec argparse, support GitHub URLs (clone temporaire), --format, --output, --version
- Architecture `src/everse_scan/` : `cli.py`, `scanner.py`, `checks/` (17 modules), `reporters/`, `languages/`, `context/`
- 15 tests passants avec fixtures (`tests/fixtures.py` : sample repo good practices + minimal repo)
- pyproject.toml avec hatchling build, entry point `everse-scan`, pytest config, ruff config
- Auto-scan validé sur le repo lui-même : 4/17 pass, 10 warn, 3 fail

**Architecture créée** :
```
src/everse_scan/
├── __init__.py
├── cli.py              # Entry point CLI (argparse, --format, --output)
├── scanner.py          # Orchestration du scan (17 checks + contexte + AI)
├── models.py           # CheckResult, ScanResult, CheckStatus
├── checks/             # 17 modules de checks déterministes
│   ├── readme.py
│   ├── license.py
│   ├── citation.py
│   ├── codemeta.py
│   ├── structure.py
│   ├── version_control.py
│   ├── tests.py
│   ├── documentation.py
│   ├── cicd.py
│   ├── packaging.py
│   ├── static_analysis.py
│   ├── security.py
│   ├── reproducible_envs.py
│   ├── code_review.py
│   ├── software_identifiers.py
│   ├── releasing.py
│   └── readable_code.py
├── reporters/
│   ├── json.py         # Sortie JSON structurée
│   └── markdown.py     # Sortie Markdown complète
├── languages/
│   └── detector.py     # Détection multi-langage
└── context/
    ├── tier.py          # Three-tier detection (script/tool/infrastructure)
    └── lifecycle.py     # Lifecycle detection (early/active/maintenance/published)
```

**Non implémenté dans M3 (à reporter)** :
- `knowledge/rsqkit.yaml` : base de connaissances RSQKit manuelle (tâches, checks, liens). Le plan prévoyait "manuelle pour M3" mais n'a pas été créée. Les URLs RSQKit sont actuellement hardcodées dans chaque check. À créer pour M5 (sync automatique).
- Tests pour les checks individuels (seuls les tests d'intégration scanner + reporters existent)

---

## Milestones restantes

### M4 — CLI V2 : Rapport adaptatif + Re-scan

**Objectif** : Rapport adaptatif par rôle, tracking de progression, priorisation 2D.

**À implémenter** :
- `--role rse` / `--role researcher` → ton, priorités, profondeur du rapport adaptés au rôle
  - Researcher : langage simple, crédit/citation en premier, résumé exécutif + quick wins
  - RSE : technique concis, engineering d'abord (tests, CI, code review), détails complets
- `--save baseline.json` : sauvegarder le résultat du scan comme baseline
- `--diff baseline.json` : re-scanner et comparer avec la baseline → delta avant/après
  - Le rapport de diff doit afficher : score avant/après, checks nouvellement passés, checks régressés, prochaines étapes mises à jour
  - Format : "7/17 (was 4/17). Improvements: LICENSE ✅, CITATION.cff ✅, CI ✅"
- Priorisation 2D : matrice effort × impact (avec facteurs risque, tier, lifecycle, rôle)
  - Facteurs d'impact : risque sécurité, tier de logiciel, stage de lifecycle, rôle cible, exigences funder
- Nouveaux fichiers à créer :
  - `src/everse_scan/reporters/adaptive.py` — reporter adaptatif par rôle
  - `src/everse_scan/reporters/diff.py` — reporter de progression (re-scan)
- Modifier `cli.py` pour ajouter `--role`, `--save`, `--diff`
- Tests pour le diff et le reporter adaptatif

**Critère de fin** : Scan baseline → corrections → re-scan → rapport de progression affiche "7/17 (was 4/17)"

### M5 — CLI V2 : Intégrations FAIR + Couverture complète

**Objectif** : Intégrer les outils FAIR existants, couvrir les 35+ tâches RSQKit.

**À implémenter** :
- Intégration [howfairis](https://github.com/fair-software/howfairis) : `everse-scan scan ./repo --use howfairis` → 5 principes FAIR
- Intégration [cffconvert](https://github.com/citation-file-format/cffconvert) : validation automatique CITATION.cff
- Intégration [codemeta validator](https://codemeta.github.io/codemetar/) : validation codemeta.json
- Intégration GitHub security advisories : dépendances vulnérables
- Couverture complète des 35+ tâches RSQKit : chaque tâche a un check (déterministe ou heuristique)
- `knowledge/` directory :
  - `knowledge/rsqkit.yaml` : base de connaissances (tâches, checks, liens, tools par langage) — manuelle puis sync
  - `knowledge/sync.py` : sync automatique depuis [GitHub RSQKit](https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages)
- `integrations/` directory :
  - `integrations/howfairis.py`
  - `integrations/cffconvert.py`
  - `integrations/codemeta.py`
- `--use` flag pour activer les intégrations externes

**Critère de fin** : `everse-scan scan ./repo --use howfairis` → rapport croisé CLI + howfairis, 35+ checks

### M6 — CLI V2 : Funder compliance + Contexte avancé

**Objectif** : Alignement funder, détection de grants, recommandations selon le funder.

**À implémenter** :
- Détection funder (Horizon Europe, NSF, Wellcome) depuis :
  - README (mentions de grants)
  - `.zenodo.json` (grants field)
  - `CITATION.cff` (grants field)
- `knowledge/funders.yaml` : exigences par funder (Horizon Europe : open access + FAIR + DOI, NSF, Wellcome)
- Section "Conformité funder" dans le rapport : croisement exigences funder vs état du repo
  - Ex : "Ce projet est financé par Horizon Europe. Manquant : DOI persistant, licence open source explicite."
- Tier avancé : détection fine + suppression de checks non pertinents selon le tier
- `context/funder.py` : détection du funder

**Critère de fin** : Scan d'un repo Horizon Europe → rapport affiche "Manquant : DOI persistant, licence open source" selon exigences HE

---

## Comment reprendre

1. Merger `feat/cli-python` dans `main` :
   ```bash
   git checkout main
   git merge feat/cli-python
   ```
2. Créer une branche pour M4 :
   ```bash
   git checkout -b feat/adaptive-reporting
   ```
3. Implémenter M4 (rapport adaptatif + re-scan + priorisation 2D)
4. Pause + commit
5. Continuer avec M5, puis M6

## Commandes utiles

```bash
# Installer en mode dev
uv pip install -e ".[dev]"

# Lancer les tests
python3 -m pytest tests/ -v

# Scanner un repo
everse-scan scan ./repo --format both -o report

# Scanner un repo GitHub
everse-scan scan https://github.com/org/repo --format markdown
```
