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


def _check_gitlab_ci_content(path: Path) -> dict[str, bool]:
    """Analyze .gitlab-ci.yml (jobs + script) for test/lint/matrix, like the GitHub workflows scan."""
    has_test_job = False
    has_lint_job = False
    has_matrix = False
    ci_file = path / ".gitlab-ci.yml"
    if ci_file.exists():
        content = ci_file.read_text(errors="ignore").lower()
        if any(k in content for k in ("test", "pytest", "ctest", "gtest", "unittest")):
            has_test_job = True
        if any(k in content for k in ("lint", "clang-tidy", "cppcheck", "ruff", "eslint")):
            has_lint_job = True
        if "matrix" in content or "parallel:" in content:
            has_matrix = True
    return {"test": has_test_job, "lint": has_lint_job, "matrix": has_matrix}


def _has_dependency_bot(path: Path) -> bool:
    """Dependabot on GitHub, Renovate on GitLab (or GitHub)."""
    return (
        (path / ".github" / "dependabot.yml").exists()
        or (path / "renovate.json").exists()
        or (path / ".renovaterc").exists()
        or (path / ".renovaterc.json").exists()
    )


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

    gh_info = _check_workflow_content(path)
    gl_info = _check_gitlab_ci_content(path)
    # Merge both forge formats so GitLab content is not scored as absent
    wf_info = {
        "test": gh_info["test"] or gl_info["test"],
        "lint": gh_info["lint"] or gl_info["lint"],
        "matrix": gh_info["matrix"] or gl_info["matrix"],
    }
    has_dependabot = _has_dependency_bot(path)

    details = [
        f"CI system: {', '.join(found_ci)}",
        f"Test job: {'yes' if wf_info['test'] else 'no'}",
        f"Lint job: {'yes' if wf_info['lint'] else 'no'}",
        f"Matrix builds: {'yes' if wf_info['matrix'] else 'no'}",
        f"Dependency bot (Dependabot/Renovate): {'yes' if has_dependabot else 'no'}",
    ]

    score = sum([wf_info["test"], wf_info["lint"], has_dependabot])

    recs = []
    if not wf_info["test"]:
        recs.append("Add a test job to your CI pipeline")
    if not wf_info["lint"]:
        recs.append("Add a linting job (ruff for Python, eslint for JS)")
    if not has_dependabot:
        recs.append("Add Dependabot (.github/dependabot.yml) or Renovate (renovate.json) for dependency updates")

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
