# Plan : everse-scan

## Vision

`everse-scan` est un outil d'analyse de repositories de recherche qui génère un rapport structuré sur la qualité et la conformité du logiciel aux pratiques EVERSE/RSQKit. L'objectif est d'aider les ingénieurs logiciel de recherche et les chercheurs qui codent à améliorer leurs projets selon les standards de la communauté.

> "Scanne mon repo, fais-moi un rapport structuré sur les points à améliorer en suivant les pratiques d'EVERSE dans le RSQKit."

---

## Roadmap

### V1 — Skill/Agent opencode

| Aspect | Décision |
|---|---|
| **Forme** | Skill opencode (analyse directe depuis la session IA conversationnelle) |
| **Portée** | Cœur FAIR + qualité de base (10 checks) |
| **Format rapport** | Markdown structuré (`everse-scan-report.md`) |
| **Méthodologie** | Analyse par l'IA : lecture de fichiers (Read, Glob, Grep) + interprétation contextuelle |
| **Structure rapport** | Résumé exécutif + Plan d'action priorisé + Détails techniques par tâche avec liens RSQKit |
| **Invocation** | Déclenchement naturel (description du skill) |
| **Source RSQKit** | Connaissances embarquées dans le SKILL.md |
| **Public** | Research Software Engineers + Researchers who code |
| **Remédiation** | Diagnostic + invitation interactive à la génération |
| **Repos** | Local + distant (GitHub URLs) |
| **Langages** | Multi-langage (détection Python, R, C++, Julia, etc.) |
| **AI spectrum** | Évaluation de la position du repo sur le spectrum 0-10 du RSQKit |

### V2 — CLI + Skill hybride

| Aspect | Décision |
|---|---|
| **Forme** | CLI Python (checks déterministes) + skill opencode (enrichissement IA) |
| **Portée** | Modulaire / à la carte (`--focus fair,security,ci-cd`) |
| **Méthodologie** | Checks Bash/Python déterministes + IA hybride |
| **Source RSQKit** | Base locale YAML + sync optionnel depuis [GitHub RSQKit](https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages) |
| **Rapport** | Adaptatif (résumé exécutif pour PI/researcher + détails techniques pour RSE) |
| **Invocation** | Commande explicite, contextuelle, avec arguments |
| **Portée tâches** | Toutes les tâches RSQKit (35+) |
| **Remédiation** | Phasé : diagnostic → templates → génération avec accord utilisateur |

---

## V1 — Spécifications détaillées

### 1. Skill opencode

#### 1.1 Description (déclenchement naturel)

Le skill se déclenche quand l'utilisateur demande une analyse de repo, de qualité logicielle, de conformité FAIR, etc. Exemples de phrases déclenchantes :

- "Scanne mon repo"
- "Analyse la qualité de mon code"
- "Vérifie si mon projet respecte les pratiques FAIR"
- "Fais un audit EVERSE de mon repo"
- "everse-scan"

#### 1.2 Référentiel RSQKit embarqué

Le SKILL.md embarque pour chacun des 10 checks :

- **Nom de la tâche** et lien vers la page RSQKit correspondante
- **Critères d'évaluation** (que chercher dans le repo)
- **Niveaux de conformité** (pass / warn / fail)
- **Recommandations types** selon le statut

### 2. Les 10 checks V1

| # | Check | RSQKit page | Ce qu'on cherche |
|---|---|---|---|
| 1 | **README** | `/creating_good_readme` | Présence du README.md, qualité du contenu (description, installation, usage, licence), badges |
| 2 | **LICENSE** | `/licensing_software` | Présence d'un fichier LICENSE, type de licence (SPDX), compatibilité |
| 3 | **Citation** | `/citing_software` | Présence de CITATION.cff, validité, champs requis |
| 4 | **CodeMeta** | `/complete_software_metadata_codemeta` | Présence de codemeta.json, structure, champs requis |
| 5 | **Structure du projet** | `/software_project_structure` | Organisation des dossiers (src/, tests/, docs/, etc.), conventions |
| 6 | **Version control** | `/using_version_control` | Utilisation de git, .gitignore, nombre de commits, branches, tags/releases |
| 7 | **Tests** | `/testing_software` | Présence de tests (tests/, pytest, unittest, etc.), framework, couverture |
| 8 | **Documentation** | `/software_documentation` | Présence de docs/, docstrings, README, site de doc |
| 9 | **CI/CD** | `/ci_cd` | Présence de .github/workflows/, .gitlab-ci.yml, Jenkinsfile, etc. |
| 10 | **Packaging** | `/packaging_software` | pyproject.toml, setup.py, Dockerfile, package.json, etc. |

### 3. Détection multi-langage

Le skill détecte le langage principal du repo en analysant :

- Les fichiers de configuration (`pyproject.toml` → Python, `package.json` → JS/TS, `Cargo.toml` → Rust, `DESCRIPTION` → R, `Project.toml` → Julia, `CMakeLists.txt` → C/C++, etc.)
- L'extension des fichiers sources
- La présence de `.python-version`, `.ruby-version`, `.tool-versions`, etc.

Les checks s'adaptent au langage détecté (ex: pour Python → pytest, pour R → testthat, pour C++ → CTest, etc.).

### 4. Support des repos distants

- **Repo local** : le skill analyse le répertoire courant ou un chemin fourni
- **Repo GitHub distant** : le skill clone temporairement le repo (via `git clone` dans le répertoire temporaire) puis l'analyse comme un repo local
- **Détection de l'URL** : `https://github.com/org/repo` → clone + scan

### 5. Évaluation AI spectrum (RSQKit)

Le skill évalue où se situe le repo sur le spectrum d'intensité AI (0-10) du RSQKit :

