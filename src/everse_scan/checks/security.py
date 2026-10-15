"""Check: Security practices (secrets, dependabot, CODEOWNERS)."""

from __future__ import annotations

import os
import re
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"-----BEGIN (RSA |EC )?PRIVATE KEY-----", "Private key"),
    (r"api[_-]?key\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]", "Hardcoded API key"),
    (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password"),
]

SECRET_FILE_EXTS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".env",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".cfg",
    ".ini",
    ".sh",
    ".rb",
    ".go",
    ".rs",
}
IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}


def _scan_secrets(path: Path) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for root, dirs, files in os.walk(path):
        if any(p in IGNORE_DIRS for p in Path(root).parts):
            dirs.clear()
            continue
        for f in files:
            fpath = Path(root) / f
            if fpath.suffix in SECRET_FILE_EXTS or f == ".env":
                try:
                    content = fpath.read_text(errors="ignore")
                    for pattern, name in SECRET_PATTERNS:
                        if re.search(pattern, content):
                            findings.append((str(fpath.relative_to(path)), name))
                except Exception:
                    pass
    return findings


def check_security(repo_path: str) -> CheckResult:
    path = Path(repo_path)
    secrets = _scan_secrets(path)
    has_dependabot = (path / ".github" / "dependabot.yml").exists()
    has_codeowners = False
    for p in [path / ".github" / "CODEOWNERS", path / "CODEOWNERS"]:
        if p.exists():
            has_codeowners = True
            break
    has_security_policy = (path / "SECURITY.md").exists() or (path / ".github" / "SECURITY.md").exists()

    details = [
        f"Secrets found: {len(secrets)}",
        f"Dependabot: {'yes' if has_dependabot else 'no'}",
        f"CODEOWNERS: {'yes' if has_codeowners else 'no'}",
        f"Security policy: {'yes' if has_security_policy else 'no'}",
    ]

    if secrets:
        for fpath, sname in secrets[:5]:
            details.append(f"  {sname} in {fpath}")
        return CheckResult(
            name="Security",
            status=CheckStatus.FAIL,
            message=f"CRITICAL: {len(secrets)} potential secret(s) found in repository",
            details=details,
            recommendations=[
                "Remove hardcoded secrets immediately",
                "Use environment variables or secret managers instead",
                "Rotate any exposed credentials",
            ],
            rsqkit_url="https://everse.software/RSQKit/research_software_security",
            category="security",
        )

    score = sum([has_dependabot, has_codeowners, has_security_policy])
    if score >= 2:
        status = CheckStatus.PASS
        msg = "Good security practices"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = "Partial security configuration"
    else:
        status = CheckStatus.WARN
        msg = "No security tools or policies found"

    recs = []
    if not has_dependabot:
        recs.append("Add Dependabot for dependency vulnerability scanning")
    if not has_codeowners:
        recs.append("Add a CODEOWNERS file for review accountability")
    if not has_security_policy:
        recs.append("Add a SECURITY.md with vulnerability reporting instructions")

    return CheckResult(
        name="Security",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/research_software_security",
        category="security",
    )
