"""Check: Project structure quality."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".eggs",
    # Generated/build/IDE output that would skew structure listing
    "cmake-build-debug",
    "cmake-build-release",
    ".idea",
}

# Standard dirs across ecosystems (GitHub/Python + GitLab/C++ CMake layouts)
EXPECTED_DIRS = {
    "src",
    "source",
    "tests",
    "test",
    "docs",
    "doc",
    "documentation",
    "documentations",
    "examples",
    "example",
    "GTest",
    "gtest",
}


def _list_top_dirs(path: Path) -> set[str]:
    return {f.name for f in path.iterdir() if f.is_dir() and f.name not in IGNORE_DIRS}


def _has_src_layout(path: Path) -> bool:
    src = path / "src"
    if not src.is_dir():
        return False
    return any(p.is_dir() for p in src.iterdir())


def check_structure(repo_path: str) -> CheckResult:
    path = Path(repo_path)
    top_dirs = _list_top_dirs(path)

    found_expected = EXPECTED_DIRS & top_dirs
    EXPECTED_DIRS - top_dirs

    has_src = _has_src_layout(path)
    has_tests = bool(top_dirs & {"tests", "test", "GTest", "gtest"})
    has_docs = bool(top_dirs & {"docs", "doc", "documentation", "documentations"})

    details = [
        f"Top-level directories: {', '.join(sorted(top_dirs))}" if top_dirs else "No directories found",
        f"src/ layout: {'yes' if has_src else 'no'}",
        f"tests/ directory: {'yes' if has_tests else 'no'}",
        f"docs/ directory: {'yes' if has_docs else 'no'}",
    ]

    score = sum([has_src, has_tests, has_docs])

    if score >= 3:
        status = CheckStatus.PASS
        msg = "Well-structured project with src/, tests/, and docs/"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = f"Partially structured (found: {', '.join(sorted(found_expected))})"
    else:
        status = CheckStatus.FAIL
        msg = "Flat structure, no standard directories found"

    recs = []
    if not has_src:
        recs.append("Consider using a src/ layout for source code")
    if not has_tests:
        recs.append("Create a tests/ directory for test files")
    if not has_docs:
        recs.append("Create a documentation directory (docs/ or documentation/)")

    return CheckResult(
        name="Structure",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/software_project_structure",
        category="quality",
    )
