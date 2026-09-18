"""Check: Code review practices (PR templates, CODEOWNERS, branch protection)."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

PR_TEMPLATE_PATHS = [
    ".github/pull_request_template.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/pull_request_template/",
    "docs/pull_request_template.md",
]


def check_code_review(repo_path: str) -> CheckResult:
    path = Path(repo_path)

    has_pr_template = any((path / p).exists() or (path / p).is_dir() for p in PR_TEMPLATE_PATHS)

    has_codeowners = False
    for p in [path / ".github" / "CODEOWNERS", path / "CODEOWNERS"]:
        if p.exists():
            has_codeowners = True
            break

    has_contributing = False
    for p in [path / "CONTRIBUTING.md", path / ".github" / "CONTRIBUTING.md", path / "docs" / "CONTRIBUTING.md"]:
        if p.exists():
            has_contributing = True
            break

    # Branch protection can't be checked locally, note it
    has_issue_template = (path / ".github" / "ISSUE_TEMPLATE").is_dir()

    details = [
        f"PR template: {'yes' if has_pr_template else 'no'}",
        f"CODEOWNERS: {'yes' if has_codeowners else 'no'}",
        f"CONTRIBUTING.md: {'yes' if has_contributing else 'no'}",
        f"Issue templates: {'yes' if has_issue_template else 'no'}",
    ]

    score = sum([has_pr_template, has_codeowners, has_contributing])

    recs = []
    if not has_pr_template:
        recs.append("Add a PR template (.github/pull_request_template.md)")
    if not has_codeowners:
        recs.append("Add a CODEOWNERS file for review accountability")
    if not has_contributing:
        recs.append("Add a CONTRIBUTING.md with contribution guidelines")

    if score >= 2:
        status = CheckStatus.PASS
        msg = "Good code review practices"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = "Partial code review configuration"
    else:
        status = CheckStatus.WARN
        msg = "No code review practices found"

    return CheckResult(
        name="Code review",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/code_review",
        category="collaboration",
    )
