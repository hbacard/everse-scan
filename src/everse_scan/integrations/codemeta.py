"""codemeta validator: validate codemeta.json structure.

Validates against the codemeta schema requirements using stdlib JSON parsing.
"""

from __future__ import annotations

import json
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

REQUIRED_CODEMETA_FIELDS = ["@context", "@type", "name", "author", "license"]
RECOMMENDED_CODEMETA_FIELDS = ["version", "url", "identifier", "description", "codeRepository", "dateCreated"]


def check_codemeta_validation(repo_path: str) -> CheckResult:
    """Validate codemeta.json structure."""
    path = Path(repo_path)
    cm_path = path / "codemeta.json"

    if not cm_path.exists():
        return CheckResult(
            name="codemeta.json validation",
            status=CheckStatus.FAIL,
            message="No codemeta.json found to validate",
            details=["codemeta.json not found"],
            recommendations=["Create a codemeta.json file"],
            rsqkit_url="https://codemeta.github.io/",
            category="fair",
        )

    try:
        data = json.loads(cm_path.read_text())
    except json.JSONDecodeError as e:
        return CheckResult(
            name="codemeta.json validation",
            status=CheckStatus.FAIL,
            message=f"codemeta.json is not valid JSON: {e}",
            details=[f"JSON parse error: {e}"],
            recommendations=["Fix JSON syntax errors in codemeta.json"],
            rsqkit_url="https://codemeta.github.io/",
            category="fair",
        )

    missing_required = [f for f in REQUIRED_CODEMETA_FIELDS if f not in data]
    missing_recommended = [f for f in RECOMMENDED_CODEMETA_FIELDS if f not in data]

    details: list[str] = []
    details.append(
        f"Required fields present: {sum(1 for f in REQUIRED_CODEMETA_FIELDS if f in data)}/{len(REQUIRED_CODEMETA_FIELDS)}"
    )
    details.append(
        f"Recommended fields present: {sum(1 for f in RECOMMENDED_CODEMETA_FIELDS if f in data)}/{len(RECOMMENDED_CODEMETA_FIELDS)}"
    )
    if missing_required:
        details.append(f"Missing required: {', '.join(missing_required)}")
    if missing_recommended:
        details.append(f"Missing recommended: {', '.join(missing_recommended)}")

    if missing_required:
        return CheckResult(
            name="codemeta.json validation",
            status=CheckStatus.WARN,
            message=f"codemeta.json missing required fields: {', '.join(missing_required)}",
            details=details,
            recommendations=[f"Add missing field: {f}" for f in missing_required],
            rsqkit_url="https://codemeta.github.io/",
            category="fair",
        )

    if missing_recommended:
        return CheckResult(
            name="codemeta.json validation",
            status=CheckStatus.WARN,
            message=f"codemeta.json valid but missing recommended fields: {', '.join(missing_recommended)}",
            details=details,
            recommendations=[f"Consider adding: {f}" for f in missing_recommended],
            rsqkit_url="https://codemeta.github.io/",
            category="fair",
        )

    return CheckResult(
        name="codemeta.json validation",
        status=CheckStatus.PASS,
        message="codemeta.json has all required and recommended fields",
        details=details,
        rsqkit_url="https://codemeta.github.io/",
        category="fair",
    )
