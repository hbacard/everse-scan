"""Markdown reporter for everse-scan."""

from __future__ import annotations

from everse_scan.models import CheckResult, CheckStatus, ScanResult

STATUS_ICONS = {
    CheckStatus.PASS: "✅ Pass",
    CheckStatus.WARN: "⚠️ Warn",
    CheckStatus.FAIL: "❌ Fail",
    CheckStatus.NA: "⬜ N/A",
}

# Tasks not covered by the scan
UNCOVERED_TASKS = [
    ("Archiving software", "https://everse.software/RSQKit/archiving_software"),
    ("Future proofing", "https://everse.software/RSQKit/future_proofing"),
    ("Performance profiling", "https://everse.software/RSQKit/performance_profiling_and_optimization"),
    ("Environmental sustainability", "https://everse.software/RSQKit/improving_environmental_sustainability"),
    ("Computational workflows", "https://everse.software/RSQKit/computational_workflows"),
]

# All evaluated tasks (for the disclosure section)
EVALUATED_TASKS = [
    ("README", "https://everse.software/RSQKit/creating_good_readme"),
    ("Licensing", "https://everse.software/RSQKit/licensing_software"),
    ("Citation", "https://everse.software/RSQKit/citing_software"),
    ("Codemeta", "https://everse.software/RSQKit/complete_software_metadata_codemeta"),
    ("Project structure", "https://everse.software/RSQKit/software_project_structure"),
    ("Version control", "https://everse.software/RSQKit/using_version_control"),
    ("Testing", "https://everse.software/RSQKit/testing_software"),
    ("Documentation", "https://everse.software/RSQKit/software_documentation"),
    ("CI/CD", "https://everse.software/RSQKit/ci_cd"),
    ("Packaging", "https://everse.software/RSQKit/packaging_software"),
    ("Static analysis", "https://everse.software/RSQKit/static_analysis"),
    ("Security", "https://everse.software/RSQKit/research_software_security"),
    ("Reproducible environments", "https://everse.software/RSQKit/reproducible_software_environments"),
    ("Code review", "https://everse.software/RSQKit/code_review"),
    ("Software identifiers", "https://everse.software/RSQKit/software_identifiers"),
    ("Releasing", "https://everse.software/RSQKit/releasing_software"),
    ("Readable code", "https://everse.software/RSQKit/writing_readable_code"),
]


def _quality_dimensions(result: ScanResult) -> list[tuple[str, str, str]]:
    """Calculate quality dimension scores."""
    checks_by_name = {c.name: c for c in result.checks}

    def dim_status(check_names: list[str]) -> str:
        statuses = [checks_by_name.get(n).status for n in check_names if checks_by_name.get(n)]
        if not statuses:
            return "❌"
        if all(s == CheckStatus.PASS for s in statuses):
            return "✅"
        if any(s == CheckStatus.FAIL for s in statuses):
            return "❌"
        return "⚠️"

    return [
        ("Reproducibility", dim_status(["Packaging", "Tests", "CI/CD"]), "Packaging, Tests, CI/CD"),
        ("Maintainability", dim_status(["Structure", "Documentation", "Readable code"]), "Structure, Documentation, Readable code"),
        ("Findability", dim_status(["CITATION.cff", "codemeta.json", "Software identifiers"]), "CITATION.cff, codemeta.json, Software identifiers"),
        ("Trustworthiness", dim_status(["Tests", "CI/CD", "Version control", "Security"]), "Tests, CI/CD, Version control, Security"),
        ("Reusability", dim_status(["LICENSE", "README", "Documentation"]), "LICENSE, README, Documentation"),
    ]


def _tier_label(tier: str) -> str:
    labels = {"script": "Script (tier 1)", "tool": "Tool/Library (tier 2)", "infrastructure": "Infrastructure (tier 3)"}
    return labels.get(tier, tier)


def _lifecycle_label(stage: str) -> str:
    labels = {"early": "Early", "active_dev": "Active dev", "maintenance": "Maintenance", "published": "Published"}
    return labels.get(stage, stage)


