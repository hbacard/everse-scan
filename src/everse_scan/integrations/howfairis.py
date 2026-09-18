"""howfairis integration: check 5 FAIR principles for research software.

If the howfairis package is installed, use it. Otherwise, fall back to
deterministic checks based on repository content.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from everse_scan.models import CheckResult, CheckStatus


FAIR_PRINCIPLES = [
    ("repository", "Repository is publicly accessible (version control)"),
    ("license", "Repository has a license"),
    ("registry", "Repository is in a registry (PyPI, CRAN, npm, etc.)"),
    ("citation", "Repository enables citation (CITATION.cff or CITATION)"),
    ("checklist", "Repository uses a software quality checklist"),
]


def check_howfairis(repo_path: str) -> list[CheckResult]:
    """Check the 5 FAIR principles. Falls back to heuristic if howfairis not installed."""
    path = Path(repo_path)
    results: list[CheckResult] = []

    # Try to use howfairis if available
    try:
        return _check_with_howfairis(repo_path)
    except (ImportError, Exception):
        pass

    # Fallback: deterministic heuristic checks
    for principle_id, description in FAIR_PRINCIPLES:
        results.append(_check_principle(path, principle_id, description))

    return results


def _check_with_howfairis(repo_path: str) -> list[CheckResult]:
    """Use the howfairis package if installed."""
    from howfairis import Checker
    from howfairis.model import Repo

    results: list[CheckResult] = []
    # howfairis expects a GitHub URL; for local repos we do a best-effort
    checker = Checker(Repo(url=f"file://{repo_path}"))
    compliance = checker.check_five_recommendations()

    principle_names = ["repository", "license", "registry", "citation", "checklist"]
    for i, (name, desc) in enumerate(zip(principle_names, FAIR_PRINCIPLES)):
        passed = compliance[i] if i < len(compliance) else False
        status = CheckStatus.PASS if passed else CheckStatus.WARN
        results.append(CheckResult(
            name=f"FAIR: {name}",
            status=status,
            message=f"{'Pass' if passed else 'Not met'}: {desc[1]}",
            details=[f"howfairis principle: {name}"],
            rsqkit_url="https://fair-software.eu/",
            category="fair",
        ))

    return results


def _check_principle(path: Path, principle_id: str, description: str) -> CheckResult:
    """Heuristic check for a FAIR principle."""
    if principle_id == "repository":
        is_git = (path / ".git").exists()
        return CheckResult(
            name="FAIR: repository",
            status=CheckStatus.PASS if is_git else CheckStatus.FAIL,
            message=f"{'Git repository detected' if is_git else 'No git repository found'}: {description}",
            details=[f".git exists: {is_git}"],
            rsqkit_url="https://fair-software.eu/recommendations/repository",
            category="fair",
        )

    if principle_id == "license":
        has_license = any((path / f).exists() for f in ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"])
        in_pyproject = False
        pp = path / "pyproject.toml"
        if pp.exists():
            content = pp.read_text(errors="ignore").lower()
            in_pyproject = "license" in content
        has_any = has_license or in_pyproject
        return CheckResult(
            name="FAIR: license",
            status=CheckStatus.PASS if has_license else (CheckStatus.WARN if in_pyproject else CheckStatus.FAIL),
            message=f"{'License file found' if has_license else ('License in pyproject.toml' if in_pyproject else 'No license found')}: {description}",
            details=[f"LICENSE file: {has_license}", f"pyproject.toml license: {in_pyproject}"],
            rsqkit_url="https://fair-software.eu/recommendations/license",
            category="fair",
        )

    if principle_id == "registry":
        # Check if the package is registered (heuristic: packaging file present)
        registry_files = ["pyproject.toml", "setup.py", "package.json", "DESCRIPTION", "Gemfile", "Cargo.toml", "go.mod"]
        found = [f for f in registry_files if (path / f).exists()]
        return CheckResult(
            name="FAIR: registry",
            status=CheckStatus.PASS if found else CheckStatus.WARN,
            message=f"{'Packaging file found (registry-ready)' if found else 'No packaging file found'}: {description}",
            details=[f"Found: {', '.join(found)}" if found else "None"],
            rsqkit_url="https://fair-software.eu/recommendations/registry",
            category="fair",
        )

    if principle_id == "citation":
        has_citation = (path / "CITATION.cff").exists() or (path / "CITATION").exists()
        return CheckResult(
            name="FAIR: citation",
            status=CheckStatus.PASS if has_citation else CheckStatus.FAIL,
            message=f"{'CITATION.cff found' if has_citation else 'No citation file found'}: {description}",
            details=[f"CITATION.cff: {(path / 'CITATION.cff').exists()}"],
            rsqkit_url="https://fair-software.eu/recommendations/citation",
            category="fair",
        )

    if principle_id == "checklist":
        # Check for quality checklist / CI / static analysis
        checklist_indicators = [
            path / ".github" / "workflows",
            path / "pyproject.toml",
            path / "tox.ini",
            path / ".pre-commit-config.yaml",
        ]
        found = [str(p.relative_to(path)) for p in checklist_indicators if p.exists()]
        has_checklist = len(found) >= 2
        return CheckResult(
            name="FAIR: checklist",
            status=CheckStatus.PASS if has_checklist else CheckStatus.WARN,
            message=f"{'Quality checklist indicators found' if has_checklist else 'Limited quality checklist'}: {description}",
            details=[f"Found: {', '.join(found)}" if found else "None"],
            rsqkit_url="https://fair-software.eu/recommendations/checklist",
            category="fair",
        )

    return CheckResult(
        name=f"FAIR: {principle_id}",
        status=CheckStatus.NA,
        message=description,
        rsqkit_url="https://fair-software.eu/",
        category="fair",
    )
