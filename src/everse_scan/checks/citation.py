"""Check: CITATION.cff presence and validity."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

REQUIRED_FIELDS = ["title", "authors", "date-released", "version"]


def _parse_cff_fields(cff_file: Path) -> dict[str, str]:
    import yaml

    with open(cff_file, "r") as f_in:
        fields = yaml.safe_load(f_in)
    return fields


def check_citation(repo_path: str) -> CheckResult:
    path = Path(repo_path)
    cff_file = path / "CITATION.cff"

    if not cff_file.exists():
        return CheckResult(
            name="CITATION.cff",
            status=CheckStatus.FAIL,
            message="No CITATION.cff found",
            details=["CITATION.cff not present at repository root"],
            recommendations=[
                "Create a CITATION.cff to enable proper citation of your software",
                "Fields can be pre-filled from git log (authors) and README (title)",
            ],
            rsqkit_url="https://everse.software/RSQKit/citing_software",
            category="fair",
        )

    fields = _parse_cff_fields(cff_file=cff_file)

    missing = [f for f in REQUIRED_FIELDS if f not in fields or not fields[f]]
    present = [f for f in REQUIRED_FIELDS if fields.get(f)]

    details = [f"Found fields: {', '.join(present)}"] if present else ["No required fields found"]
    if missing:
        details.append(f"Missing required fields: {', '.join(missing)}")

    if not missing:
        return CheckResult(
            name="CITATION.cff",
            status=CheckStatus.PASS,
            message="CITATION.cff found with all required fields",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/citing_software",
            category="fair",
        )

    return CheckResult(
        name="CITATION.cff",
        status=CheckStatus.WARN,
        message=f"CITATION.cff found but missing fields: {', '.join(missing)}",
        details=details,
        recommendations=[f"Add missing fields: {', '.join(missing)}"],
        rsqkit_url="https://everse.software/RSQKit/citing_software",
        category="fair",
    )
