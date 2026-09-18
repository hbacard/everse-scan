---
name: everse-scan
description: >-
  Scanne un dépôt de code (local ou distant GitHub) et génère un rapport structuré
  sur la qualité et la conformité du logiciel aux pratiques EVERSE/RSQKit. Évalue 10
  checks clés (README, LICENSE, CITATION.cff, codemeta.json, structure, version control,
  tests, documentation, CI/CD, packaging), détecte le langage et le tier de logiciel,
  évalue le stage de lifecycle, le spectrum AI, les dimensions de qualité, et propose
  des actions de remédiation contextuelles. Se déclenche sur des demandes comme
  "scanne mon repo", "analyse la qualité de mon code", "vérifie les pratiques FAIR",
  "audit EVERSE", "everse-scan", ou toute demande d'analyse de qualité/conformité d'un
  dépôt logiciel de recherche.
---

# EVERSE Scan

Outil d'analyse de repositories de recherche qui génère un rapport structuré sur la qualité et la conformité du logiciel aux pratiques EVERSE/RSQKit.

> "Scanne mon repo, fais-moi un rapport structuré sur les points à améliorer en suivant les pratiques d'EVERSE dans le RSQKit."

## Public cible

Research Software Engineers (RSE) et chercheurs qui codent (researchers who code).

---

## Workflow

### Étape 1 — Identifier la cible

Déterminer ce qu'on scanne :

1. **Repo local** : chemin fourni par l'utilisateur ou répertoire courant (`.`)
2. **Repo GitHub distant** : URL au format `https://github.com/org/repo`

Si l'utilisateur fournit une URL GitHub, cloner temporairement :

```bash
git clone --depth 1 https://github.com/org/repo /tmp/everse-scan-<repo-name>
```

Puis analyser le repo cloné comme un repo local. Nettoyer le répertoire temporaire après l'analyse.

Si aucun chemin/URL n'est fourni et qu'aucun repo n'est évident dans le contexte, **demander avant de continuer**.

### Étape 2 — Détection multi-langage

Détecter le ou les langages principaux du repo en analysant :

**Fichiers de configuration** (via Glob) :
- `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt` → **Python**
- `package.json`, `tsconfig.json` → **JavaScript/TypeScript**
- `Cargo.toml` → **Rust**
- `DESCRIPTION`, `NAMESPACE` → **R**
- `Project.toml` → **Julia**
- `CMakeLists.txt`, `Makefile` → **C/C++**
- `go.mod` → **Go**
- `pom.xml`, `build.gradle` → **Java**
- `Gemfile` → **Ruby**

**Fichiers de version** (via Glob) :
- `.python-version` → Python
- `.ruby-version` → Ruby
- `.tool-versions`, `.node-version` → JS/TS

**Extensions de fichiers sources** (via Glob, compter les occurrences) :
- `.py` → Python, `.js`/`.ts`/`.jsx`/`.tsx` → JS/TS, `.R`/`.r` → R, `.jl` → Julia, `.c`/`.cpp`/`.h`/`.hpp` → C/C++, `.rs` → Rust, `.go` → Go, `.java` → Java, `.rb` → Ruby

Le rapport indique le langage principal (le plus de fichiers) et les langages secondaires détectés.

### Étape 3 — Détection du tier (three-tier model)

