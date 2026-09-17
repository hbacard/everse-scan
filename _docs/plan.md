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

#### 2.1 Tâches RSQKit non couvertes en V1 — divulgation obligatoire

Le rapport V1 **doit inclure une section de divulgation** listant les tâches RSQKit non évaluées, avec liens. Un "pass" ne doit pas donner de fausse confiance.

> ⚠️ Ce scan évalue 10 des 35+ tâches RSQKit. Les tâches suivantes ne sont **pas** évaluées :
> - [Static analysis](https://everse.software/RSQKit/static_analysis)
> - [Software security](https://everse.software/RSQKit/research_software_security)
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments)
> - [Code review](https://everse.software/RSQKit/code_review)
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers)
> - [Releasing software](https://everse.software/RSQKit/releasing_software)
> - [Writing readable code](https://everse.software/RSQKit/writing_readable_code)
> - [Archiving software](https://everse.software/RSQKit/archiving_software)
> - [Future proofing](https://everse.software/RSQKit/future_proofing)
> - [Performance profiling](https://everse.software/RSQKit/performance_profiling_and_optimization)
> - [Environmental sustainability](https://everse.software/RSQKit/improving_environmental_sustainability)
> - [Computational workflows](https://everse.software/RSQKit/computational_workflows)
> - ... (voir [liste complète](https://everse.software/RSQKit/tasks))

#### 2.2 Checks à fort impact manquants (candidats V1.1/V2)

Plusieurs tâches RSQKit sont détectables mécaniquement avec un impact élevé. À ajouter dès que possible :

| # | Check | RSQKit page | Ce qu'on cherche | Pourquoi c'est important |
|---|---|---|---|---|
| 11 | **Static analysis** | `/static_analysis` | Configs de linters/formatters (ruff, eslint, mypy, prettier, rustfmt) | Qualité code, détection bugs, faible effort |
| 12 | **Security** | `/research_software_security` | Secrets hardcodés, dependabot, pip-audit/safety, CODEOWNERS | Risque direct, pas juste qualité |
| 13 | **Reproducible envs** | `/reproducible_software_environments` | Lockfiles (requirements.txt pinned, poetry.lock, conda-lock), Dockerfile, Nix | Exigence fondeurs, reproductibilité |
| 14 | **Code review** | `/code_review` | PR templates (.github/pull_request_template.md), CODEOWNERS, branch protection | Collaboration, qualité partagée |
| 15 | **Software identifiers** | `/software_identifiers` | DOI, .zenodo.json, badges Zenodo dans README | Citabilité, findabilité |
| 16 | **Releasing** | `/releasing_software` | Git tags, GitHub releases, CHANGELOG.md, semantic versioning | Traçabilité, reproductibilité |
| 17 | **Readable code** | `/writing_readable_code` | Configs de formatting (black, isort, prettier), conventions | Maintenabilité |

### 3. Détection multi-langage

Le skill détecte le langage principal du repo en analysant :

- Les fichiers de configuration (`pyproject.toml` → Python, `package.json` → JS/TS, `Cargo.toml` → Rust, `DESCRIPTION` → R, `Project.toml` → Julia, `CMakeLists.txt` → C/C++, etc.)
- L'extension des fichiers sources
- La présence de `.python-version`, `.ruby-version`, `.tool-versions`, etc.

Les checks s'adaptent au langage détecté (ex: pour Python → pytest, pour R → testthat, pour C++ → CTest, etc.).

### 3.1 Détection du tier de logiciel (three-tier model RSQKit)

RSQKit définit un [modèle à trois tiers](https://everse.software/RSQKit/three_tier_view) : **scripts** → **outils/prototypes** → **infrastructure**. Un script d'analyse jetable et un framework HPC publié n'ont pas besoin des mêmes pratiques. Le skill détecte le tier via des heuristiques et **adapte les checks pertinents** :

| Tier | Heuristiques de détection | Checks pertinents | Checks supprimés/atténués |
|---|---|---|---|
| **Script** (tier 1) | < 10 fichiers sources, pas de packaging, pas de tests, 1 auteur git, pas de releases | Version control, LICENSE, README, .gitignore | codemeta.json, CI testing matrices, containers, future-proofing |
| **Outil/Bibliothèque** (tier 2) | Packaging présent (pyproject.toml, package.json), > 1 auteur, tests présents ou recommandés, README structuré | Tous les 10 checks V1 + citation, metadata, releasing | Infrastructure-level only |
| **Infrastructure** (tier 3) | Multi-package, CI complexe, Docker, docs étendues, nombreux contributeurs, releases taguées | Tous les checks + security, reproducible envs, performance, future-proofing, environmental sustainability | Aucun — évaluation complète |

Le rapport affiche le tier détecté et justifie les checks ignorés :
> "Ce repo est détecté comme **script (tier 1)**. Les checks CI testing matrices, codemeta.json et containers ne sont pas pertinents à ce niveau. Voir le [modèle three-tier RSQKit](https://everse.software/RSQKit/three_tier_view)."

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

#### 5.1 Contenu de guidance AI (pas juste le numéro)

Le numéro (0-10) n'est qu'un point d'entrée. La **vraie valeur** est le contenu de guidance RSQKit associé à chaque niveau. Le rapport doit inclure :

**Cross-cutting practices** (appliquables à tous les niveaux) :
- Toujours relire le code généré par AI avant commit
- Garder le code AI dans des commits séparés pour l'auditabilité
- Documenter quels outils AI sont utilisés et comment
- Maintenir la capacité de rollback (version control + tests)
- Source : https://everse.software/RSQKit/cross_cutting_practices

**Guidance par niveau détecté** (exemples) :

| Niveau détecté | Guidance à afficher dans le rapport |
|---|---|
| 0 (No Gen-AI) | "Aucun usage d'AI détecté. C'est parfaitement valide. Si vous envisagez l'AI, commencez par le niveau 1 (conversationnel) pour des tâches ponctuelles. Voir [Conversational Interaction](https://everse.software/RSQKit/conversational_interaction)." |
| 1-3 (Conversational) | "Usage conversationnel détecté. Bon point de départ. **Risques** : pas de traçabilité du code généré, pas de contexte repo. **Qualité** : documentez vos prompts, committez séparément. Voir [Cross Cutting Practices](https://everse.software/RSQKit/cross_cutting_practices)." |
| 4-6 (IDE/Repo-aware) | "Assistant IDE/repo détecté (`.cursorrules`, `AGENTS.md`, `.opencode/`). **Risques** : confiance excessive dans le contexte repo, hallucinations sur API. **Qualité** : ajoutez des garde-fous dans les règles (ex: ne pas modifier les fichiers de config sans accord), maintenez des tests comme filet. Voir [Repository-aware assistance](https://everse.software/RSQKit/repository_aware_assistance)." |
| 7-9 (Agents) | "Agents CI/PR détectés. **Risques** : blast radius élevé, modifications automatisées sans revue. **Qualité** : exigez une revue humaine obligatoire sur tout PR généré par agent, limitez les permissions du bot, ajoutez des tests de non-régression. Voir [CI/PR/repository agents](https://everse.software/RSQKit/ci_pr_repository_agents)." |
| 10 (Autonomous) | "Agents autonomes détectés. **Risque maximal** : conséquences difficiles à prévoir, volume de modifications élevé. **Qualité** : garde-fous stricts obligatoires — tests exhaustifs, rollback automatique, monitoring, limites de scope. Voir [Open-ended autonomous agents](https://everse.software/RSQKit/open_ended_autonomous_agents)." |

**AI intensity considerations** : le rapport doit aussi indiquer *pourquoi* on pourrait vouloir monter ou descendre, pas juste le niveau actuel :
- Monter : tâches répétitives, documentation, tests → gain de temps
- Descendre : code critique pour résultats de recherche, sécurité, dépendances → risque trop élevé
- Source : https://everse.software/RSQKit/ai_intensity_considerations

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

### Dimensions de qualité (mapping RSQKit)
> Source : https://everse.software/RSQKit/all_indicators

| Dimension | Score | Checks impliqués |
|---|---|---|
| Reproductibilité | ⚠️ | Packaging, Tests, CI/CD, Reproducible envs |
| Maintenabilité | ✅ | Structure, Documentation, Readable code |
| Findability | ❌ | CITATION.cff, codemeta.json, Software identifiers |
| Trustworthiness | ⚠️ | Tests, CI/CD, Code review, Security |
| Réutilisabilité | ⚠️ | LICENSE, README, Documentation, Metadata |

### Tâches non évaluées
> ⚠️ Ce scan évalue 10 des 35+ tâches RSQKit. Les tâches suivantes ne sont **pas** évaluées :
> - [Static analysis](https://everse.software/RSQKit/static_analysis)
> - [Software security](https://everse.software/RSQKit/research_software_security)
> - [Reproducible environments](https://everse.software/RSQKit/reproducible_software_environments)
> - [Code review](https://everse.software/RSQKit/code_review)
> - [Software identifiers](https://everse.software/RSQKit/software_identifiers)
> - ... (voir [liste complète](https://everse.software/RSQKit/tasks))

### Tier de logiciel détecté
**Tier**: [Script / Outil-Bibliothèque / Infrastructure]
**Justification**: [heuristiques qui ont mené à cette classification]

---

## 2. Plan d'action priorisé

> Priorisation 2D : effort × impact. L'impact facture le risque, le tier, et le rôle.

### Quick wins (faible effort, impact élevé)
1. Ajouter un fichier LICENSE (cf. https://everse.software/RSQKit/licensing_software) — **impact: critique** (sans licence = non réutilisable)
2. Créer un CITATION.cff minimal (cf. https://everse.software/RSQKit/citing_software) — **impact: élevé** (crédit académique)
...

### Risques critiques (à traiter en priorité si détectés)
1. 🔴 Secret hardcodé dans le repo — **impact: critique** (sécurité)
2. 🔴 Pas de version control — **impact: critique** (tout le reste en dépend)
...

### Moyen terme (effort modéré, impact modéré)
1. Mettre en place une CI/CD basique (cf. https://everse.software/RSQKit/ci_cd)
2. Ajouter des tests unitaires — RSQKit recommande **pytest** pour Python (cf. https://everse.software/RSQKit/testing_software)
...

### Long terme (effort élevé, impact structurel)
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

**Outils RSQKit recommandés** (pour [langage détecté]):
- [outil 1] — [pourquoi]
- [outil 2] — [pourquoi]
- Voir : https://everse.software/RSQKit/[page]#tools

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

### 7. Remédiation interactive — génération contextuelle

La remédiation ne génère **pas des templates vierges**. Chaque fichier généré est **pré-rempli depuis le contenu réel du repo** :

#### 7.1 Génération contextuelle (pré-fill from repo data)

| Fichier à générer | Source de données pour pré-fill |
|---|---|
| `CITATION.cff` | Auteurs via `git log --format='%aN <%aE>'`, titre depuis README H1, licence depuis LICENSE → SPDX, URL repo depuis `git remote -v`, version depuis dernier tag |
| `codemeta.json` | Idem CITATION.cff + dépendances depuis pyproject.toml/package.json, langage depuis détecteur, keywords depuis README |
| `README.md` | Nom projet depuis repo dir, description depuis README existant (si partiel), section installation depuis deps détectés, section licence depuis LICENSE |
| `.github/workflows/test.yml` | Runner selon langage (pytest pour Python, `npm test` pour JS, CTest pour C++), version Python depuis `.python-version` ou `pyproject.toml` |
| `.gitignore` | Template selon langage détecté (Python → `__pycache__/`, `.venv/`, `*.pyc`, etc.) |

#### 7.2 Flux de génération (trust + transparence)

1. **Prévisualiser** le contenu qui sera généré (avant d'écrire)
2. Demander **confirmation explicite** de l'utilisateur
3. **Écrire** le fichier
4. **Afficher** ce qui a été créé/modifié
5. Proposer le **prochain step** de la chaîne de remédiation

#### 7.3 Chaînes de remédiation (pas juste one-shot)

La génération d'un fichier n'est souvent que la première étape. Le skill propose des **chaînes** :

**Chaîne citation** :
```
1. Générer CITATION.cff (pré-rempli depuis git + README + LICENSE)
   → 2. Connecter le repo à Zenodo (GitHub integration)
   → 3. Créer une release (tag) pour déclencher le DOI Zenodo
   → 4. Ajouter le badge DOI dans le README
   → 5. Ajouter le DOI dans codemeta.json "identifier"
```

**Chaîne CI** :
```
1. Générer .github/workflows/test.yml (adapté au langage détecté)
   → 2. Ajouter un job de linting (ruff pour Python, eslint pour JS)
   → 3. Ajouter Dependabot (.github/dependabot.yml)
   → 4. Ajouter un PR template (.github/pull_request_template.md)
   → 5. Activer branch protection (instructions, pas automatisé)
```

**Chaîne metadata** :
```
1. Générer codemeta.json (pré-rempli depuis deps + langage + auteurs)
   → 2. Valider avec le validateur codemeta (lien)
   → 3. Ajouter .zenodo.json pour contrôler le dépôt Zenodo
   → 4. Vérifier la cohérence CITATION.cff ↔ codemeta.json
```

#### 7.4 Menu interactif

À la fin du rapport, le skill propose :

```
Je peux t'aider à corriger les problèmes identifiés :

📋 Fichiers à générer (pré-remplis depuis ton repo) :
  1. LICENSE (MIT détecté depuis pyproject.toml)
  2. CITATION.cff (auteurs: 3 trouvés via git log)
  3. codemeta.json (deps: 5 depuis pyproject.toml)
  4. .github/workflows/test.yml (pytest pour Python 3.12)
  5. .gitignore (template Python)

🔗 Chaînes de remédiation disponibles :
  A. Chaîne citation → CITATION.cff → Zenodo → DOI → README badge
  B. Chaîne CI → workflow → linting → dependabot → PR template
  C. Chaîne metadata → codemeta.json → .zenodo.json → validation

Dis-moi ce que tu veux faire (numéro, lettre, ou "tout").
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
5. **AI spectrum** (critères d'évaluation 0-10 + guidance par niveau)
6. **Instructions de remédiation interactive** (génération contextuelle + chaînes)

---

## V1.1 — Améliorations rapides (skill opencode, pas de CLI)

Ces améliorations restent dans le cadre du skill opencode (pas de dépendance externe) mais augmentent significativement la valeur :

### 1. Recommandations d'outils RSQKit par check

Chaque check du rapport inclut les **outils recommandés par RSQKit pour le langage détecté**, pas juste "ajoute des tests" :

| Check | Python | R | JS/TS | C++ | Julia |
|---|---|---|---|---|---|
| Tests | pytest, hypothesis | testthat | jest, vitest | CTest, Google Test | Test.jl |
| Linting | ruff, mypy | lintr | eslint, prettier | clang-tidy | JuliaFormatter.jl |
| CI | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions |
| Packaging | pyproject.toml, hatch | devtools | npm publish | CMake, Conan | Pkg.jl |
| Docs | Sphinx, MkDocs | pkgdown | JSDoc, Docusaurus | Doxygen | Documenter.jl |

Source : https://everse.software/RSQKit/all_tools_and_resources

### 2. Détection du tier (three-tier model)

Déjà spécifié en section 3.1. Implémentation dans le skill via heuristiques :
- Compter les fichiers sources (Glob)
- Vérifier présence de packaging (Glob pour pyproject.toml, package.json, etc.)
- Compter les auteurs via `git log --format='%aN' | sort -u | wc -l`
- Vérifier présence de releases/tags via `git tag`

### 3. Guidance AI spectrum (pas juste le numéro)

Déjà spécifié en section 5.1. Le SKILL.md embarque le contenu de guidance pour chaque niveau.

### 4. Chaînes de remédiation

Déjà spécifié en section 7.3. Implémentation : le skill propose les chaînes et guide étape par étape.

### 5. RSQKit tool tables embarquées

Le SKILL.md embarque une table de référence des outils RSQKit par langage (extrait condensé de https://everse.software/RSQKit/all_tools_and_resources). Permet au rapport de recommander l'outil exact plutôt qu'un conseil générique.

### 6. Détection du stage de lifecycle

Détection heuristique du [lifecycle stage](https://everse.software/RSQKit/life_cycle) du repo :

| Stage | Heuristiques | Recommandations priorisées |
|---|---|---|
| **Early** | < 10 commits, pas de tags, 1 auteur | Structure, LICENSE, .gitignore, README |
| **Active dev** | Commits réguliers, pas de CI | Tests, CI, documentation |
| **Maintenance** | Releases présentes, peu de commits récents | Future-proofing, dependency update, archiving |
| **Published** | DOI présent, activité minimale | Vérifier citation à jour, metadata complète |

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
everse-scan scan ./mon-repo --tier auto  # détection automatique du tier
everse-scan scan ./mon-repo --funder horizon-europe  # alignement funder
everse-scan diff ./mon-repo --baseline last-report.json  # re-scan + delta
```

### V2 — Nouvelles fonctionnalités

#### 1. Priorisation 2D (effort × impact)

Le rapport V2 utilise une matrice 2D au lieu d'une simple liste par effort :

```
         Impact →
          Faible    Modéré    Élevé    Critique
Effort   ┌─────────┬──────────┬─────────┬──────────┐
Faible   │  skip   │  later   │ DO NOW  │ URGENT   │
         ├─────────┼──────────┼─────────┼──────────┤
Modéré   │  skip   │  later   │ quick   │ priority │
         ├─────────┼──────────┼─────────┼──────────┤
Élevé    │  skip   │  plan    │  plan   │ critical │
         └─────────┴──────────┴─────────┴──────────┘
```

Facteurs d'impact :
- **Risque sécurité** (secret hardcodé = critique)
- **Tier de logiciel** (script: pas de codemeta; infrastructure: security obligatoire)
- **Stage de lifecycle** (pre-publication: citation urgent; maintenance: future-proofing)
- **Rôle cible** (researcher: crédit d'abord; RSE: engineering d'abord)
- **Exigences funder** (Horizon Europe: open access + FAIR obligatoire)

#### 2. Détection du stage de lifecycle

Basé sur le [lifecycle model RSQKit](https://everse.software/RSQKit/life_cycle) :
- Analyse git log (fréquence commits, dernière activité)
- Détection de releases/tags
- Détection de DOI/publication
- Adaptation des recommandations au stage

#### 3. Rapport adaptatif par rôle

| | Researcher who codes | RSE |
|---|---|---|
| **Ton** | Langage simple, explications | Technique, concis |
| **Priorité** | Crédit/citation en premier (LICENSE, CITATION.cff, DOI) | Engineering d'abord (tests, CI, code review) |
| **Profondeur** | Résumé exécutif + quick wins | Détails techniques complets |
| **Exemples** | Research software stories similaires | Tool comparisons, CI matrix patterns |

#### 4. Re-scan et tracking de progression

```bash
# Premier scan
everse-scan scan ./mon-repo --save baseline.json

# Après corrections
everse-scan scan ./mon-repo --diff baseline.json
# → "7/10 checks pass (was 4/10). Improvements: LICENSE ✅, CITATION.cff ✅, CI ✅"
```

Le rapport de diff inclut :
- Score avant/après
- Checks nouvellement passés
- Checks régressés (si applicable)
- Prochaines étapes recommandées mises à jour

#### 5. Intégration avec outils FAIR existants

Plutôt que de dupliquer les checks, le CLI peut intégrer et orchestrer des outils existants :

| Outil | Ce qu'il vérifie | Intégration |
|---|---|---|
| [howfairis](https://github.com/fair-software/howfairis) | FAIR principles (5 aspects) | `everse-scan scan --use howfairis` |
| [FAIR software checklist](https://fair-software.eu/) | Checklist FAIR | Intégration résultats dans le rapport |
| [cffconvert](https://github.com/citation-file-format/cffconvert) | Validation CITATION.cff | Check automatique |
| [codemeta validator](https://codemeta.github.io/codemetar/) | Validation codemeta.json | Check automatique |
| [GitHub security advisories](https://docs.github.com/en/code-security) | Dépendances vulnérables | Check automatique |

Avantages :
- Réduit les faux positifs (outils éprouvés)
- Crédibilité (pas juste "l'IA le dit")
- Moins d'effort de développement

#### 6. Couverture complète des 35+ tâches RSQKit

Le CLI V2 embarque une base de connaissances locale (`rsqkit.yaml`) synchronisée depuis le [GitHub RSQKit](https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages). Chaque tâche RSQKit a un check correspondant (déterministe ou heuristique).

#### 7. Alignement funder

Détection du funder (Horizon Europe, NSF, Wellcome, etc.) depuis :
- README (mentions de grants)
- `.zenodo.json` (grants field)
- `CITATION.cff` (grants field)

Le rapport croise les exigences funder avec l'état du repo :
> "Ce projet est financé par Horizon Europe. Exigences : open access code, FAIR, DOI persistant. **Manquant** : pas de DOI, pas de licence open source explicite."

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
│       │   ├── reproducibility.py
│       │   └── ...
│       ├── reporters/          # Générateurs de rapport
│       │   ├── markdown.py
│       │   ├── json.py
│       │   ├── adaptive.py     # Adaptatif par rôle (researcher/RSE)
│       │   └── diff.py         # Rapport de progression (re-scan)
│       ├── knowledge/           # Base de connaissances RSQKit
│       │   ├── rsqkit.yaml     # Tâches, checks, liens, tools par langage
│       │   ├── sync.py         # Sync depuis GitHub RSQKit
│       │   └── funders.yaml    # Exigences par funder (Horizon Europe, NSF, etc.)
│       ├── languages/          # Détection multi-langage
│       │   ├── detector.py
│       │   └── ...
│       ├── context/            # Analyse contextuelle du repo
│       │   ├── tier.py         # Détection three-tier (script/tool/infrastructure)
│       │   ├── lifecycle.py    # Détection du stage (early/active/maintenance/published)
│       │   └── funder.py       # Détection du funder
│       └── integrations/       # Outils FAIR externes
│           ├── howfairis.py
│           ├── cffconvert.py
│           └── codemeta.py
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
- **Spectrum of AI Intensity** : https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
- **Cross Cutting Practices** : https://everse.software/RSQKit/cross_cutting_practices
- **AI Intensity Considerations** : https://everse.software/RSQKit/ai_intensity_considerations
- **Three-tier model** : https://everse.software/RSQKit/three_tier_view
- **Lifecycle** : https://everse.software/RSQKit/life_cycle
- **Quality dimensions** : https://everse.software/RSQKit/quality_dimensions
- **Tous les outils** : https://everse.software/RSQKit/all_tools_and_resources
- **Indicateurs** : https://everse.software/RSQKit/all_indicators
- **Research software stories** : https://everse.software/RSQKit/research_software_stories
- **Source GitHub** : https://github.com/EVERSE-ResearchSoftware/RSQKit
- **Pages RSQKit** : https://github.com/EVERSE-ResearchSoftware/RSQKit/tree/main/pages

## Outils FAIR externes (intégration V2)

- **howfairis** : https://github.com/fair-software/howfairis
- **cffconvert** : https://github.com/citation-file-format/cffconvert
- **codemeta validator** : https://codemeta.github.io/codemetar/
- **FAIR software checklist** : https://fair-software.eu/

---

## Milestones

### M1 — Skill opencode V1 (MVP)

**Objectif** : Skill opencode fonctionnel, 10 checks, rapport Markdown structuré.

| Item | Détail |
|---|---|
| **Livrable** | `.opencode/skills/everse-scan/SKILL.md` |
| **Checks** | 10 checks V1 (README, LICENSE, CITATION.cff, codemeta.json, tests, CI/CD, structure, docs, dép packaging, version control) |
| **Détection** | Multi-langage (Python, R, C++, Julia, JS/TS) |
| **Rapport** | Markdown : résumé exécutif + plan d'action + détails techniques + AI spectrum |
| **Remédiation** | Menu interactif simple (liste de fichiers à générer) |
| **Repos** | Local + distant (URLs GitHub) |
| **Critère de fin** | Scan d'un repo Python réel → rapport complet généré en une session |

### M2 — V1.1 : Améliorations du skill (valeur ajoutée)

**Objectif** : Enrichir le skill V1 sans passer au CLI. Rendre le rapport réellement actionnable.

| Item | Détail |
|---|---|
| **Détection du tier** | Heuristiques script / outil-bibliothèque / infrastructure |
| **Outils RSQKit par check** | Table embarquée (pytest, ruff, Sphinx, etc. par langage) |
| **Guidance AI spectrum** | Contenu par niveau (pas juste le numéro), cross-cutting practices |
| **Remédiation contextuelle** | Pré-fill CITATION.cff / codemeta.json depuis git log + README + LICENSE |
| **Chaînes de remédiation** | Chaîne citation, chaîne CI, chaîne metadata |
| **Détection lifecycle** | Early / active dev / maintenance / published |
| **Dimensions de qualité** | Scorecard reproducibility / maintainability / findability / trustworthiness |
| **Tâches non couvertes** | Divulgation explicite des 25+ tâches RSQKit non évaluées |
| **Critère de fin** | Scan d'un repo Python + R → rapport avec tier détecté, outils recommandés, chaînes proposées, pré-fill CITATION.cff |

### M3 — CLI Python V2 : Core

**Objectif** : CLI Python fonctionnel, checks déterministes, sortie JSON + Markdown.

| Item | Détail |
|---|---|
| **Livrable** | `pip install everse-scan` |
| **Checks** | 10 checks V1 portés en Python déterministe + 7 checks V1.1 (static analysis, security, reproducible envs, code review, software identifiers, releasing, readable code) |
| **Détection** | Multi-langage + tier + lifecycle |
| **Sortie** | `--format json,markdown` |
| **Architecture** | `src/everse_scan/` avec `cli.py`, `scanner.py`, `checks/`, `reporters/`, `languages/` |
| **Base de connaissances** | `rsqkit.yaml` (tâches, checks, liens) — manuelle pour M3 |
| **Critère de fin** | `everse-scan scan ./repo --format json` → JSON valide + Markdown lisible, 17 checks |

### M4 — CLI V2 : Rapport adaptatif + Re-scan

**Objectif** : Rapport adaptatif par rôle, tracking de progression, priorisation 2D.

| Item | Détail |
|---|---|
| **Rôle** | `--role rse` / `--role researcher` → ton, priorités, profondeur adaptés |
| **Re-scan** | `--save baseline.json` + `--diff baseline.json` → delta avant/après |
| **Priorisation 2D** | Matrice effort × impact (avec facteurs risque, tier, lifecycle, rôle) |
| **Reporter adaptatif** | `reporters/adaptive.py` + `reporters/diff.py` |
| **Critère de fin** | Scan baseline → corrections → re-scan → rapport de progression affiche "7/17 (was 4/17)" |

### M5 — CLI V2 : Intégrations FAIR + Couverture complète

**Objectif** : Intégrer les outils FAIR existants, couvrir les 35+ tâches RSQKit.

| Item | Détail |
|---|---|
| **Intégrations** | howfairis, cffconvert, codemeta validator, GitHub security advisories |
| **Couverture RSQKit** | 35+ tâches → chaque tâche a un check (déterministe ou heuristique) |
| **Sync RSQKit** | `knowledge/sync.py` — sync automatique depuis GitHub RSQKit |
| **Critère de fin** | `everse-scan scan ./repo --use howfairis` → rapport croisé CLI + howfairis, 35+ checks |

### M6 — CLI V2 : Funder compliance + Contexte avancé

**Objectif** : Alignement funder, détection de grants, recommandations selon le funder.

| Item | Détail |
|---|---|
| **Détection funder** | Horizon Europe, NSF, Wellcome (depuis README, .zenodo.json, CITATION.cff) |
| **Exigences funder** | `knowledge/funders.yaml` — exigences par funder |
| **Rapport funder** | Section "Conformité funder" : exigences vs état du repo |
| **Tier avancé** | Détection fine + suppression de checks non pertinents |
| **Critère de fin** | Scan d'un repo Horizon Europe → rapport affiche "Manquant : DOI persistant, licence open source" selon exigences HE |