def _ai_guidance(level: int) -> str:
    if level == 0:
        return ("No AI usage detected. This is perfectly valid. If you are considering AI, "
                "start with level 1 (conversational) for occasional tasks. "
                "See [Conversational Interaction](https://everse.software/RSQKit/conversational_interaction).")
    if level <= 3:
        return ("Conversational AI usage detected. Good starting point. **Risks**: no traceability of generated code, "
                "no repository context. **Quality**: document your prompts, commit separately. "
                "See [Cross Cutting Practices](https://everse.software/RSQKit/cross_cutting_practices).")
    if level <= 6:
        return ("IDE/repo-aware assistant detected. **Risks**: over-reliance on repository context, "
                "API hallucinations. **Quality**: add guardrails to rules, "
                "maintain tests as a safety net. "
                "See [Repository-aware assistance](https://everse.software/RSQKit/repository_aware_assistance).")
    if level <= 9:
        return ("CI/PR agents detected. **Risks**: high blast radius, automated changes without review. "
                "**Quality**: require mandatory human review, limit bot permissions, "
                "add non-regression tests. "
                "See [CI/PR/repository agents](https://everse.software/RSQKit/ci_pr_repository_agents).")
    return ("Autonomous agents detected. **Maximum risk**: consequences hard to predict, "
            "high volume of changes. **Quality**: strict guardrails required — "
            "exhaustive tests, automatic rollback, monitoring. "
            "See [Open-ended autonomous agents](https://everse.software/RSQKit/open_ended_autonomous_agents).")


