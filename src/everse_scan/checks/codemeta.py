"""Check: codemeta.json presence and validity."""

from __future__ import annotations

import json
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

REQUIRED_FIELDS = ["@context", "@type", "name", "author", "description", "license", "codeRepository"]
RECOMMENDED_FIELDS = ["programmingLanguage", "softwareVersion", "developmentStatus"]


def check_codemeta(repo_path: str) -> CheckResult:
    path = Path(repo_path)
    codemeta_file = path / "codemeta.json"

    if not codemeta_file.exists():
        return CheckResult(
            name="codemeta.json",
            status=CheckStatus.FAIL,
            message="No codemeta.json found",
            details=["codemeta.json not present at repository root"],
            recommendations=[
                "Create a codemeta.json with software metadata",
                "Can be generated from CITATION.cff and packaging files",
            ],
            rsqkit_url="https://everse.software/RSQKit/complete_software_metadata_codemeta",
            category="fair",
        )

    try:
        content = codemeta_file.read_text(errors="ignore")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return CheckResult(
            name="codemeta.json",
            status=CheckStatus.FAIL,
            message=f"codemeta.json is not valid JSON: {e}",
            details=[f"Parse error: {e}"],
            recommendations=["Fix JSON syntax errors in codemeta.json"],
            rsqkit_url="https://everse.software/RSQKit/complete_software_metadata_codemeta",
            category="fair",
        )

    missing_required = [f for f in REQUIRED_FIELDS if f not in data]
    missing_recommended = [f for f in RECOMMENDED_FIELDS if f not in data]

    details = []
    if missing_required:
        details.append(f"Missing required fields: {', '.join(missing_required)}")
    else:
        details.append("All required fields present")
    if missing_recommended:
        details.append(f"Missing recommended fields: {', '.join(missing_recommended)}")

    if not missing_required:
        status = CheckStatus.PASS if not missing_recommended else CheckStatus.WARN
        msg = "codemeta.json valid with all required fields"
        if missing_recommended:
            msg += f" (missing recommended: {', '.join(missing_recommended)})"
        return CheckResult(
            name="codemeta.json",
            status=status,
            message=msg,
            details=details,
            recommendations=[f"Consider adding: {', '.join(missing_recommended)}"] if missing_recommended else [],
            rsqkit_url="https://everse.software/RSQKit/complete_software_metadata_codemeta",
            category="fair",
        )

    return CheckResult(
        name="codemeta.json",
        status=CheckStatus.WARN,
        message=f"codemeta.json found but missing required fields: {', '.join(missing_required)}",
        details=details,
        recommendations=[f"Add missing required fields: {', '.join(missing_required)}"],
        rsqkit_url="https://everse.software/RSQKit/complete_software_metadata_codemeta",
        category="fair",
    )
