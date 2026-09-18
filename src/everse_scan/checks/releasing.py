"""Check: Releasing practices (tags, CHANGELOG, semantic versioning)."""

from __future__ import annotations

import subprocess
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

SEMVER_PATTERN = r"v?\d+\.\d+\.\d+"


def _git_tags(path: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "tag"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return [t.strip() for t in result.stdout.splitlines() if t.strip()]
    except Exception:
        return []


def check_releasing(repo_path: str) -> CheckResult:
    path = Path(repo_path)

    tags = _git_tags(path)
    has_changelog = (path / "CHANGELOG.md").exists() or (path / "CHANGES.md").exists() or (path / "CHANGES.rst").exists()

    # Check for semver compliance
    import re
    semver_tags = [t for t in tags if re.match(SEMVER_PATTERN, t.lstrip("v"))]
    has_semver = len(semver_tags) > 0

    # Check for GitHub releases (can't verify locally, but .github/release.yml exists?)
    has_release_template = (path / ".github" / "release.yml").exists() or (path / ".github" / "release-drafter.yml").exists()

    details = [
        f"Git tags: {len(tags)} ({', '.join(tags[:5]) if tags else 'none'})",
        f"Semantic versioning: {'yes' if has_semver else 'no'}",
        f"CHANGELOG: {'yes' if has_changelog else 'no'}",
        f"Release template: {'yes' if has_release_template else 'no'}",
    ]

    score = sum([len(tags) > 0, has_semver, has_changelog])

    recs = []
    if not tags:
        recs.append("Create version tags (git tag v0.1.0)")
    if not has_semver and tags:
        recs.append("Use semantic versioning for tags (v1.0.0, v1.1.0, etc.)")
    if not has_changelog:
        recs.append("Add a CHANGELOG.md to track release changes")

    if score >= 3:
        status = CheckStatus.PASS
        msg = f"Good releasing practices ({len(tags)} tags, semver, changelog)"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = f"Partial releasing practices ({len(tags)} tags)"
    else:
        status = CheckStatus.WARN
        msg = "No releasing practices found"

    return CheckResult(
        name="Releasing",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/releasing_software",
        category="quality",
    )
