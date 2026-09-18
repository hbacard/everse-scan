"""RSQKit knowledge base — task definitions, URLs, tools per language.

This module provides programmatic access to the RSQKit task catalogue.
The data is stored as a Python dict for M5; a YAML file + sync script
will be added for automated updates from GitHub RSQKit in a future iteration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


RSQKIT_BASE = "https://everse.software/RSQKit"


@dataclass(frozen=True)
class RSQKitTask:
    id: str
    name: str
    url: str
    category: str           # fair, engineering, documentation, security, sustainability
    covered_by: str         # check function name, "" if not covered
    effort: str             # low, medium, high
    impact: str             # low, medium, high, critical
    description: str = ""


# Full RSQKit task catalogue (35+ tasks)
TASKS: list[RSQKitTask] = [
    # --- FAIR & metadata ---
    RSQKitTask("readme", "Creating good README", f"{RSQKIT_BASE}/creating_good_readme", "documentation", "check_readme", "low", "high"),
    RSQKitTask("license", "Licensing software", f"{RSQKIT_BASE}/licensing_software", "fair", "check_license", "low", "high"),
    RSQKitTask("citation", "Citing software (CITATION.cff)", f"{RSQKIT_BASE}/citing_software", "fair", "check_citation", "low", "high"),
    RSQKitTask("codemeta", "Complete software metadata (codemeta.json)", f"{RSQKIT_BASE}/complete_software_metadata_codemeta", "fair", "check_codemeta", "medium", "high"),
    RSQKitTask("software_identifiers", "Software identifiers (DOI, Zenodo)", f"{RSQKIT_BASE}/software_identifiers", "fair", "check_software_identifiers", "low", "medium"),
    RSQKitTask("authorship", "Authorship and contributions", f"{RSQKIT_BASE}/authorship_and_contributions", "fair", "check_authorship", "low", "medium"),
    RSQKitTask("orcid", "ORCID integration", f"{RSQKIT_BASE}/orcid_integration", "fair", "check_orcid", "low", "low"),

    # --- Engineering ---
    RSQKitTask("structure", "Software project structure", f"{RSQKIT_BASE}/software_project_structure", "engineering", "check_structure", "medium", "medium"),
    RSQKitTask("version_control", "Using version control", f"{RSQKIT_BASE}/using_version_control", "engineering", "check_version_control", "low", "high"),
    RSQKitTask("testing", "Testing software", f"{RSQKIT_BASE}/testing_software", "engineering", "check_tests", "high", "high"),
    RSQKitTask("cicd", "CI/CD", f"{RSQKIT_BASE}/ci_cd", "engineering", "check_cicd", "medium", "high"),
    RSQKitTask("packaging", "Packaging software", f"{RSQKIT_BASE}/packaging_software", "engineering", "check_packaging", "medium", "medium"),
    RSQKitTask("static_analysis", "Static analysis", f"{RSQKIT_BASE}/static_analysis", "engineering", "check_static_analysis", "low", "medium"),
    RSQKitTask("code_review", "Code review", f"{RSQKIT_BASE}/code_review", "engineering", "check_code_review", "medium", "medium"),
    RSQKitTask("releasing", "Releasing software", f"{RSQKIT_BASE}/releasing_software", "engineering", "check_releasing", "medium", "medium"),
    RSQKitTask("readable_code", "Writing readable code", f"{RSQKIT_BASE}/writing_readable_code", "engineering", "check_readable_code", "low", "low"),
    RSQKitTask("dependency_management", "Dependency management", f"{RSQKIT_BASE}/dependency_management", "engineering", "check_dependency_management", "low", "high"),
    RSQKitTask("containers", "Containerization", f"{RSQKIT_BASE}/containerization", "engineering", "check_containers", "medium", "medium"),
    RSQKitTask("workflow_files", "Computational workflows", f"{RSQKIT_BASE}/computational_workflows", "engineering", "check_workflow_files", "medium", "low"),
    RSQKitTask("api_docs", "API documentation", f"{RSQKIT_BASE}/api_documentation", "engineering", "check_api_docs", "medium", "medium"),

    # --- Documentation ---
    RSQKitTask("documentation", "Software documentation", f"{RSQKIT_BASE}/software_documentation", "documentation", "check_documentation", "medium", "medium"),
    RSQKitTask("changelog", "Changelog", f"{RSQKIT_BASE}/changelog", "documentation", "check_changelog", "low", "low"),
    RSQKitTask("contribution_guide", "Contribution guidelines", f"{RSQKIT_BASE}/contribution_guidelines", "documentation", "check_contribution_guide", "low", "medium"),
    RSQKitTask("code_of_conduct", "Code of conduct", f"{RSQKIT_BASE}/code_of_conduct", "documentation", "check_code_of_conduct", "low", "low"),
    RSQKitTask("issue_templates", "Issue templates", f"{RSQKIT_BASE}/issue_templates", "documentation", "check_issue_templates", "low", "low"),

    # --- Security ---
    RSQKitTask("security", "Research software security", f"{RSQKIT_BASE}/research_software_security", "security", "check_security", "medium", "critical"),
    RSQKitTask("secret_management", "Secret management", f"{RSQKIT_BASE}/secret_management", "security", "check_secret_management", "low", "critical"),

    # --- Reproducibility ---
    RSQKitTask("reproducible_envs", "Reproducible software environments", f"{RSQKIT_BASE}/reproducible_software_environments", "engineering", "check_reproducible_envs", "medium", "high"),
    RSQKitTask("data_management", "Data management plan", f"{RSQKIT_BASE}/data_management", "reproducibility", "check_data_management", "low", "medium"),
    RSQKitTask("reproducibility_checklist", "Reproducibility checklist", f"{RSQKIT_BASE}/reproducibility_checklist", "reproducibility", "check_reproducibility_checklist", "low", "medium"),

    # --- Sustainability ---
    RSQKitTask("archiving", "Archiving software", f"{RSQKIT_BASE}/archiving_software", "sustainability", "check_archiving", "medium", "medium"),
    RSQKitTask("future_proofing", "Future proofing", f"{RSQKIT_BASE}/future_proofing", "sustainability", "check_future_proofing", "medium", "medium"),
    RSQKitTask("sustainability_plan", "Software sustainability plan", f"{RSQKIT_BASE}/software_sustainability_plan", "sustainability", "check_sustainability_plan", "low", "low"),
    RSQKitTask("env_sustainability", "Environmental sustainability", f"{RSQKIT_BASE}/improving_environmental_sustainability", "sustainability", "check_env_sustainability", "medium", "low"),

    # --- Quality & review ---
    RSQKitTask("software_peereview", "Software peer review", f"{RSQKIT_BASE}/software_peer_review", "quality", "check_software_peer_review", "high", "medium"),
    RSQKitTask("quality_model", "Software quality models", f"{RSQKIT_BASE}/software_quality_models", "quality", "check_quality_model", "medium", "low"),
]


def get_task(task_id: str) -> Optional[RSQKitTask]:
    for t in TASKS:
        if t.id == task_id:
            return t
    return None


def get_covered_tasks() -> list[RSQKitTask]:
    return [t for t in TASKS if t.covered_by]


def get_uncovered_tasks() -> list[RSQKitTask]:
    return [t for t in TASKS if not t.covered_by]


def tasks_by_category(category: str) -> list[RSQKitTask]:
    return [t for t in TASKS if t.category == category]


TOOLS_BY_LANGUAGE: dict[str, dict[str, list[str]]] = {
    "Python": {
        "testing": ["pytest", "unittest", "tox", "nox"],
        "linting": ["ruff", "pylint", "flake8", "mypy"],
        "formatting": ["black", "ruff format", "isort"],
        "docs": ["Sphinx", "MkDocs", "pdoc"],
        "packaging": ["hatch", "setuptools", "poetry", "pdm", "flit"],
        "envs": ["venv", "pip-tools", "uv", "conda", "poetry"],
        "security": ["bandit", "pip-audit", "safety"],
        "ci": ["GitHub Actions", "GitLab CI", "tox"],
    },
    "R": {
        "testing": ["testthat", "tinytest"],
        "linting": ["lintr"],
        "formatting": ["styler"],
        "docs": ["pkgdown", "roxygen2"],
        "packaging": ["devtools", "usethis"],
        "envs": ["renv", "conda"],
        "security": ["gitleaks"],
        "ci": ["GitHub Actions", "GitLab CI"],
    },
    "JavaScript": {
        "testing": ["jest", "mocha", "vitest"],
        "linting": ["eslint", "biome"],
        "formatting": ["prettier"],
        "docs": ["JSDoc", "TypeDoc"],
        "packaging": ["npm", "yarn", "pnpm"],
        "envs": ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
        "security": ["npm audit", "snyk"],
        "ci": ["GitHub Actions", "GitLab CI"],
    },
    "TypeScript": {
        "testing": ["jest", "mocha", "vitest"],
        "linting": ["eslint", "biome"],
        "formatting": ["prettier"],
        "docs": ["TypeDoc"],
        "packaging": ["npm", "yarn", "pnpm"],
        "envs": ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
        "security": ["npm audit", "snyk"],
        "ci": ["GitHub Actions", "GitLab CI"],
    },
    "C++": {
        "testing": ["Google Test", "Catch2", "doctest"],
        "linting": ["clang-tidy", "cppcheck", "clang-format"],
        "formatting": ["clang-format"],
        "docs": ["Doxygen", "Sphinx+Breathe"],
        "packaging": ["CMake", "Meson", "vcpkg", "Conan"],
        "envs": ["Docker", "Spack"],
        "security": ["clang-tidy security checks"],
        "ci": ["GitHub Actions", "GitLab CI"],
    },
    "Julia": {
        "testing": ["Test.jl", "Aqua.jl"],
        "linting": ["JET.jl"],
        "formatting": ["JuliaFormatter.jl"],
        "docs": ["Documenter.jl"],
        "packaging": ["Pkg.jl"],
        "envs": ["Manifest.toml", "PkgTemplates.jl"],
        "security": [],
        "ci": ["GitHub Actions"],
    },
    "Rust": {
        "testing": ["cargo test"],
        "linting": ["clippy"],
        "formatting": ["rustfmt"],
        "docs": ["rustdoc"],
        "packaging": ["cargo"],
        "envs": ["Cargo.lock"],
        "security": ["cargo audit"],
        "ci": ["GitHub Actions", "GitLab CI"],
    },
    "Go": {
        "testing": ["go test", "testify"],
        "linting": ["golangci-lint", "golint", "revive"],
        "formatting": ["gofmt", "gofumpt"],
        "docs": ["godoc", "pkg.go.dev"],
        "packaging": ["go mod"],
        "envs": ["go.mod", "go.sum"],
        "security": ["govulncheck"],
        "ci": ["GitHub Actions", "GitLab CI"],
    },
    "Java": {
        "testing": ["JUnit", "TestNG"],
        "linting": ["Checkstyle", "SpotBugs", "PMD"],
        "formatting": ["google-java-format", "Spotless"],
        "docs": ["Javadoc", "Sphinx"],
        "packaging": ["Maven", "Gradle"],
        "envs": ["Maven", "Gradle"],
        "security": ["OWASP Dependency-Check", "SpotBugs"],
        "ci": ["GitHub Actions", "GitLab CI", "Jenkins"],
    },
    "Ruby": {
        "testing": ["RSpec", "Minitest"],
        "linting": ["RuboCop"],
        "formatting": ["RuboCop"],
        "docs": ["YARD", "RDoc"],
        "packaging": ["Bundler", "gem"],
        "envs": ["Gemfile.lock"],
        "security": ["bundler-audit", "brakeman"],
        "ci": ["GitHub Actions", "GitLab CI"],
    },
}


def get_tools(language: str, category: str) -> list[str]:
    return TOOLS_BY_LANGUAGE.get(language, {}).get(category, [])