| Niveau | Intensité | Indicateurs dans le repo |
|---|---|---|
| 0 | No Gen-AI | Aucun usage d'AI |
| 1-3 | Conversational | Présence de prompts, notes sur usage ChatGPT/Claude |
| 4-6 | IDE/Repo-aware | .cursorrules, copilot config, opencode config, AGENTS.md, .opencode/ |
| 7-9 | Agents | CI avec agents AI, GitHub Actions AI, configuration d'agents |
| 10 | Autonomous | Agents autonomes, configuration complète d'agents ouverts |

Le rapport inclut :
- Position actuelle estimée sur le spectrum
- Recommandations pour monter/descendre d'intensité selon le contexte du projet
- Lien vers les pages RSQKit AI correspondantes

### 6. Structure du rapport Markdown

```markdown
# EVERSE Scan Report

**Repository**: [nom du repo]
**Date**: [date]
**Language(s) detected**: [langages]
**AI Intensity**: [niveau estimé] / 10

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
| README | ✅ Pass |
| LICENSE | ⚠️ Warn |
| CITATION.cff | ❌ Fail |
| ... | ... |

---

## 2. Plan d'action priorisé

### Quick wins (< 1h, impact immédiat)
1. Ajouter un fichier LICENSE (cf. https://everse.software/RSQKit/licensing_software)
2. Créer un CITATION.cff minimal (cf. https://everse.software/RSQKit/citing_software)
...

### Moyen terme (1-4h)
1. Mettre en place une CI/CD basique (cf. https://everse.software/RSQKit/ci_cd)
2. Ajouter des tests unitaires (cf. https://everse.software/RSQKit/testing_software)
...

### Long terme (> 4h, structurel)
1. Restructurer le projet selon les conventions (cf. https://everse.software/RSQKit/software_project_structure)
2. Créer une documentation complète (cf. https://everse.software/RSQKit/software_documentation)
...

---

## 3. Détails techniques par tâche

### 3.1 README
**Statut**: ✅ Pass / ⚠️ Warn / ❌ Fail
**RSQKit**: https://everse.software/RSQKit/creating_good_readme

**Constats**:
- [détail précis de ce qui a été trouvé/manque]

**Recommandations**:
- [action concrète recommandée]

> 💡 Je peux générer un template de README amélioré si tu le souhaites.

---

### 3.2 LICENSE
...

---

## 4. AI Spectrum Assessment

**Position actuelle estimée**: Niveau X / 10 — [description]

**Analyse**:
- [indicateurs trouvés dans le repo]

**Recommandations**:
- [suggestions pour ajuster l'intensité AI]

**Références RSQKit**:
- https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- https://everse.software/RSQKit/cross_cutting_practices
```

### 7. Remédiation interactive

À la fin du rapport, le skill propose une remédiation interactive :

```
Je peux t'aider à corriger les problèmes identifiés :
1. Générer un fichier CITATION.cff
2. Créer un fichier codemeta.json
3. Ajouter une GitHub Action basique pour les tests
4. Créer un template de README amélioré

Dis-moi ce que tu veux faire, ou tape "tout" pour tout générer.
```

---

## Architecture du skill V1

```
.opencode/skills/everse-scan/
├── SKILL.md              # Instructions du skill + référentiel RSQKit embarqué
└── (pas de dépendances externes en V1)
```

Le SKILL.md contiendra :
1. **Description** (pour le déclenchement naturel)
2. **Workflow** (étapes d'analyse)
3. **Référentiel des 10 checks** (critères, niveaux, recommandations)
4. **Template de rapport** (structure Markdown)
5. **AI spectrum** (critères d'évaluation 0-10)
6. **Instructions de remédiation interactive**

---

## V2 — Spécifications (vue d'ensemble)

### CLI Python

```bash
# Installation
pip install everse-scan

# Usage basique
everse-scan scan ./mon-repo
everse-scan scan https://github.com/org/repo

# Usage modulaire
everse-scan scan ./mon-repo --focus fair,security,ci-cd
everse-scan scan ./mon-repo --format json,markdown
everse-scan scan ./mon-repo --role rse  # rapport adaptatif
```

### Architecture V2

```
everse-scan/
├── pyproject.toml
├── src/
│   └── everse_scan/
│       ├── __init__.py
│       ├── cli.py              # Point d'entrée CLI
│       ├── scanner.py          # Orchestration du scan
│       ├── checks/             # Modules de checks par catégorie
│       │   ├── fair.py
│       │   ├── cicd.py
│       │   ├── testing.py
│       │   ├── documentation.py
│       │   ├── security.py
│       │   └── ...
│       ├── reporters/          # Générateurs de rapport
│       │   ├── markdown.py
│       │   ├── json.py
│       │   └── adaptive.py
│       ├── knowledge/          # Base de connaissances RSQKit
│       │   ├── rsqkit.yaml     # Tâches, checks, liens
│       │   └── sync.py         # Sync depuis GitHub RSQKit
│       └── languages/          # Détection multi-langage
│           ├── detector.py
│           └── ...
├── .opencode/
│   └── skills/
│       └── everse-scan/
│           └── SKILL.md        # Skill qui utilise le CLI + enrichit avec IA
└── tests/
```

---

## Références RSQKit

- **Page d'accueil** : https://everse.software/RSQKit/
- **Tâches** : https://everse.software/RSQKit/tasks
- **AI Guidance** : https://everse.software/RSQKit/ai
- **Tous les outils** : https://everse.software/RSQKit/all_tools_and_resources
- **Indicateurs** : https://everse.software/RSQKit/all_indicators
- **Source GitHub** : https://github.com/EVERSE-ResearchSoftware/RSQKit
- **Pages RSQKit** : https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages
