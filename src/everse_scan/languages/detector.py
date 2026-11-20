"""Language detection for everse-scan."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

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
    "*.egg-info",
    ".tox",
    ".hypothesis",
    "htmlcov",
    ".coverage",
    # Generated/build/IDE output that would skew language detection
    "doxygen",
    "cmake-build-debug",
    "cmake-build-release",
    ".idea",
}

CONFIG_FILES = {
    "pyproject.toml": "Python",
    "setup.py": "Python",
    "setup.cfg": "Python",
    "requirements.txt": "Python",
    "requirements-dev.txt": "Python",
    "package.json": "JavaScript/TypeScript",
    "tsconfig.json": "JavaScript/TypeScript",
    "Cargo.toml": "Rust",
    "DESCRIPTION": "R",
    "NAMESPACE": "R",
    "Project.toml": "Julia",
    "CMakeLists.txt": "C/C++",
    "go.mod": "Go",
    "pom.xml": "Java",
    "build.gradle": "Java",
    "Gemfile": "Ruby",
}

VERSION_FILES = {
    ".python-version": "Python",
    ".ruby-version": "Ruby",
    ".node-version": "JavaScript/TypeScript",
}

EXTENSION_MAP = {
    ".py": "Python",
    ".js": "JavaScript/TypeScript",
    ".ts": "JavaScript/TypeScript",
    ".jsx": "JavaScript/TypeScript",
    ".tsx": "JavaScript/TypeScript",
    ".R": "R",
    ".r": "R",
    ".jl": "Julia",
    ".c": "C/C++",
    ".cpp": "C/C++",
    ".cc": "C/C++",
    ".h": "C/C++",
    ".hpp": "C/C++",
    ".rs": "Rust",
    ".go": "Go",
    ".java": "Java",
    ".rb": "Ruby",
}


@dataclass
class LanguageInfo:
    languages: list[str] = field(default_factory=list)
    primary: str | None = None
    counts: dict[str, int] = field(default_factory=dict)


def _should_ignore_dir(dirpath: str) -> bool:
    for part in Path(dirpath).parts:
        if part in IGNORE_DIRS:
            return True
    return False


def detect_languages(repo_path: str) -> LanguageInfo:
    """Detect programming languages in a repository."""
    path = Path(repo_path)
    counts: dict[str, int] = {}

    # Check config files at root
    for config_file, lang in CONFIG_FILES.items():
        if (path / config_file).exists():
            counts[lang] = counts.get(lang, 0) + 5

    # Check version files at root
    for version_file, lang in VERSION_FILES.items():
        if (path / version_file).exists():
            counts[lang] = counts.get(lang, 0) + 3

    # Count source files by extension
    for root, dirs, files in os.walk(path):
        if _should_ignore_dir(root):
            dirs.clear()
            continue
        for f in files:
            ext = Path(f).suffix
            lang = EXTENSION_MAP.get(ext)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1

    if not counts:
        return LanguageInfo()

    sorted_langs = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    languages = [lang for lang, _ in sorted_langs]
    primary = sorted_langs[0][0] if sorted_langs else None

    return LanguageInfo(languages=languages, primary=primary, counts=counts)
