"""Funder compliance reporter: checks repo against funder requirements."""

from __future__ import annotations

from typing import Optional

from everse_scan.models import CheckResult, CheckStatus, ScanResult
from everse_scan.context.funder import FunderResult
from everse_scan.knowledge.funders import FunderProfile, get_funder_profile


def generate_funder_section(result: ScanResult, funder: FunderResult) -> str:
    """Generate a funder compliance section for the report."""
    lines: list[str] = []

    lines.append("## Funder Compliance")
    lines.append("")

    if not funder.detected:
        lines.append("No funder detected in repository metadata.")
        lines.append("")
        lines.append("If your project is funded by a research grant (Horizon Europe, NSF, Wellcome, etc.),")
        lines.append("add funder information to `.zenodo.json`, `CITATION.cff`, or `README.md` to enable")
        lines.append("funder-specific compliance checking.")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"**Detected funder**: {funder.funder_label}")
    lines.append(f"**Detection confidence**: {funder.confidence}")
    if funder.grant_ids:
        lines.append(f"**Grant IDs**: {', '.join(funder.grant_ids)}")
    if funder.detection_sources:
        lines.append(f"**Detection sources**: {', '.join(funder.detection_sources)}")
    lines.append("")

    profile = get_funder_profile(funder.funder)
    if not profile:
        lines.append(f"No specific compliance profile available for {funder.funder_label}.")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"### Requirements for {profile.label}")
    lines.append("")

    # Cross-reference requirements with scan results
    checks_by_name = {c.name: c for c in result.checks}

    lines.append("| # | Requirement | Related check | Status | Mandatory |")
    lines.append("|---|-------------|---------------|--------|-----------|")

    met = 0
    total_req = 0
    missing: list[str] = []
    partial: list[str] = []

    for i, req in enumerate(profile.requirements, 1):
        total_req += 1
        check = checks_by_name.get(req.related_check)
        if check:
            if check.status == CheckStatus.PASS:
                status_icon = "PASS"
                met += 1
            elif check.status == CheckStatus.WARN:
                status_icon = "WARN"
                partial.append(req.description)
            elif check.status == CheckStatus.FAIL:
                status_icon = "FAIL"
                missing.append(req.description)
            else:
                status_icon = "N/A"
        else:
            status_icon = "Not checked"

        mandatory = "Yes" if req.mandatory else "No"
        lines.append(f"| {i} | {req.description} | {req.related_check} | {status_icon} | {mandatory} |")

    lines.append("")

    # Summary
    pct = round(met / total_req * 100) if total_req else 0
    lines.append(f"**Compliance**: {met}/{total_req} ({pct}%) requirements met")
    lines.append("")

    # Missing mandatory requirements
    mandatory_missing = [
        req.description for req in profile.requirements
        if req.mandatory
        and (checks_by_name.get(req.related_check) and
             checks_by_name[req.related_check].status in (CheckStatus.FAIL, CheckStatus.WARN))
    ]
    if mandatory_missing:
        lines.append("### Missing mandatory requirements")
        lines.append("")
        for m in mandatory_missing:
            lines.append(f"- {m}")
        lines.append("")

    if partial:
        lines.append("### Partially met requirements")
        lines.append("")
        for p in partial:
            lines.append(f"- {p}")
        lines.append("")

    if not missing and not partial:
        lines.append("All funder requirements are met.")
        lines.append("")

    return "\n".join(lines)
