"""Check: Version control practices."""

from __future__ import annotations

import subprocess
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

COMMON_GITIGNORE_ENTRIES = ["__pycache__", ".venv", "venv", "node_modules", "dist", "build", ".env"]


def _run_git(args: list[str], cwd: str) -> str:
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def check_version_control(repo_path: str) -> CheckResult:
    path = Path(repo_path)
    git_dir = path / ".git"

    if not git_dir.exists():
        return CheckResult(
            name="Version control",
            status=CheckStatus.FAIL,
            message="Not a git repository",
            details=["No .git directory found"],
            recommendations=["Initialize git: git init", "Create a .gitignore appropriate for your language"],
            rsqkit_url="https://everse.software/RSQKit/using_version_control",
            category="quality",
        )

    cwd = str(path)
    commit_count_str = _run_git(["rev-list", "--count", "HEAD"], cwd)
    commit_count = int(commit_count_str) if commit_count_str.isdigit() else 0

    authors_str = _run_git(["log", "--format=%aN"], cwd)
    authors = {a.strip() for a in authors_str.splitlines() if a.strip()}
    author_count = len(authors)

    tags_str = _run_git(["tag"], cwd)
    tags = [t for t in tags_str.splitlines() if t.strip()]
    tag_count = len(tags)

    gitignore = path / ".gitignore"
    gitignore_content = gitignore.read_text(errors="ignore").lower() if gitignore.exists() else ""

    gitignore_quality = 0
    for entry in COMMON_GITIGNORE_ENTRIES:
        if entry in gitignore_content:
            gitignore_quality += 1

    details = [
        f"Commits: {commit_count}",
        f"Authors: {author_count}",
        f"Tags/releases: {tag_count}",
        f".gitignore: {'present' if gitignore.exists() else 'missing'} "
        f"({gitignore_quality}/{len(COMMON_GITIGNORE_ENTRIES)} common entries)",
    ]

    recs = []
    if not gitignore.exists():
        recs.append("Create a .gitignore file")
    elif gitignore_quality < 3:
        recs.append("Add more common entries to .gitignore (venv, __pycache__, .env, etc.)")
    if tag_count == 0:
        recs.append("Create tags for version releases (git tag v0.1.0)")

    if gitignore.exists() and gitignore_quality >= 3 and tag_count > 0:
        status = CheckStatus.PASS
        msg = f"Git repository with good .gitignore and {tag_count} release(s)"
    elif git_dir.exists():
        score = sum([gitignore.exists(), gitignore_quality >= 3, tag_count > 0, commit_count > 10])
        status = CheckStatus.WARN if score < 3 else CheckStatus.PASS
        msg = f"Git repository ({commit_count} commits, {author_count} authors, {tag_count} tags)"
    else:
        status = CheckStatus.FAIL
        msg = "Not a git repository"

    return CheckResult(
        name="Version control",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/using_version_control",
        category="quality",
    )
