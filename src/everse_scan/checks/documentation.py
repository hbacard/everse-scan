"""Check: Documentation presence and quality."""

from __future__ import annotations

import os
import re
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

DOC_SITE_FILES = {
    "mkdocs.yml": "MkDocs",
    "conf.py": "Sphinx",
    ".readthedocs.yaml": "Read the Docs",
    ".readthedocs.yml": "Read the Docs",
    "docusaurus.config.js": "Docusaurus",
    "docusaurus.config.ts": "Docusaurus",
    "_pkgdown.yml": "pkgdown",
}

# Real projects use docs/, doc/, documentation/ or documentations/
DOC_DIR_NAMES = ("docs", "doc", "documentation", "documentations")


def _find_docs_dir(path: Path) -> Path | None:
    for name in DOC_DIR_NAMES:
        d = path / name
        if d.is_dir():
            return d
    return None

DOCSTRING_PATTERNS = {
    "Python": [r'"""', r"'''"],
    "JavaScript/TypeScript": [r"/\*\*", r"//"],
    "R": [r"#'"],
    "C/C++": [r"/\*\*", r"//"],
    "Julia": [r'"""'],
}

SOURCE_EXTENSIONS = {".py", ".js", ".ts", ".R", ".r", ".jl", ".c", ".cpp", ".cc", ".h", ".hpp"}


def _count_docstrings(path: Path, language: str | None) -> int:
    patterns = DOCSTRING_PATTERNS.get(language or "Python", [r'"""'])
    count = 0
    ignore_dirs = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        "dist",
        "build",
        # Generated/build/IDE output that would skew docstring counting
        "doxygen",
        "cmake-build-debug",
        "cmake-build-release",
        ".idea",
    }
    for root, dirs, files in os.walk(path):
        if any(p in ignore_dirs for p in Path(root).parts):
            dirs.clear()
            continue
        for f in files:
            if Path(f).suffix in SOURCE_EXTENSIONS:
                content = (Path(root) / f).read_text(errors="ignore")
                for pattern in patterns:
                    count += len(re.findall(pattern, content))
    return count


def check_documentation(repo_path: str, language: str | None = None) -> CheckResult:
    path = Path(repo_path)

    docs_dir = _find_docs_dir(path)
    has_docs_dir = docs_dir is not None
    docs_file_count = 0
    if has_docs_dir:
        assert docs_dir is not None
        docs_file_count = len(list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.rst")))

    doc_sites = []
    for fname, tool in DOC_SITE_FILES.items():
        if (path / fname).exists():
            doc_sites.append(tool)

    docstring_count = _count_docstrings(path, language)

    readme = path / "README.md"
    has_readme = readme.exists()
    readme_quality = len(readme.read_text(errors="ignore")) if has_readme else 0

    details = [
        f"Documentation dir: {'yes (' + docs_dir.name + '/)' if has_docs_dir else 'no'} ({docs_file_count} files)",
        f"Doc site configs: {', '.join(doc_sites) if doc_sites else 'none'}",
        f"Docstrings found: {docstring_count}",
        f"README: {'present' if has_readme else 'missing'} ({readme_quality} chars)",
    ]

    score = sum(
        [
            has_docs_dir and docs_file_count > 0,
            bool(doc_sites),
            docstring_count > 5,
            has_readme and readme_quality > 200,
        ]
    )

    if score >= 3:
        status = CheckStatus.PASS
        msg = "Good documentation coverage"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = "Partial documentation"
    else:
        status = CheckStatus.FAIL
        msg = "No documentation found"

    recs = []
    if not has_docs_dir:
        recs.append("Create a documentation directory (docs/ or documentation/)")
    if not doc_sites:
        tool_rec = {"Python": "Sphinx or MkDocs", "R": "pkgdown", "JavaScript/TypeScript": "Docusaurus"}.get(
            language or "", "a documentation generator"
        )
        recs.append(f"Set up {tool_rec} for documentation generation")
    if docstring_count < 5:
        recs.append("Add docstrings to public functions/classes")

    return CheckResult(
        name="Documentation",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/software_documentation",
        category="quality",
    )
