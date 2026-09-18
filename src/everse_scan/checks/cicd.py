"""Check: CI/CD configuration."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

CI_PATHS = {
    ".github/workflows": "GitHub Actions",
    ".gitlab-ci.yml": "GitLab CI",
    "Jenkinsfile": "Jenkins",
    ".circleci/config.yml": "CircleCI",
    ".travis.yml": "Travis CI",
    "azure-pipelines.yml": "Azure Pipelines",
}


def _check_workflow_content(path: Path) -> dict[str, bool]:
    has_test_job = False
    has_lint_job = False
    has_matrix = False
    workflows_dir = path / ".github" / "workflows"
    if workflows_dir.is_dir():
        for wf in workflows_dir.glob("*.yml"):
            content = wf.read_text(errors="ignore").lower()
            if "test" in content or "pytest" in content or "npm test" in content:
                has_test_job = True
            if "lint" in content or "ruff" in content or "eslint" in content or "flake8" in content:
                has_lint_job = True
            if "matrix" in content:
                has_matrix = True
    return {"test": has_test_job, "lint": has_lint_job, "matrix": has_matrix}


def check_cicd(repo_path: str) -> CheckResult:
    path = Path(repo_path)

    found_ci = []
    for ci_path, ci_name in CI_PATHS.items():
        if (path / ci_path).exists() or (path / ci_path).is_dir():
            found_ci.append(ci_name)

    if not found_ci:
        return CheckResult(
            name="CI/CD",
            status=CheckStatus.FAIL,
            message="No CI/CD configuration found",
            details=["No .github/workflows/, .gitlab-ci.yml, Jenkinsfile, or other CI config found"],
            recommendations=["Create a GitHub Actions workflow for automated testing"],
            rsqkit_url="https://everse.software/RSQKit/ci_cd",
            category="quality",
        )

    wf_info = _check_workflow_content(path)
    has_dependabot = (path / ".github" / "dependabot.yml").exists()

    details = [
        f"CI system: {', '.join(found_ci)}",
        f"Test job: {'yes' if wf_info['test'] else 'no'}",
        f"Lint job: {'yes' if wf_info['lint'] else 'no'}",
        f"Matrix builds: {'yes' if wf_info['matrix'] else 'no'}",
        f"Dependabot: {'yes' if has_dependabot else 'no'}",
    ]

    score = sum([wf_info["test"], wf_info["lint"], has_dependabot])

    recs = []
    if not wf_info["test"]:
        recs.append("Add a test job to your CI pipeline")
    if not wf_info["lint"]:
        recs.append("Add a linting job (ruff for Python, eslint for JS)")
    if not has_dependabot:
        recs.append("Add Dependabot for dependency updates (.github/dependabot.yml)")

    if score >= 3:
        status = CheckStatus.PASS
        msg = f"CI/CD well configured ({', '.join(found_ci)})"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = f"CI/CD present but minimal ({', '.join(found_ci)})"
    else:
        status = CheckStatus.WARN
        msg = f"CI/CD configured but no test/lint jobs ({', '.join(found_ci)})"

    return CheckResult(
        name="CI/CD",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/ci_cd",
        category="quality",
    )
