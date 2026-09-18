"""Check: Readable code (formatting conventions)."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

FORMATTER_CONFIGS = {
    "ruff": ["ruff.toml", "pyproject.toml"],
    "black": ["pyproject.toml", "setup.cfg", ".black"],
    "isort": [".isort.cfg", "pyproject.toml", "setup.cfg"],
    "prettier": [".prettierrc", ".prettierrc.json", ".prettierrc.yml", "prettier.config.js"],
    "clang-format": [".clang-format"],
    "styler": [".lintr"],
    "JuliaFormatter": [".JuliaFormatter.toml"],
    "rustfmt": ["rustfmt.toml", ".rustfmt.toml"],
}

EDITORCONFIG = ".editorconfig"


def _check_pyproject_for_formatters(path: Path) -> list[str]:
    pp = path / "pyproject.toml"
    if not pp.exists():
        return []
    content = pp.read_text(errors="ignore").lower()
    found = []
    for tool in ["ruff", "black", "isort"]:
        if f"[tool.{tool}]" in content or f"[{tool}]" in content:
            found.append(tool)
    return found


def check_readable_code(repo_path: str, language: str | None = None) -> CheckResult:
    path = Path(repo_path)

    found_formatters: list[str] = []

    # Check for dedicated formatter config files
    for tool, configs in FORMATTER_CONFIGS.items():
        for cfg in configs:
            if cfg in ("pyproject.toml", "setup.cfg"):
                continue
            if (path / cfg).exists():
                found_formatters.append(tool)
                break

    # Check pyproject.toml for formatter mentions
    pp_formatters = _check_pyproject_for_formatters(path)
    for tool in pp_formatters:
        if tool not in found_formatters:
            found_formatters.append(tool)

    # Check package.json for prettier
    pj = path / "package.json"
    if pj.exists():
        content = pj.read_text(errors="ignore").lower()
        if "prettier" in content and "prettier" not in found_formatters:
            found_formatters.append("prettier")

    has_editorconfig = (path / EDITORCONFIG).exists()

    details = [
        f"Formatters configured: {', '.join(found_formatters) if found_formatters else 'none'}",
        f".editorconfig: {'yes' if has_editorconfig else 'no'}",
    ]

    score = sum([len(found_formatters) > 0, has_editorconfig])

    recs = []
    if not found_formatters:
        tool_rec = {"Python": "ruff format or black", "JavaScript/TypeScript": "prettier",
                    "C/C++": "clang-format", "R": "styler"}.get(language or "", "a code formatter")
        recs.append(f"Configure {tool_rec}")
    if not has_editorconfig:
        recs.append("Add an .editorconfig for consistent editor settings")

    if score >= 2:
        status = CheckStatus.PASS
        msg = f"Code formatting configured ({', '.join(found_formatters)})"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = f"Partial formatting config ({', '.join(found_formatters)})"
    else:
        status = CheckStatus.WARN
        msg = "No code formatting configuration found"

    return CheckResult(
        name="Readable code",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/writing_readable_code",
        category="quality",
    )
