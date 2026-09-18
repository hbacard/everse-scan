---
name: everse-scan
description: >-
  Scanne un dépôt de code (local ou distant GitHub) et génère un rapport structuré
  sur la qualité et la conformité du logiciel aux pratiques EVERSE/RSQKit. Évalue 10
  checks clés (README, LICENSE, CITATION.cff, codemeta.json, structure, version control,
  tests, documentation, CI/CD, packaging), détecte le langage, évalue le spectrum AI,
  et propose des actions de remédiation. Se déclenche sur des demandes comme
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

### Étape 3 — Exécuter les 10 checks

Pour chaque check, utiliser les outils disponibles (Glob, Grep, Read, Bash) pour examiner le repo. Voir la section **Référentiel des 10 checks** ci-dessous pour les critères détaillés.

Pour chaque check, déterminer un statut :
- **PASS** : le check est satisfait
- **WARN** : partiellement satisfait, améliorations nécessaires
- **FAIL** : non satisfait ou absent

### Étape 4 — Évaluation AI spectrum

Évaluer la position du repo sur le spectrum d'intensité AI du RSQKit (0-10). Voir la section **AI Spectrum Assessment** ci-dessous.

### Étape 5 — Générer le rapport

Générer le rapport en suivant strictement la structure du **Template de rapport** ci-dessous. Le rapport est écrit en Markdown et sauvegardé dans `everse-scan-report.md` à la racine du repo analysé (ou affiché si l'utilisateur préfère).

### Étape 6 — Menu de remédiation

À la fin du rapport, proposer un menu interactif simple listant les fichiers qui pourraient être générés pour corriger les problèmes identifiés. Voir la section **Menu de remédiation** ci-dessous.

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
- Si FAIL : créer un CITATION.cff minimal (title, authors depuis `git log`, version depuis dernier tag)
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
- Si FAIL : créer un codemeta.json (générable depuis CITATION.cff et pyproject.toml/package.json)
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
- Si FAIL : créer un dossier `tests/` avec un premier test (framework selon langage)
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
- Pour Python : recommander Sphinx ou MkDocs ; pour R : pkgdown ; pour JS : Docusaurus

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
- Si FAIL : créer un workflow GitHub Actions basique (test selon langage détecté)
- Si WARN : ajouter du linting, étendre la matrice de versions

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
- Si FAIL : créer un fichier de packaging selon le langage (pyproject.toml pour Python)
- Si WARN : migrer vers les standards modernes (pyproject.toml pour Python)

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
| 7-9 | Agents | CI avec agents AI (GitHub Actions utilisant AI), `.github/workflows/*ai*` ou `*agent*`, bots de PR automatisés, config d'agents (ex: `.github/dependabot.yml` ne compte pas, mais des workflows utilisant des API AI oui) |
| 10 | Autonomous | Configuration complète d'agents autonomes, agents en production modifiant le code sans intervention humaine directe, mentions d'agents autonomes dans la doc |

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

### Ce que le rapport doit afficher

- Position actuelle estimée (niveau X / 10)
- Les indicateurs trouvés qui justifient cette estimation
- Lien vers https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage

---

## Template de rapport

Générer le rapport en suivant **strictement** cette structure. Le rapport est sauvegardé dans `everse-scan-report.md`.

```markdown
# EVERSE Scan Report

**Repository**: [nom du repo]
**Date**: [date du scan]
**Language(s) detected**: [langages détectés, langage principal en premier]
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

> Priorisation par effort × impact. L'impact facture le risque et le rôle cible.

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

**Références RSQKit**:
- https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- https://everse.software/RSQKit/cross_cutting_practices
```

---

## Menu de remédiation

À la fin du rapport (après la section 4), afficher le menu interactif suivant, adapté aux problèmes trouvés :

```
---

## 5. Remédiation

Je peux t'aider à corriger les problèmes identifiés. Voici les fichiers que je peux générer :

📋 Fichiers à générer :
  1. LICENSE ([type de licence suggéré])
  2. CITATION.cff ([nombre d'auteurs trouvés via git log])
  3. codemeta.json ([langage détecté])
  4. .github/workflows/test.yml ([framework de test pour le langage détecté])
  5. .gitignore ([template pour le langage détecté])
  6. README.md ([si manquant ou incomplet])

Dis-moi ce que tu veux faire (numéro du fichier, ou "tout").
```

**Règles de remédiation** :
- Seulement proposer les fichiers pertinents aux checks qui ont FAIL ou WARN
- Ne pas générer sans confirmation explicite de l'utilisateur
- Après génération d'un fichier, proposer le prochain step logique
- Pré-remplir avec les données du repo quand possible (auteurs git, nom du projet, langage détecté)

---

## Références RSQKit

- **Page d'accueil** : https://everse.software/RSQKit/
- **Tâches** : https://everse.software/RSQKit/tasks
- **AI Guidance** : https://everse.software/RSQKit/ai
- **Spectrum of AI Intensity** : https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- **Cross Cutting Practices** : https://everse.software/RSQKit/cross_cutting_practices
- **All indicators** : https://everse.software/RSQKit/all_indicators
- **All tools and resources** : https://everse.software/RSQKit/all_tools_and_resources
- **Source GitHub** : https://github.com/EVERSE-ResearchSoftware/RSQKit