def generate_markdown(result: ScanResult) -> str:
    """Generate a Markdown report from scan results."""
    lines: list[str] = []

    # Header
    lines.append("# EVERSE Scan Report")
    lines.append("")
    lines.append(f"**Repository**: {result.repo_name}")
    lines.append(f"**Date**: {result.date}")
    langs = ", ".join(result.languages) if result.languages else "Unknown"
    lines.append(f"**Language(s) detected**: {langs}")
    lines.append(f"**Software tier**: {_tier_label(result.tier)}")
    lines.append(f"**Lifecycle stage**: {_lifecycle_label(result.lifecycle)}")
    lines.append(f"**AI Intensity**: {result.ai_intensity} / 10")
    if result.funder:
        lines.append(f"**Funder**: {result.funder_label} (confidence: {result.funder_confidence})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Executive summary
    lines.append("## 1. Executive Summary")
    lines.append("")

    strong = [c for c in result.checks if c.status == CheckStatus.PASS]
    weak = [c for c in result.checks if c.status in (CheckStatus.WARN, CheckStatus.FAIL)]

    lines.append("### Strengths")
    if strong:
        for c in strong:
            lines.append(f"- **{c.name}**: {c.message}")
    else:
        lines.append("- No checks passed")
    lines.append("")

    lines.append("### Weaknesses")
    if weak:
        for c in weak:
            lines.append(f"- **{c.name}**: {c.message}")
    else:
        lines.append("- No weaknesses detected")
    lines.append("")

    # Conformity table
    lines.append("### Overall Compliance")
    lines.append("")
    lines.append("| Check | Status |")
    lines.append("|-------|--------|")
    for c in result.checks:
        lines.append(f"| {c.name} | {STATUS_ICONS[c.status]} |")
    lines.append("")

    # Quality dimensions
    lines.append("### Quality Dimensions (RSQKit mapping)")
    lines.append("")
    lines.append("> Source: https://everse.software/RSQKit/all_indicators")
    lines.append("")
    lines.append("| Dimension | Score | Checks involved |")
    lines.append("|---|---|---|")
    for dim_name, score, checks_list in _quality_dimensions(result):
        lines.append(f"| {dim_name} | {score} | {checks_list} |")
    lines.append("")

    # Tier
    lines.append("### Detected Software Tier")
    lines.append(f"**Tier**: {_tier_label(result.tier)}")
    lines.append(f"**Justification**: {result.tier_justification}")
    if result.tier_checks_adjusted:
        lines.append(f"**Adjusted checks**: {', '.join(result.tier_checks_adjusted)}")
    lines.append("")

    # Lifecycle
    lines.append("### Detected Lifecycle Stage")
    lines.append(f"**Stage**: {_lifecycle_label(result.lifecycle)}")
    lines.append(f"**Justification**: {result.lifecycle_justification}")
    lines.append("")

    # Disclosure
    lines.append("### Non-evaluated Tasks")
    lines.append("")
    lines.append(f"> ⚠️ This scan evaluates {result.total} of the 35+ RSQKit tasks. "
                 f"The following tasks are **not** evaluated:")
    lines.append(">")
    for name, url in UNCOVERED_TASKS:
        lines.append(f"> - [{name}]({url})")
    lines.append("> - ... (see [complete list](https://everse.software/RSQKit/tasks))")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 2. Action plan
    lines.append("## 2. Prioritized Action Plan")
    lines.append("")
    lines.append("> Prioritization by effort × impact. Impact factors in risk, tier, lifecycle, and target role.")
    lines.append("")

    critical = [c for c in result.checks if c.status == CheckStatus.FAIL and c.category == "security"]
    fails = [c for c in result.checks if c.status == CheckStatus.FAIL and c.category != "security"]
    warns = [c for c in result.checks if c.status == CheckStatus.WARN]

    lines.append("### Critical Risks (address first if detected)")
    if critical:
        for c in critical:
            lines.append(f"1. 🔴 {c.message} — **impact: critical** ({c.rsqkit_url})")
    else:
        lines.append("- No critical risks detected")
    lines.append("")

    lines.append("### Quick Wins (low effort, high impact)")
    quick_wins = [c for c in fails if c.category == "fair"]
    if quick_wins:
        for c in quick_wins:
            rec = c.recommendations[0] if c.recommendations else "Fix this issue"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url}) — **impact: high**")
    elif warns:
        for c in warns[:3]:
            rec = c.recommendations[0] if c.recommendations else "Improve this check"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url}) — **impact: moderate**")
    else:
        lines.append("- No quick wins needed")
    lines.append("")

    lines.append("### Medium Term (moderate effort, moderate impact)")
    remaining_warns = [c for c in warns if c not in (warns[:3] if not quick_wins else [])]
    if remaining_warns:
        for c in remaining_warns[:5]:
            rec = c.recommendations[0] if c.recommendations else "Improve this check"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url})")
    else:
        lines.append("- Nothing to report")
    lines.append("")

    lines.append("### Long Term (high effort, structural impact)")
    long_term = [c for c in fails if c.category != "fair"]
    if long_term:
        for c in long_term:
            rec = c.recommendations[0] if c.recommendations else "Fix this issue"
            lines.append(f"1. {rec} (cf. {c.rsqkit_url})")
    else:
        lines.append("- Nothing to report")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Funder compliance section (if funder detected)
    if result.funder:
        from everse_scan.reporters.funder import generate_funder_section
        from everse_scan.context.funder import FunderResult
        funder_result = FunderResult(
            funder=result.funder,
            funder_label=result.funder_label,
            grant_ids=result.funder_grant_ids,
            detection_sources=[],
            confidence=result.funder_confidence,
        )
        lines.append(generate_funder_section(result, funder_result))
        lines.append("---")
        lines.append("")

    # 3. Technical details
    lines.append("## 3. Technical Details by Task")
    lines.append("")
    for i, c in enumerate(result.checks, 1):
        lines.append(f"### 3.{i} {c.name}")
        lines.append(f"**Status**: {STATUS_ICONS[c.status]}")
        lines.append(f"**RSQKit**: {c.rsqkit_url}")
        lines.append("")
        lines.append("**Findings**:")
        for d in c.details:
            lines.append(f"- {d}")
        lines.append("")
        if c.recommendations:
            lines.append("**Recommendations**:")
            for r in c.recommendations:
                lines.append(f"- {r}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # 4. AI Spectrum
    lines.append("## 4. AI Spectrum Assessment")
    lines.append("")
    lines.append(f"**Estimated current position**: Level {result.ai_intensity} / 10")
    lines.append("")
    lines.append("**Analysis**:")
    if result.ai_indicators:
        for ind in result.ai_indicators:
            lines.append(f"- {ind}")
    else:
        lines.append("- No AI indicators found")
    lines.append("")
    lines.append("**Guidance**:")
    lines.append(_ai_guidance(result.ai_intensity))
    lines.append("")
    lines.append("**Cross-cutting practices** (applicable to all levels):")
    lines.append("- Always review AI-generated code before committing")
    lines.append("- Keep AI-generated code in separate commits for auditability")
    lines.append("- Document which AI tools are used and how")
    lines.append("- Maintain rollback capability (version control + tests)")
    lines.append("")
    lines.append("**RSQKit References**:")
    lines.append("- https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage")
    lines.append("- https://everse.software/RSQKit/cross_cutting_practices")
    lines.append("- https://everse.software/RSQKit/ai_intensity_considerations")
    lines.append("")

    return "\n".join(lines)
