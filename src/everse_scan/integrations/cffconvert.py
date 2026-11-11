"""cffconvert integration: validate CITATION.cff format.

If cffconvert is installed, use it. Otherwise, do basic YAML structure validation.
"""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

REQUIRED_CFF_FIELDS = ["cff-version", "title", "authors", "message"]
RECOMMENDED_CFF_FIELDS = ["version", "date-released", "license", "doi", "url"]


def check_cffconvert(repo_path: str) -> CheckResult:
    """Validate CITATION.cff using cffconvert or heuristic validation."""
    path = Path(repo_path)
    cff_path = path / "CITATION.cff"

    if not cff_path.exists():
        return CheckResult(
            name="CITATION.cff validation",
            status=CheckStatus.FAIL,
            message="No CITATION.cff found to validate",
            details=["CITATION.cff not found"],
            recommendations=["Create a CITATION.cff file"],
            rsqkit_url="https://github.com/citation-file-format/cffconvert",
            category="fair",
        )

    # Try cffconvert CLI
    try:
        import subprocess

        result = subprocess.run(
            ["cffconvert", "--validate", "-i", str(cff_path)],
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return CheckResult(
                name="CITATION.cff validation",
                status=CheckStatus.PASS,
                message="CITATION.cff is valid (cffconvert)",
                details=["cffconvert validation: PASS"],
                rsqkit_url="https://github.com/citation-file-format/cffconvert",
                category="fair",
            )
        else:
            return CheckResult(
                name="CITATION.cff validation",
                status=CheckStatus.FAIL,
                message=f"CITATION.cff validation failed (cffconvert): {result.stderr.strip()}",
                details=[f"cffconvert stderr: {result.stderr.strip()[:200]}"],
                recommendations=["Fix CITATION.cff errors reported by cffconvert"],
                rsqkit_url="https://github.com/citation-file-format/cffconvert",
                category="fair",
            )
    except FileNotFoundError:
        pass

    # Fallback: heuristic YAML validation
    return _heuristic_validate(cff_path)


def _heuristic_validate(cff_path: Path) -> CheckResult:
    """Basic validation of CITATION.cff structure."""
    content = cff_path.read_text(errors="ignore")
    lines = content.splitlines()

    # Check for required fields
    found_fields: dict[str, bool] = {}
    for field in REQUIRED_CFF_FIELDS + RECOMMENDED_CFF_FIELDS:
        for line in lines:
            if line.strip().startswith(f"{field}:") or f"{field}:" in line.split("#")[0]:
                found_fields[field] = True
                break

    missing_required = [f for f in REQUIRED_CFF_FIELDS if not found_fields.get(f)]
    missing_recommended = [f for f in RECOMMENDED_CFF_FIELDS if not found_fields.get(f)]

    details: list[str] = []
    details.append(
        f"Required fields present: {sum(1 for f in REQUIRED_CFF_FIELDS if found_fields.get(f))}/{len(REQUIRED_CFF_FIELDS)}"
    )
    details.append(
        f"Recommended fields present: {sum(1 for f in RECOMMENDED_CFF_FIELDS if found_fields.get(f))}/{len(RECOMMENDED_CFF_FIELDS)}"
    )
    if missing_required:
        details.append(f"Missing required: {', '.join(missing_required)}")
    if missing_recommended:
        details.append(f"Missing recommended: {', '.join(missing_recommended)}")

    if missing_required:
        return CheckResult(
            name="CITATION.cff validation",
            status=CheckStatus.WARN,
            message=f"CITATION.cff has missing required fields: {', '.join(missing_required)}",
            details=details,
            recommendations=[f"Add missing required field: {f}" for f in missing_required],
            rsqkit_url="https://github.com/citation-file-format/cffconvert",
            category="fair",
        )

    if missing_recommended:
        return CheckResult(
            name="CITATION.cff validation",
            status=CheckStatus.WARN,
            message=f"CITATION.cff is valid but missing recommended fields: {', '.join(missing_recommended)}",
            details=details,
            recommendations=[f"Consider adding: {f}" for f in missing_recommended],
            rsqkit_url="https://github.com/citation-file-format/cffconvert",
            category="fair",
        )

    return CheckResult(
        name="CITATION.cff validation",
        status=CheckStatus.PASS,
        message="CITATION.cff has all required and recommended fields",
        details=details,
        rsqkit_url="https://github.com/citation-file-format/cffconvert",
        category="fair",
    )
