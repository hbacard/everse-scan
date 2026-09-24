"""Scanner orchestration for everse-scan."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from everse_scan.models import CheckResult, CheckStatus, ScanResult, AIIntensityProfile
from everse_scan.languages.detector import detect_languages, LanguageInfo
from everse_scan.context.tier import detect_tier, TierResult, TIER_SCRIPT
from everse_scan.context.lifecycle import detect_lifecycle, LifecycleResult
from everse_scan.context.funder import detect_funder, FunderResult
from everse_scan.checks.readme import check_readme
from everse_scan.checks.license import check_license
from everse_scan.checks.citation import check_citation
from everse_scan.checks.codemeta import check_codemeta
from everse_scan.checks.structure import check_structure
from everse_scan.checks.version_control import check_version_control
from everse_scan.checks.tests import check_tests
from everse_scan.checks.documentation import check_documentation
from everse_scan.checks.cicd import check_cicd
from everse_scan.checks.packaging import check_packaging
from everse_scan.checks.static_analysis import check_static_analysis
from everse_scan.checks.security import check_security
from everse_scan.checks.reproducible_envs import check_reproducible_envs
from everse_scan.checks.code_review import check_code_review
from everse_scan.checks.software_identifiers import check_software_identifiers
from everse_scan.checks.releasing import check_releasing
from everse_scan.checks.readable_code import check_readable_code
from everse_scan.checks.extended import (
    check_authorship,
    check_orcid,
    check_dependency_management,
    check_containers,
    check_workflow_files,
    check_api_docs,
    check_changelog,
    check_contribution_guide,
    check_code_of_conduct,
    check_issue_templates,
    check_secret_management,
    check_data_management,
    check_reproducibility_checklist,
    check_archiving,
    check_future_proofing,
    check_sustainability_plan,
    check_env_sustainability,
    check_software_peer_review,
    check_quality_model,
)


def _read_ai_intensity_profile(repo_path: str) -> AIIntensityProfile:
    """Read ai-intensity.yaml from the repository if present.

    This does NOT detect or infer AI usage from repository files.
    It only reads a self-determined profile created by the AI Intensity Q&A skill.
    """
    profile_path = Path(repo_path) / "ai-intensity.yaml"
    if not profile_path.exists():
        return AIIntensityProfile(found=False)

    try:
        import yaml
        with open(profile_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        intensity = data.get("intensity", {}) or {}
        determination = data.get("determination", {}) or {}
        declaration = data.get("declaration", {}) or {}

        return AIIntensityProfile(
            found=True,
            current=intensity.get("current"),
            desired=intensity.get("desired"),
            authorized=intensity.get("authorized"),
            sustainable=intensity.get("sustainable"),
            current_usage=determination.get("current_usage", ""),
            desired_intensity=determination.get("desired_intensity", ""),
            authorized_intensity=determination.get("authorized_intensity", ""),
            review_capacity=determination.get("review_capacity", ""),
            determined_by=declaration.get("determined_by", ""),
            date=declaration.get("date", ""),
        )
    except (ImportError, OSError, ValueError):
        return AIIntensityProfile(found=False)


def scan_repo(
    repo_path: str,
    use_integrations: bool = False,
) -> ScanResult:
    """Run the full scan on a repository.

    Args:
        repo_path: Path to the repository to scan.
        use_integrations: If True, run external tool integrations (howfairis, cffconvert, codemeta).
    """
    path = Path(repo_path).resolve()
    repo_name = path.name

    # Language detection
    lang_info: LanguageInfo = detect_languages(str(path))

    # Tier detection
    tier_result: TierResult = detect_tier(str(path))

    # Lifecycle detection
    lifecycle_result: LifecycleResult = detect_lifecycle(str(path))

    # AI intensity profile (read-only, no detection)
    ai_profile = _read_ai_intensity_profile(str(path))

    # Funder detection
    funder_result = detect_funder(str(path))

    # Run all 17 core checks + 18 extended checks = 35 total
    checks: list[CheckResult] = []
    lang = lang_info.primary

    # Core checks (M3)
    checks.append(check_readme(str(path)))
    checks.append(check_license(str(path)))
    checks.append(check_citation(str(path)))
    checks.append(check_codemeta(str(path)))
    checks.append(check_structure(str(path)))
    checks.append(check_version_control(str(path)))
    checks.append(check_tests(str(path), lang))
    checks.append(check_documentation(str(path), lang))
    checks.append(check_cicd(str(path)))
    checks.append(check_packaging(str(path), lang))
    checks.append(check_static_analysis(str(path), lang))
    checks.append(check_security(str(path)))
    checks.append(check_reproducible_envs(str(path), lang))
    checks.append(check_code_review(str(path)))
    checks.append(check_software_identifiers(str(path)))
    checks.append(check_releasing(str(path)))
    checks.append(check_readable_code(str(path), lang))

    # Extended checks (M5)
    checks.append(check_authorship(str(path)))
    checks.append(check_orcid(str(path)))
    checks.append(check_dependency_management(str(path)))
    checks.append(check_containers(str(path)))
    checks.append(check_workflow_files(str(path)))
    checks.append(check_api_docs(str(path)))
    checks.append(check_changelog(str(path)))
    checks.append(check_contribution_guide(str(path)))
    checks.append(check_code_of_conduct(str(path)))
    checks.append(check_issue_templates(str(path)))
    checks.append(check_secret_management(str(path)))
    checks.append(check_data_management(str(path)))
    checks.append(check_reproducibility_checklist(str(path)))
    checks.append(check_archiving(str(path)))
    checks.append(check_future_proofing(str(path)))
    checks.append(check_sustainability_plan(str(path)))
    checks.append(check_env_sustainability(str(path)))
    checks.append(check_software_peer_review(str(path)))
    checks.append(check_quality_model(str(path)))

    # Run integrations if requested
    if use_integrations:
        from everse_scan.integrations.howfairis import check_howfairis
        from everse_scan.integrations.cffconvert import check_cffconvert
        from everse_scan.integrations.codemeta import check_codemeta_validation

        checks.extend(check_howfairis(str(path)))
        checks.append(check_cffconvert(str(path)))
        checks.append(check_codemeta_validation(str(path)))

    # Adjust checks for tier 1 (script)
    if tier_result.is_script:
        na_checks = ("codemeta.json", "CI/CD", "Packaging", "API documentation",
                      "Computational workflows", "Software sustainability plan",
                      "Environmental sustainability", "Software peer review",
                      "Software quality model", "Containerization")
        for check in checks:
            if check.name in na_checks:
                check.status = CheckStatus.NA
                check.message = f"N/A for tier 1 (script): {check.message}"

    return ScanResult(
        repo_path=str(path),
        repo_name=repo_name,
        date=datetime.now().strftime("%Y-%m-%d"),
        languages=lang_info.languages,
        primary_language=lang_info.primary,
        tier=tier_result.tier,
        tier_justification=tier_result.justification,
        tier_checks_adjusted=tier_result.checks_adjusted,
        lifecycle=lifecycle_result.stage,
        lifecycle_justification=lifecycle_result.justification,
        ai_intensity_profile=ai_profile,
        funder=funder_result.funder,
        funder_label=funder_result.funder_label,
        funder_grant_ids=funder_result.grant_ids,
        funder_confidence=funder_result.confidence,
        checks=checks,
    )