Le RSQKit définit un [modèle à trois tiers](https://everse.software/RSQKit/three_tier_view) : **scripts** → **outils/prototypes** → **infrastructure**. Un script d'analyse jetable et un framework HPC publié n'ont pas besoin des mêmes pratiques. Détecter le tier via des heuristiques (voir la section **Détection du tier** ci-dessous) et **adapter les checks pertinents**.

### Étape 4 — Détection du lifecycle

Détecter le [stage de lifecycle](https://everse.software/RSQKit/life_cycle) du repo (early / active dev / maintenance / published) via des heuristiques (voir la section **Détection du lifecycle** ci-dessous). Le lifecycle influence les recommandations priorisées.

### Étape 5 — Exécuter les 10 checks

Pour chaque check, utiliser les outils disponibles (Glob, Grep, Read, Bash) pour examiner le repo. Voir la section **Référentiel des 10 checks** ci-dessous pour les critères détaillés. Adapter les checks selon le tier détecté (certains checks sont supprimés ou atténués pour les scripts).

Pour chaque check, déterminer un statut :
- **PASS** : le check est satisfait
- **WARN** : partiellement satisfait, améliorations nécessaires
- **FAIL** : non satisfait ou absent

### Étape 6 — Évaluation AI spectrum

Évaluer la position du repo sur le spectrum d'intensité AI du RSQKit (0-10). Voir la section **AI Spectrum Assessment** ci-dessous. Le rapport inclut la guidance RSQKit associée au niveau détecté, pas juste le numéro.

### Étape 7 — Évaluer les dimensions de qualité

Calculer un scorecard par dimension de qualité (voir la section **Dimensions de qualité** ci-dessous). Les dimensions sont : reproductibilité, maintenabilité, findability, trustworthiness, réutilisabilité.

### Étape 8 — Générer le rapport

Générer le rapport en suivant strictement la structure du **Template de rapport** ci-dessous. Le rapport est écrit en Markdown et sauvegardé dans `everse-scan-report.md` à la racine du repo analysé (ou affiché si l'utilisateur préfère).

### Étape 9 — Menu de remédiation

À la fin du rapport, proposer un menu interactif listant les fichiers à générer (pré-remplis depuis le repo) et les chaînes de remédiation disponibles. Voir la section **Remédiation contextuelle et chaînes** ci-dessous.

---

## Référentiel des 10 checks

### Check 1 — README

**RSQKit** : https://everse.software/RSQKit/creating_good_readme

**Ce qu'on cherche** :
- Présence de `README.md` ou `README.rst` à la racine
- Qualité du contenu : description du projet, instructions d'installation, exemples d'usage, mention de la licence
- Présence de badges (CI, coverage, licence, DOI)

**Critères d'évaluation** :
- **PASS** : README présent avec description, installation, usage, et licence mentionnée
- **WARN** : README présent mais manque de sections clés (installation, usage, ou licence)
- **FAIL** : Aucun README trouvé

**Recommandations types** :
- Si FAIL : créer un README.md minimal (nom du projet, description brève, installation, usage, licence)
- Si WARN : compléter les sections manquantes

**Outils RSQKit recommandés** (selon langage) :
- Voir la section **Table des outils RSQKit par langage** — ligne "Docs"

---

### Check 2 — LICENSE

**RSQKit** : https://everse.software/RSQKit/licensing_software

**Ce qu'on cherche** :
- Présence d'un fichier `LICENSE`, `LICENSE.md`, `LICENCE`, `COPYING` à la racine
- Type de licence identifiable (SPDX identifier)
- Mention de la licence dans `pyproject.toml`, `package.json`, ou autre fichier de packaging

**Critères d'évaluation** :
- **PASS** : Fichier LICENSE présent avec licence reconnue (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, etc.)
- **WARN** : Licence mentionnée dans un fichier de config mais pas de fichier LICENSE dédié, ou licence non standard
- **FAIL** : Aucune information de licence

**Recommandations types** :
- Sans licence = non réutilisable juridiquement. C'est un **risque critique**.
- Si FAIL : ajouter un fichier LICENSE (recommander MIT ou Apache-2.0 pour du research software, sauf contrainte funder)

---

### Check 3 — CITATION.cff

**RSQKit** : https://everse.software/RSQKit/citing_software

**Ce qu'on cherche** :
- Présence de `CITATION.cff` à la racine
- Validité des champs requis : `title`, `authors`, `date-released`, `version`, `preferred-citation`
- Cohérence avec les auteurs git

**Critères d'évaluation** :
- **PASS** : CITATION.cff présent avec champs requis complétés
- **WARN** : CITATION.cff présent mais champs manquants ou incomplets
- **FAIL** : Aucun fichier CITATION.cff

**Recommandations types** :
- Si FAIL : créer un CITATION.cff minimal — pré-remplissable depuis `git log` + README + LICENSE (voir **Remédiation contextuelle**)
- Si WARN : compléter les champs manquants

---

### Check 4 — codemeta.json

**RSQKit** : https://everse.software/RSQKit/complete_software_metadata_codemeta

**Ce qu'on cherche** :
- Présence de `codemeta.json` à la racine
- Structure valide (JSON parsable)
- Champs requis : `@context`, `@type`, `name`, `author`, `description`, `license`, `codeRepository`
- Présence de `programmingLanguage`, `softwareVersion`, `developmentStatus`

**Critères d'évaluation** :
- **PASS** : codemeta.json présent avec champs requis et structure valide
- **WARN** : codemeta.json présent mais champs manquants ou structure incomplète
- **FAIL** : Aucun codemeta.json

**Recommandations types** :
- Si FAIL : créer un codemeta.json — pré-remplissable depuis CITATION.cff + pyproject.toml/package.json + dépendances (voir **Remédiation contextuelle**)
- Si WARN : compléter les champs manquants

---

### Check 5 — Structure du projet

**RSQKit** : https://everse.software/RSQKit/software_project_structure

**Ce qu'on cherche** (via Glob sur la racine) :
- Organisation des dossiers : présence de `src/`, `tests/`, `docs/`, `examples/`
- Séparation code/source vs configuration vs documentation
- Conventions par langage :
  - Python : `src/` layout (`src/package_name/`), `tests/` séparé
  - JS/TS : `src/` + `dist/`, `test/` ou `__tests__/`
  - R : `R/`, `tests/testthat/`, `vignettes/`, `man/`
  - C++ : `src/` + `include/`, `tests/`
  - Julia : `src/`, `test/`, `docs/`

**Critères d'évaluation** :
- **PASS** : Structure claire avec séparation code/tests/docs selon les conventions du langage
- **WARN** : Structure partiellement organisée (ex: tests présents mais pas de `src/`, ou docs mélangées au code)
- **FAIL** : Structure plate, tout à la racine, aucune organisation

**Recommandations types** :
- Si FAIL/WARN : réorganiser selon les conventions du langage détecté
- Référer à la page RSQKit pour les conventions spécifiques

---

### Check 6 — Version control

**RSQKit** : https://everse.software/RSQKit/using_version_control

**Ce qu'on cherche** (via Bash) :
- Présence de `.git/` (repo git)
- Présence de `.gitignore` et qualité (ignore les artefacts de build, venvs, etc.)
- Nombre de commits (`git rev-list --count HEAD`)
- Nombre d'auteurs (`git log --format='%aN' | sort -u | wc -l`)
- Présence de tags/releases (`git tag`)
- Branches (`git branch -a`)

**Critères d'évaluation** :
- **PASS** : Repo git avec `.gitignore` approprié, commits réguliers, tags/releases présents
- **WARN** : Repo git mais `.gitignore` manquant ou incomplet, ou aucun tag/release
- **FAIL** : Pas de repo git

**Recommandations types** :
- Si FAIL : initialiser git (`git init`), créer un `.gitignore` adapté au langage
- Si WARN : compléter le `.gitignore`, créer des tags pour les versions

---

### Check 7 — Tests

**RSQKit** : https://everse.software/RSQKit/testing_software

**Ce qu'on cherche** (selon le langage détecté) :
- **Python** : dossier `tests/`, fichiers `test_*.py` ou `*_test.py`, config `pytest` dans `pyproject.toml` ou `setup.cfg`, présence de `conftest.py`
- **R** : dossier `tests/testthat/`, fichiers `test-*.R` ou `testthat.R`
- **JS/TS** : dossier `test/` ou `__tests__/`, fichiers `*.test.js` ou `*.spec.js`, config dans `package.json` (`jest`, `vitest`, `mocha`)
- **C++** : `CMakeLists.txt` avec `enable_testing()`, fichiers `test_*.cpp`, usage de Google Test / Catch2
- **Julia** : dossier `test/`, fichier `runtests.jl`, usage de `Test.jl`

**Présence de coverage** :
- Python : `coverage`, `pytest-cov` dans les dépendances
- JS/TS : `nyc`, `c8`, ou config `collectCoverage` dans jest
- Général : présence de badges de coverage dans le README

**Critères d'évaluation** :
- **PASS** : Tests présents avec framework configuré, plusieurs fichiers de test
- **WARN** : Tests présents mais minimalistes (un seul fichier, pas de framework clair), ou framework mentionné mais peu de tests
- **FAIL** : Aucun test trouvé

**Recommandations types** :
- Si FAIL : créer un dossier `tests/` avec un premier test — utiliser le framework recommandé (voir **Table des outils** — ligne "Tests")
- Si WARN : étendre la couverture de test

---

### Check 8 — Documentation

**RSQKit** : https://everse.software/RSQKit/software_documentation

**Ce qu'on cherche** :
- Présence d'un dossier `docs/` avec du contenu (pas vide)
- Docstrings dans le code source (via Grep : `"""`, `/**`, `#'`, `//`)
- README comme documentation minimale (croisé avec Check 1)
- Site de documentation : `mkdocs.yml`, `conf.py` (Sphinx), `.readthedocs.yaml`, `docusaurus.config.js`, `_pkgdown.yml`
- Wiki GitHub (via API ou mention dans README)

**Critères d'évaluation** :
- **PASS** : Documentation dédiée (docs/ + site de doc) avec docstrings dans le code
- **WARN** : Documentation limitée au README uniquement, ou docstrings présents mais pas de docs/ dédié
- **FAIL** : Aucune documentation (pas même un README structuré)

**Recommandations types** :
- Si FAIL/WARN : créer un dossier `docs/`, ajouter des docstrings au code public
- Pour Python : recommander Sphinx ou MkDocs ; pour R : pkgdown ; pour JS : Docusaurus (voir **Table des outils** — ligne "Docs")

---

### Check 9 — CI/CD

**RSQKit** : https://everse.software/RSQKit/ci_cd

**Ce qu'on cherche** (via Glob) :
- **GitHub Actions** : `.github/workflows/*.yml`
- **GitLab CI** : `.gitlab-ci.yml`
- **Jenkins** : `Jenkinsfile`
- **CircleCI** : `.circleci/config.yml`
- **Travis** : `.travis.yml`
- **Azure Pipelines** : `azure-pipelines.yml`

**Qualité de la CI** :
- Présence de jobs de test
- Présence de jobs de linting/formatting
- Matrice de versions (ex: Python 3.11, 3.12, 3.13)
- Présence de Dependabot (`.github/dependabot.yml`)

**Critères d'évaluation** :
- **PASS** : CI/CD configuré avec jobs de test et linting
- **WARN** : CI/CD présent mais minimal (un seul job, pas de linting, pas de matrice)
- **FAIL** : Aucune configuration CI/CD

**Recommandations types** :
- Si FAIL : créer un workflow GitHub Actions basique (test selon langage détecté — voir **Table des outils** — ligne "CI")
- Si WARN : ajouter du linting (voir **Table des outils** — ligne "Linting"), étendre la matrice de versions

---

### Check 10 — Packaging

**RSQKit** : https://everse.software/RSQKit/packaging_software

**Ce qu'on cherche** (selon le langage détecté) :
- **Python** : `pyproject.toml` (recommandé), `setup.py`, `setup.cfg`, présence de `[build-system]`, entry points `[project.scripts]`
- **JS/TS** : `package.json` avec `name`, `version`, `main`/`exports`, `bin`
- **R** : `DESCRIPTION` avec `Package`, `Version`, `Imports`
- **Julia** : `Project.toml` avec `name`, `version`, `deps`
- **C++** : `CMakeLists.txt` avec `install()`, `CPack`, ou `Conan` (`conanfile.py`/`conanfile.txt`)
- **Rust** : `Cargo.toml` avec `[package]`
- **Docker** : `Dockerfile` ou `docker-compose.yml` (packaging par conteneur)

**Critères d'évaluation** :
- **PASS** : Packaging configuré correctement avec métadonnées complètes (nom, version, dépendances, entry points)
- **WARN** : Packaging basique présent (ex: `setup.py` minimal sans `pyproject.toml`, ou `package.json` sans `version`)
- **FAIL** : Aucune configuration de packaging

**Recommandations types** :
- Si FAIL : créer un fichier de packaging selon le langage (voir **Table des outils** — ligne "Packaging")
- Si WARN : migrer vers les standards modernes (pyproject.toml pour Python)

---

## Table des outils RSQKit par langage

Source : https://everse.software/RSQKit/all_tools_and_resources

Le rapport recommande l'outil exact pour le langage détecté plutôt qu'un conseil générique.

| Check / Catégorie | Python | R | JS/TS | C++ | Julia |
|---|---|---|---|---|---|
| **Tests** | pytest, hypothesis | testthat | jest, vitest | CTest, Google Test | Test.jl |
| **Linting** | ruff, mypy | lintr | eslint, prettier | clang-tidy | JuliaFormatter.jl |
| **Formatting** | ruff format, black | styler | prettier | clang-format | JuliaFormatter.jl |
| **CI** | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions |
| **Packaging** | pyproject.toml, hatch, uv | devtools | npm publish | CMake, Conan | Pkg.jl |
| **Docs** | Sphinx, MkDocs | pkgdown | JSDoc, Docusaurus | Doxygen | Documenter.jl |
| **Coverage** | pytest-cov, coverage | covr | nyc, c8 | gcov, lcov | Coverage.jl |
| **Security** | pip-audit, safety | oysteR | npm audit | trivy | Pkg.jl audit |
| **Repro envs** | uv.lock, poetry.lock, pip-tools | renv | package-lock.json | conan.lock | Manifest.toml |

---

## Détection du tier (three-tier model)

Source : https://everse.software/RSQKit/three_tier_view

Le RSQKit définit un modèle à trois tiers. Un script d'analyse jetable et un framework HPC publié n'ont pas besoin des mêmes pratiques. Détecter le tier via les heuristiques ci-dessous et **adapter les checks pertinents**.

### Heuristiques de détection

Pour détecter le tier, rassembler les signaux suivants (via Glob, Bash) :

- **Nombre de fichiers sources** (via Glob : `**/*.py`, `**/*.js`, etc., en excluant `.venv`, `node_modules`, `.git`, `__pycache__`, `dist`, `build`)
- **Présence de packaging** (via Glob : `pyproject.toml`, `package.json`, `Cargo.toml`, `DESCRIPTION`, `Project.toml`, `CMakeLists.txt`)
- **Nombre d'auteurs git** (via Bash : `git log --format='%aN' | sort -u | wc -l`)
- **Présence de tests** (via Glob : `tests/`, `test/`, `test_*.py`, etc.)
- **Présence de releases/tags** (via Bash : `git tag`)
- **Présence de CI** (via Glob : `.github/workflows/`, `.gitlab-ci.yml`, etc.)
- **Présence de Dockerfile** (via Glob : `Dockerfile`)
- **Présence de docs étendues** (via Glob : `docs/` avec plusieurs fichiers)

### Classification

| Tier | Heuristiques | Checks pertinents | Checks supprimés/atténués |
|---|---|---|---|
| **Script** (tier 1) | < 10 fichiers sources, pas de packaging, pas de tests, 1 auteur git, pas de releases | Version control, LICENSE, README, .gitignore | codemeta.json, CI testing matrices, containers, packaging |
| **Outil/Bibliothèque** (tier 2) | Packaging présent (pyproject.toml, package.json, etc.), > 1 auteur, tests présents ou recommandés, README structuré | Tous les 10 checks + recommandation citation, metadata, releasing | Infrastructure-level only |
| **Infrastructure** (tier 3) | Multi-package, CI complexe, Docker, docs étendues, nombreux contributeurs, releases taguées | Tous les 10 checks + recommandation security, reproducible envs, performance, future-proofing | Aucun — évaluation complète |

### Affichage dans le rapport

Le rapport affiche le tier détecté et justifie les checks ignorés :

> "Ce repo est détecté comme **script (tier 1)**. Les checks CI testing matrices, codemeta.json et containers ne sont pas pertinents à ce niveau. Voir le [modèle three-tier RSQKit](https://everse.software/RSQKit/three_tier_view)."

Pour un repo détecté comme tier 1 (script) :
- Les checks codemeta.json, CI/CD matrices, packaging et containers sont marqués **N/A** au lieu de FAIL
- Une note explique pourquoi ils ne sont pas pertinents
- Les recommandations se concentrent sur : LICENSE, README, .gitignore, version control

Pour un repo détecté comme tier 2 (outil/bibliothèque) :
- Tous les 10 checks sont évalués
- Recommandations supplémentaires : citation (CITATION.cff), metadata (codemeta.json), releasing (tags)

Pour un repo détecté comme tier 3 (infrastructure) :
- Tous les 10 checks sont évalués
- Recommandations supplémentaires : security, reproducible envs, performance, future-proofing (liens RSQKit vers ces tâches non couvertes)

---

## Détection du lifecycle

Source : https://everse.software/RSQKit/life_cycle

Détecter le stage du repo pour adapter les recommandations prioritaires.

### Heuristiques de détection

- **Commits** : `git rev-list --count HEAD` (nombre total)
- **Dernière activité** : `git log -1 --format=%cd --date=short` (date du dernier commit)
- **Releases/tags** : `git tag` (présence et nombre)
- **DOI** : présence de `.zenodo.json`, ou badge DOI dans README (via Grep)
- **Fréquence des commits récents** : `git log --since='3 months ago' --oneline | wc -l`

### Classification

| Stage | Heuristiques | Recommandations priorisées |
|---|---|---|
| **Early** | < 10 commits, pas de tags, 1 auteur | Structure, LICENSE, .gitignore, README |
| **Active dev** | Commits réguliers ( > 5 dans les 3 derniers mois), pas de CI ou CI minimale | Tests, CI, documentation |
| **Maintenance** | Releases/tags présents, peu de commits récents (< 5 dans les 3 derniers mois) | Future-proofing, dependency updates, archiving |
| **Published** | DOI présent, activité minimale | Vérifier citation à jour, metadata complète (codemeta.json) |

### Affichage dans le rapport

Le rapport affiche le stage détecté et l'utilise pour prioriser les recommandations du plan d'action :

> "Stage de lifecycle détecté : **Active dev**. Recommandations priorisées : tests, CI, documentation."

---

## Dimensions de qualité

Source : https://everse.software/RSQKit/all_indicators

Le rapport inclut un scorecard par dimension de qualité. Chaque dimension est évaluée en croisant les résultats des checks pertinents.

| Dimension | Checks impliqués | Évaluation |
|---|---|---|
| **Reproductibilité** | Packaging, Tests, CI/CD | ✅ si Packaging + CI/CD PASS ; ⚠️ si partiel ; ❌ si Packaging ou CI/CD FAIL |
| **Maintenabilité** | Structure, Documentation | ✅ si Structure + Documentation PASS ; ⚠️ si partiel ; ❌ si FAIL |
| **Findability** | CITATION.cff, codemeta.json | ✅ si CITATION.cff + codemeta.json PASS ; ⚠️ si partiel ; ❌ si FAIL |
| **Trustworthiness** | Tests, CI/CD, Version control | ✅ si Tests + CI/CD PASS ; ⚠️ si partiel ; ❌ si FAIL |
| **Réutilisabilité** | LICENSE, README, Documentation | ✅ si LICENSE + README PASS ; ⚠️ si partiel ; ❌ si LICENSE FAIL |

Le scorecard est affiché dans le rapport sous forme de tableau avec une note globale par dimension (✅/⚠️/❌).

---

## Tâches RSQKit non couvertes (divulgation)

> ⚠️ Ce scan évalue **10 des 35+ tâches RSQKit**. Les tâches suivantes ne sont **pas** évaluées :
>
> - [Static analysis](https://everse.software/RSQKit/static_analysis) — linters, formatters
> - [Software security](https://everse.software/RSQKit/research_software_security) — secrets, vulnérabilités
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments) — lockfiles, conteneurs
> - [Code review](https://everse.software/RSQKit/code_review) — PR templates, CODEOWNERS
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers) — DOI, Zenodo
> - [Releasing software](https://everse.software/RSQKit/releasing_software) — CHANGELOG, semantic versioning
> - [Writing readable code](https://everse.software/RSQKit/writing_readable_code) — conventions de formatting
> - [Archiving software](https://everse.software/RSQKit/archiving_software)
> - [Future proofing](https://everse.software/RSQKit/future_proofing)
> - [Performance profiling](https://everse.software/RSQKit/performance_profiling_and_optimization)
> - [Environmental sustainability](https://everse.software/RSQKit/improving_environmental_sustainability)
> - [Computational workflows](https://everse.software/RSQKit/computational_workflows)
> - ... (voir [liste complète](https://everse.software/RSQKit/tasks))

Un "pass" sur les 10 checks ne signifie pas que le repo respecte toutes les bonnes pratiques. Il signifie que les 10 checks évalués sont satisfaits.

---

## AI Spectrum Assessment

Le RSQKit définit un [spectrum d'intensité d'usage AI](https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage) de 0 à 10. Évaluer la position du repo sur ce spectrum.

### Indicateurs de détection

| Niveau | Intensité | Indicateurs à chercher dans le repo |
|---|---|---|
| 0 | No Gen-AI | Aucun indicateur AI trouvé |
| 1-3 | Conversational | Mentions de ChatGPT/Claude/Copilot dans README, docs, ou commits. Notes sur l'usage de prompts. Pas de config AI dans le repo. |
| 4-6 | IDE/Repo-aware | Présence de `.cursorrules`, `.github/copilot-instructions.md`, `AGENTS.md`, `.opencode/` directory, `CLAUDE.md`, `.aider*` configs |
| 7-9 | Agents | CI avec agents AI (GitHub Actions utilisant AI), `.github/workflows/*ai*` ou `*agent*`, bots de PR automatisés, config d'agents |
| 10 | Autonomous | Configuration complète d'agents autonomes, agents en production modifiant le code sans intervention humaine directe |

### Détection via Glob/Grep

- `.cursorrules` → niveau 4-6
- `.github/copilot-instructions.md` → niveau 4-6
- `AGENTS.md` → niveau 4-6
- `.opencode/` directory → niveau 4-6
- `CLAUDE.md` → niveau 4-6
- `.aider*` (`.aider.conf.yml`, `.aider.input.history`) → niveau 4-6
- Grep dans README/docs : "generated by", "AI-assisted", "ChatGPT", "Claude", "Copilot" → niveau 1-3
- `.github/workflows/` contenant des références à des API AI (OpenAI, Anthropic) → niveau 7-9
- Config d'agents autonomes → niveau 10

### Guidance par niveau (à inclure dans le rapport)

Le numéro (0-10) n'est qu'un point d'entrée. La **vraie valeur** est le contenu de guidance RSQKit associé à chaque niveau. Le rapport **doit** inclure la guidance correspondant au niveau détecté.

**Cross-cutting practices** (appliquables à tous les niveaux, toujours afficher) :
- Toujours relire le code généré par AI avant commit
- Garder le code AI dans des commits séparés pour l'auditabilité
- Documenter quels outils AI sont utilisés et comment
- Maintenir la capacité de rollback (version control + tests)
- Source : https://everse.software/RSQKit/cross_cutting_practices

| Niveau détecté | Guidance à afficher dans le rapport |
|---|---|
| **0** (No Gen-AI) | "Aucun usage d'AI détecté. C'est parfaitement valide. Si vous envisagez l'AI, commencez par le niveau 1 (conversationnel) pour des tâches ponctuelles. Voir [Conversational Interaction](https://everse.software/RSQKit/conversational_interaction)." |
| **1-3** (Conversational) | "Usage conversationnel détecté. Bon point de départ. **Risques** : pas de traçabilité du code généré, pas de contexte repo. **Qualité** : documentez vos prompts, committez séparément. Voir [Cross Cutting Practices](https://everse.software/RSQKit/cross_cutting_practices)." |
| **4-6** (IDE/Repo-aware) | "Assistant IDE/repo détecté (`.cursorrules`, `AGENTS.md`, `.opencode/`). **Risques** : confiance excessive dans le contexte repo, hallucinations sur API. **Qualité** : ajoutez des garde-fous dans les règles (ex: ne pas modifier les fichiers de config sans accord), maintenez des tests comme filet. Voir [Repository-aware assistance](https://everse.software/RSQKit/repository_aware_assistance)." |
| **7-9** (Agents) | "Agents CI/PR détectés. **Risques** : blast radius élevé, modifications automatisées sans revue. **Qualité** : exigez une revue humaine obligatoire sur tout PR généré par agent, limitez les permissions du bot, ajoutez des tests de non-régression. Voir [CI/PR/repository agents](https://everse.software/RSQKit/ci_pr_repository_agents)." |
| **10** (Autonomous) | "Agents autonomes détectés. **Risque maximal** : conséquences difficiles à prévoir, volume de modifications élevé. **Qualité** : garde-fous stricts obligatoires — tests exhaustifs, rollback automatique, monitoring, limites de scope. Voir [Open-ended autonomous agents](https://everse.software/RSQKit/open_ended_autonomous_agents)." |

### AI intensity considerations

Le rapport doit aussi indiquer *pourquoi* on pourrait vouloir monter ou descendre, pas juste le niveau actuel :
- **Monter** : tâches répétitives, documentation, tests → gain de temps
- **Descendre** : code critique pour résultats de recherche, sécurité, dépendances → risque trop élevé
- Source : https://everse.software/RSQKit/ai_intensity_considerations

### Ce que le rapport doit afficher

- Position actuelle estimée (niveau X / 10)
- Les indicateurs trouvés qui justifient cette estimation
- La guidance RSQKit associée au niveau (voir tableau ci-dessus)
- Les cross-cutting practices (toujours)
- Recommandations pour monter/descendre selon le contexte du projet
- Liens vers les pages RSQKit AI correspondantes

---

## Remédiation contextuelle (pré-fill)

La remédiation ne génère **pas des templates vierges**. Chaque fichier généré est **pré-rempli depuis le contenu réel du repo**.

### Sources de données pour pré-fill

| Fichier à générer | Source de données pour pré-fill | Commandes/outils |
|---|---|---|
| `CITATION.cff` | Auteurs via `git log --format='%aN <%aE>'`, titre depuis README H1, licence depuis LICENSE → SPDX, URL repo depuis `git remote -v`, version depuis dernier tag | Bash (git log, git remote, git tag) + Read (README) + Read (LICENSE) |
| `codemeta.json` | Idem CITATION.cff + dépendances depuis pyproject.toml/package.json, langage depuis détecteur, keywords depuis README | Bash (git) + Read (pyproject.toml/package.json) + Read (README) |
| `README.md` | Nom projet depuis repo dir, description depuis README existant (si partiel), section installation depuis deps détectés, section licence depuis LICENSE | Read (README existant) + Read (LICENSE) + Glob (deps) |
| `.github/workflows/test.yml` | Runner selon langage (pytest pour Python, `npm test` pour JS, CTest pour C++), version Python depuis `.python-version` ou `pyproject.toml` | Read (pyproject.toml) + Glob (.python-version) |
| `.gitignore` | Template selon langage détecté (Python → `__pycache__/`, `.venv/`, `*.pyc`, etc.) | Glob (langage détecté) |

### Flux de génération (trust + transparence)

1. **Prévisualiser** le contenu qui sera généré (avant d'écrire) — afficher le contenu à l'utilisateur
2. Demander **confirmation explicite** de l'utilisateur
3. **Écrire** le fichier
4. **Afficher** ce qui a été créé/modifié
5. Proposer le **prochain step** de la chaîne de remédiation (voir ci-dessous)

---

## Chaînes de remédiation

La génération d'un fichier n'est souvent que la première étape. Proposer des **chaînes** qui enchaînent les actions de remédiation de façon logique.

### Chaîne citation

```
1. Générer CITATION.cff (pré-rempli depuis git + README + LICENSE)
   → 2. Connecter le repo à Zenodo (GitHub integration)
   → 3. Créer une release (tag) pour déclencher le DOI Zenodo
   → 4. Ajouter le badge DOI dans le README
   → 5. Ajouter le DOI dans codemeta.json "identifier"
```

### Chaîne CI

```
1. Générer .github/workflows/test.yml (adapté au langage détecté)
   → 2. Ajouter un job de linting (ruff pour Python, eslint pour JS)
   → 3. Ajouter Dependabot (.github/dependabot.yml)
   → 4. Ajouter un PR template (.github/pull_request_template.md)
   → 5. Activer branch protection (instructions, pas automatisé)
```

### Chaîne metadata

```
1. Générer codemeta.json (pré-rempli depuis deps + langage + auteurs)
   → 2. Valider avec le validateur codemeta (lien: https://codemeta.github.io/codemetar/)
   → 3. Ajouter .zenodo.json pour contrôler le dépôt Zenodo
   → 4. Vérifier la cohérence CITATION.cff ↔ codemeta.json
```

---

## Template de rapport

Générer le rapport en suivant **strictement** cette structure. Le rapport est sauvegardé dans `everse-scan-report.md`.

```markdown
# EVERSE Scan Report

**Repository**: [nom du repo]
**Date**: [date du scan]
**Language(s) detected**: [langages détectés, langage principal en premier]
**Software tier**: [Script / Outil-Bibliothèque / Infrastructure]
**Lifecycle stage**: [Early / Active dev / Maintenance / Published]
**AI Intensity**: [niveau estimé] / 10 — [description courte]

---

## 1. Résumé exécutif

### Points forts
- [check] : [résumé positif]
- ...

### Points faibles
- [check] : [résumé du problème]
- ...

### Conformité globale

| Check | Statut |
|-------|--------|
| README | ✅ Pass / ⚠️ Warn / ❌ Fail |
| LICENSE | ... |
| CITATION.cff | ... |
| codemeta.json | ... |
| Structure | ... |
| Version control | ... |
| Tests | ... |
| Documentation | ... |
| CI/CD | ... |
| Packaging | ... |

### Dimensions de qualité (mapping RSQKit)
> Source : https://everse.software/RSQKit/all_indicators

| Dimension | Score | Checks impliqués |
|---|---|---|
| Reproductibilité | ✅ / ⚠️ / ❌ | Packaging, Tests, CI/CD |
| Maintenabilité | ✅ / ⚠️ / ❌ | Structure, Documentation |
| Findability | ✅ / ⚠️ / ❌ | CITATION.cff, codemeta.json |
| Trustworthiness | ✅ / ⚠️ / ❌ | Tests, CI/CD, Version control |
| Réutilisabilité | ✅ / ⚠️ / ❌ | LICENSE, README, Documentation |

### Tier de logiciel détecté
**Tier**: [Script / Outil-Bibliothèque / Infrastructure]
**Justification**: [heuristiques qui ont mené à cette classification]
**Checks ajustés**: [liste des checks marqués N/A et pourquoi]

### Stage de lifecycle détecté
**Stage**: [Early / Active dev / Maintenance / Published]
**Justification**: [heuristiques qui ont mené à cette classification]

### Tâches non évaluées

> ⚠️ Ce scan évalue 10 des 35+ tâches RSQKit. Les tâches suivantes ne sont **pas** évaluées :
> - [Static analysis](https://everse.software/RSQKit/static_analysis)
> - [Software security](https://everse.software/RSQKit/research_software_security)
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments)
> - [Code review](https://everse.software/RSQKit/code_review)
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers)
> - ... (voir [liste complète](https://everse.software/RSQKit/tasks))

---

## 2. Plan d'action priorisé

> Priorisation par effort × impact. L'impact facture le risque, le tier, le lifecycle et le rôle cible.

### Risques critiques (à traiter en priorité si détectés)
1. 🔴 [problème critique, ex: pas de LICENSE] — **impact: critique** ([raison])
2. ...

### Quick wins (faible effort, impact élevé)
1. [action, ex: Ajouter un CITATION.cff minimal] (cf. [lien RSQKit]) — **impact: élevé**
2. ...

### Moyen terme (effort modéré, impact modéré)
1. [action] (cf. [lien RSQKit])
2. ...

### Long terme (effort élevé, impact structurel)
1. [action] (cf. [lien RSQKit])
2. ...

---

## 3. Détails techniques par tâche

### 3.1 README
**Statut**: ✅ Pass / ⚠️ Warn / ❌ Fail
**RSQKit**: https://everse.software/RSQKit/creating_good_readme

**Constats**:
- [détail précis de ce qui a été trouvé/manque]

**Recommandations**:
- [action concrète recommandée]

**Outils RSQKit recommandés** (pour [langage détecté]):
- [outil 1] — [pourquoi]
- Voir : https://everse.software/RSQKit/[page]#tools

> 💡 Je peux générer un template de README amélioré si tu le souhaites.

---

### 3.2 LICENSE
**Statut**: ...
**RSQKit**: https://everse.software/RSQKit/licensing_software

**Constats**:
- ...

**Recommandations**:
- ...

---

[... répéter pour chaque check : CITATION.cff, codemeta.json, Structure, Version control, Tests, Documentation, CI/CD, Packaging ...]

---

## 4. AI Spectrum Assessment

**Position actuelle estimée**: Niveau X / 10 — [description]

**Analyse**:
- [indicateurs trouvés dans le repo justifiant le niveau]

**Guidance**:
[Insérer la guidance correspondant au niveau détecté depuis le tableau de la section AI Spectrum Assessment du SKILL.md]

**Cross-cutting practices** (applicables à tous les niveaux):
- Toujours relire le code généré par AI avant commit
- Garder le code AI dans des commits séparés pour l'auditabilité
- Documenter quels outils AI sont utilisés et comment
- Maintenir la capacité de rollback (version control + tests)

**Recommandations**:
- [suggestions pour ajuster l'intensité AI selon le contexte du projet]

**Références RSQKit**:
- https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- https://everse.software/RSQKit/cross_cutting_practices
- https://everse.software/RSQKit/ai_intensity_considerations

---

## 5. Remédiation

Je peux t'aider à corriger les problèmes identifiés. Voici ce que je peux faire :

📋 Fichiers à générer (pré-remplis depuis ton repo) :
  1. LICENSE ([type de licence suggéré])
  2. CITATION.cff (auteurs: [N] trouvés via git log)
  3. codemeta.json (deps: [N] depuis [fichier packaging], langage: [langage])
  4. .github/workflows/test.yml ([framework de test] pour [langage détecté])
  5. .gitignore (template [langage détecté])
  6. README.md ([si manquant ou incomplet])

🔗 Chaînes de remédiation disponibles :
  A. Chaîne citation → CITATION.cff → Zenodo → DOI → README badge
  B. Chaîne CI → workflow → linting → dependabot → PR template
  C. Chaîne metadata → codemeta.json → .zenodo.json → validation

Dis-moi ce que tu veux faire (numéro, lettre, ou "tout").
```

---

## Règles de remédiation

- Seulement proposer les fichiers pertinents aux checks qui ont FAIL ou WARN
- Seulement proposer les chaînes pertinentes au tier et lifecycle détectés
  - Tier 1 (script) : pas de chaîne metadata, pas de chaîne CI (pas pertinent)
  - Tier 2 (outil) : toutes les chaînes pertinentes
  - Tier 3 (infrastructure) : toutes les chaînes + recommandations security/reproducible envs
- Ne pas générer sans confirmation explicite de l'utilisateur
- Toujours prévisualiser le contenu avant d'écrire (afficher le fichier qui sera créé)
- Après génération d'un fichier, proposer le prochain step de la chaîne
- Pré-remplir avec les données du repo (auteurs git, nom du projet, langage détecté, dépendances, licence)
- Si l'utilisateur demande "tout", générer les fichiers un par un avec prévisualisation + confirmation pour chacun

---

## Références RSQKit

- **Page d'accueil** : https://everse.software/RSQKit/
- **Tâches** : https://everse.software/RSQKit/tasks
- **AI Guidance** : https://everse.software/RSQKit/ai
- **Spectrum of AI Intensity** : https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- **Cross Cutting Practices** : https://everse.software/RSQKit/cross_cutting_practices
- **AI Intensity Considerations** : https://everse.software/RSQKit/ai_intensity_considerations
- **Three-tier model** : https://everse.software/RSQKit/three_tier_view
- **Lifecycle** : https://everse.software/RSQKit/life_cycle
- **Quality dimensions** : https://everse.software/RSQKit/quality_dimensions
- **All indicators** : https://everse.software/RSQKit/all_indicators
- **All tools and resources** : https://everse.software/RSQKit/all_tools_and_resources
- **Conversational Interaction** : https://everse.software/RSQKit/conversational_interaction
- **Repository-aware assistance** : https://everse.software/RSQKit/repository_aware_assistance
- **CI/PR/repository agents** : https://everse.software/RSQKit/ci_pr_repository_agents
- **Open-ended autonomous agents** : https://everse.software/RSQKit/open_ended_autonomous_agents
- **Source GitHub** : https://github.com/EVERSE-ResearchSoftware/RSQKit
