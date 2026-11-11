"""Check: Static analysis tools configuration (linters, formatters)."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

LINTER_CONFIGS = {
    "ruff": ["ruff.toml", "pyproject.toml"],
    "mypy": [".mypy.ini", "mypy.ini", "setup.cfg", "pyproject.toml"],
    "flake8": [".flake8", "setup.cfg", "tox.ini"],
    "pylint": [".pylintrc", "pylintrc", "pyproject.toml"],
    "eslint": [".eslintrc.js", ".eslintrc.json", ".eslintrc.yml", "eslint.config.js"],
    "prettier": [".prettierrc", ".prettierrc.json", ".prettierrc.yml", "prettier.config.js"],
    "clang-tidy": [".clang-tidy"],
    "lintr": [".lintr"],
    "JuliaFormatter": [".JuliaFormatter.toml"],
}


def _check_config_mentions(path: Path, config_file: str, tool_names: list[str]) -> list[str]:
    cfg = path / config_file
    if not cfg.exists():
        return []
    content = cfg.read_text(errors="ignore").lower()
    return [name for name in tool_names if name in content]


def check_static_analysis(repo_path: str, language: str | None = None) -> CheckResult:
    path = Path(repo_path)
    found_tools: list[str] = []

    # Check for dedicated config files
    for tool, configs in LINTER_CONFIGS.items():
        for cfg in configs:
            if cfg == "pyproject.toml" or cfg == "setup.cfg":
                continue
            if (path / cfg).exists():
                found_tools.append(tool)
                break

    # Check pyproject.toml for tool mentions
    pp_mentions = _check_config_mentions(path, "pyproject.toml", ["ruff", "mypy", "pylint", "flake8"])
    for tool in pp_mentions:
        if tool not in found_tools:
            found_tools.append(tool)

    # Check setup.cfg for tool mentions
    sc_mentions = _check_config_mentions(path, "setup.cfg", ["flake8", "mypy", "pylint"])
    for tool in sc_mentions:
        if tool not in found_tools:
            found_tools.append(tool)

    # Check package.json for JS linters
    pj = path / "package.json"
    if pj.exists():
        content = pj.read_text(errors="ignore").lower()
        for tool in ["eslint", "prettier"]:
            if tool in content and tool not in found_tools:
                found_tools.append(tool)

    details = [f"Linting tools configured: {', '.join(found_tools) if found_tools else 'none'}"]

    if not found_tools:
        return CheckResult(
            name="Static analysis",
            status=CheckStatus.WARN,
            message="No linter or formatter configuration found",
            details=details,
            recommendations=[
                "Configure a linter (ruff for Python, eslint for JS, clang-tidy for C++)",
                "Add a formatter (ruff format or black for Python, prettier for JS)",
            ],
            rsqkit_url="https://everse.software/RSQKit/static_analysis",
            category="quality",
        )

    has_linter = any(t in found_tools for t in ["ruff", "mypy", "flake8", "pylint", "eslint", "clang-tidy", "lintr"])
    has_formatter = any(t in found_tools for t in ["ruff", "prettier", "JuliaFormatter"])

    if has_linter and has_formatter:
        status = CheckStatus.PASS
        msg = f"Static analysis tools configured ({', '.join(found_tools)})"
    else:
        status = CheckStatus.WARN
        msg = f"Partial static analysis config ({', '.join(found_tools)})"

    recs = []
    if not has_formatter:
        recs.append("Add a code formatter (ruff format or black for Python, prettier for JS)")

    return CheckResult(
        name="Static analysis",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/static_analysis",
        category="quality",
    )
