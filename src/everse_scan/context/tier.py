"""Three-tier model detection (script / tool / infrastructure)."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

TIER_SCRIPT = "script"
TIER_TOOL = "tool"
TIER_INFRA = "infrastructure"

PACKAGING_FILES = {
    "pyproject.toml", "setup.py", "package.json", "Cargo.toml",
    "DESCRIPTION", "Project.toml", "CMakeLists.txt",
}

CI_PATHS = [
    ".github/workflows",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    ".circleci/config.yml",
    ".travis.yml",
    "azure-pipelines.yml",
]


@dataclass
class TierResult:
    tier: str
    justification: str
    checks_adjusted: list[str]

    @property
    def is_script(self) -> bool:
        return self.tier == TIER_SCRIPT

    @property
    def is_tool(self) -> bool:
        return self.tier == TIER_TOOL

    @property
    def is_infrastructure(self) -> bool:
        return self.tier == TIER_INFRA


def _count_source_files(path: Path) -> int:
    source_exts = {".py", ".js", ".ts", ".jsx", ".tsx", ".R", ".r", ".jl",
                   ".c", ".cpp", ".cc", ".h", ".hpp", ".rs", ".go", ".java", ".rb"}
    ignore_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__",
                   "dist", "build", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    count = 0
    for root, dirs, files in os.walk(path):
        if any(p in ignore_dirs for p in Path(root).parts):
            dirs.clear()
            continue
        for f in files:
            if Path(f).suffix in source_exts:
                count += 1
    return count


def _has_packaging(path: Path) -> bool:
    return any((path / f).exists() for f in PACKAGING_FILES)


def _has_tests(path: Path) -> bool:
    tests_dir = path / "tests"
    test_dir = path / "test"
    if tests_dir.is_dir() or test_dir.is_dir():
        return True
    # Check for test files at root
    for f in path.iterdir():
        if f.is_file() and (f.name.startswith("test_") or f.name.endswith("_test.py")):
            return True
    return False


def _count_git_authors(path: Path) -> int:
    try:
        result = subprocess.run(
            ["git", "log", "--format=%aN"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        authors = {line.strip() for line in result.stdout.splitlines() if line.strip()}
        return len(authors)
    except Exception:
        return 0


def _has_releases(path: Path) -> int:
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


def _has_ci(path: Path) -> bool:
    for ci_path in CI_PATHS:
        if (path / ci_path).exists() or (path / ci_path).is_dir():
            return True
    return False


def _has_docker(path: Path) -> bool:
    return (path / "Dockerfile").exists() or (path / "docker-compose.yml").exists()


def _has_extensive_docs(path: Path) -> bool:
    docs = path / "docs"
    if not docs.is_dir():
        return False
    md_files = list(docs.rglob("*.md")) + list(docs.rglob("*.rst"))
    return len(md_files) >= 3


def detect_tier(repo_path: str) -> TierResult:
    """Detect the software tier (script / tool / infrastructure)."""
    path = Path(repo_path)

    source_count = _count_source_files(path)
    has_packaging = _has_packaging(path)
    has_tests = _has_tests(path)
    author_count = _count_git_authors(path)
    release_count = _has_releases(path)
    has_ci = _has_ci(path)
    has_docker = _has_docker(path)
    has_docs = _has_extensive_docs(path)

    # Tier 3: Infrastructure
    infra_signals = sum([
        has_ci and has_docker,
        has_docs and has_ci,
        author_count > 5,
        release_count > 3,
        has_packaging and has_ci and has_docker,
    ])
    if infra_signals >= 3:
        return TierResult(
            tier=TIER_INFRA,
            justification=(
                f"Multi-package or complex CI, Docker={'yes' if has_docker else 'no'}, "
                f"docs={'extensive' if has_docs else 'minimal'}, "
                f"contributors={author_count}, releases={release_count}"
            ),
            checks_adjusted=[],
        )

    # Tier 1: Script
    script_signals = sum([
        source_count < 10,
        not has_packaging,
        not has_tests,
        author_count <= 1,
        release_count == 0,
    ])
    if script_signals >= 4:
        return TierResult(
            tier=TIER_SCRIPT,
            justification=(
                f"< 10 source files ({source_count}), no packaging, "
                f"no tests, {author_count} author(s), no releases"
            ),
            checks_adjusted=["codemeta.json", "CI/CD", "packaging", "containers"],
        )

    # Tier 2: Tool / Library
    return TierResult(
        tier=TIER_TOOL,
        justification=(
            f"Packaging={'yes' if has_packaging else 'no'}, "
            f"{author_count} author(s), tests={'yes' if has_tests else 'no'}, "
            f"source files={source_count}"
        ),
        checks_adjusted=[],
    )
