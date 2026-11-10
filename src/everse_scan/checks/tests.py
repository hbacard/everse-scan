"""Check: Test presence and framework."""

from __future__ import annotations

import os
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus


def _find_test_files(path: Path) -> list[str]:
    test_patterns = [
        "test_*.py",
        "*_test.py",
        "test-*.R",
        "*.test.js",
        "*.spec.js",
        "test_*.cpp",
        "*.test.ts",
        "*.spec.ts",
    ]
    results: list[str] = []
    ignore_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}
    for root, dirs, files in os.walk(path):
        if any(p in ignore_dirs for p in Path(root).parts):
            dirs.clear()
            continue
        for f in files:
            for pattern in test_patterns:
                if Path(f).match(pattern):
                    results.append(str(Path(root) / f))
                    break
    return results


def _detect_test_framework(path: Path, language: str | None) -> str | None:
    if language == "Python" or language is None:
        for cfg in ["pyproject.toml", "setup.cfg", "tox.ini"]:
            cfg_path = path / cfg
            if cfg_path.exists():
                content = cfg_path.read_text(errors="ignore").lower()
                if "pytest" in content:
                    return "pytest"
                if "unittest" in content:
                    return "unittest"
        conftest = path / "conftest.py"
        if conftest.exists():
            return "pytest"

    if language == "JavaScript/TypeScript":
        pkg = path / "package.json"
        if pkg.exists():
            content = pkg.read_text(errors="ignore").lower()
            for fw in ["jest", "vitest", "mocha"]:
                if fw in content:
                    return fw

    if language == "R":
        testthat = path / "tests" / "testthat"
        if testthat.exists():
            return "testthat"

    if language == "Julia":
        runtests = path / "test" / "runtests.jl"
        if runtests.exists():
            return "Test.jl"

    return None


def check_tests(repo_path: str, language: str | None = None) -> CheckResult:
    path = Path(repo_path)
    test_files = _find_test_files(path)
    framework = _detect_test_framework(path, language)

    has_tests_dir = (path / "tests").is_dir() or (path / "test").is_dir()

    # Check for coverage config
    coverage_tools = []
    if language == "Python" or language is None:
        for cfg in ["pyproject.toml", "setup.cfg"]:
            cfg_path = path / cfg
            if cfg_path.exists():
                content = cfg_path.read_text(errors="ignore").lower()
                if "coverage" in content or "pytest-cov" in content:
                    coverage_tools.append("coverage/pytest-cov")
    if language == "JavaScript/TypeScript":
        pkg = path / "package.json"
        if pkg.exists():
            content = pkg.read_text(errors="ignore").lower()
            if "nyc" in content or "c8" in content:
                coverage_tools.append("nyc/c8")

    details = [
        f"Test files found: {len(test_files)}",
        f"Test framework: {framework or 'not detected'}",
        f"Tests directory: {'yes' if has_tests_dir else 'no'}",
        f"Coverage tool: {', '.join(coverage_tools) if coverage_tools else 'none'}",
    ]

    if test_files and framework:
        status = CheckStatus.PASS
        msg = f"Tests found ({len(test_files)} files, framework: {framework})"
    elif test_files:
        status = CheckStatus.WARN
        msg = f"Test files found ({len(test_files)}) but no framework detected"
    else:
        status = CheckStatus.FAIL
        msg = "No test files found"

    recs = []
    if not test_files:
        fw_rec = {
            "Python": "pytest",
            "JavaScript/TypeScript": "jest",
            "R": "testthat",
            "Julia": "Test.jl",
            "C/C++": "Google Test / CTest",
        }
        rec_fw = fw_rec.get(language or "", "a testing framework")
        recs.append(f"Create a tests/ directory with {rec_fw}")
    elif not framework:
        recs.append("Configure a test framework (pytest recommended for Python)")
    if not coverage_tools:
        recs.append("Add coverage measurement (pytest-cov for Python)")

    return CheckResult(
        name="Tests",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/testing_software",
        category="quality",
    )
