"""Lifecycle stage detection (early / active_dev / maintenance / published)."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

LIFECYCLE_EARLY = "early"
LIFECYCLE_ACTIVE = "active_dev"
LIFECYCLE_MAINTENANCE = "maintenance"
LIFECYCLE_PUBLISHED = "published"


@dataclass
class LifecycleResult:
    stage: str
    justification: str


def _git_commit_count(path: Path) -> int:
    try:
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
    except Exception:
        return 0


def _git_recent_commits(path: Path, months: int = 3) -> int:
    try:
        result = subprocess.run(
            ["git", "log", f"--since={months} months ago", "--oneline"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return len([l for l in result.stdout.splitlines() if l.strip()])
    except Exception:
        return 0


def _git_tag_count(path: Path) -> int:
    try:
        result = subprocess.run(
            ["git", "tag"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return len([t for t in result.stdout.splitlines() if t.strip()])
    except Exception:
        return 0


def _has_doi(path: Path) -> bool:
    if (path / ".zenodo.json").exists():
        return True
    readme = path / "README.md"
    if readme.exists():
        try:
            content = readme.read_text(errors="ignore").lower()
            if "doi.org" in content or "zenodo" in content:
                return True
        except Exception:
            pass
    return False


def detect_lifecycle(repo_path: str) -> LifecycleResult:
    """Detect the lifecycle stage of a repository."""
    path = Path(repo_path)

    commit_count = _git_commit_count(path)
    recent_commits = _git_recent_commits(path)
    tag_count = _git_tag_count(path)
    has_doi = _has_doi(path)

    if has_doi and commit_count > 0 and recent_commits < 5:
        return LifecycleResult(
            stage=LIFECYCLE_PUBLISHED,
            justification=f"DOI present, minimal recent activity ({recent_commits} commits in 3 months)",
        )

    if tag_count > 0 and recent_commits < 5:
        return LifecycleResult(
            stage=LIFECYCLE_MAINTENANCE,
            justification=f"Releases present ({tag_count} tags), low recent activity ({recent_commits} commits in 3 months)",
        )

    if commit_count < 10:
        return LifecycleResult(
            stage=LIFECYCLE_EARLY,
            justification=f"< 10 commits ({commit_count}), no tags, early development",
        )

    return LifecycleResult(
        stage=LIFECYCLE_ACTIVE,
        justification=f"Regular commits ({recent_commits} in last 3 months, {commit_count} total), active development",
    )
