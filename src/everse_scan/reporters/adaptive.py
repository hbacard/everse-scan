"""Adaptive reporter: generates role-specific reports.

Roles:
- researcher: plain language, credit/citation first, quick wins focus
- rse: technical, engineering first, full details
- default: same as M3 markdown (balanced)
"""

from __future__ import annotations

from everse_scan.models import CheckResult, CheckStatus, ScanResult
from everse_scan.reporters.markdown import (
    generate_markdown,
    STATUS_ICONS,
    _tier_label,
    _lifecycle_label,
    _ai_guidance,
)
from everse_scan.priorities import (
    prioritize_checks,
    priority_label,
    EFFORT_LABELS,
    IMPACT_LABELS,
    QUICK_WIN,
    CRITICAL_FIX,
    STANDARD,
    LONG_TERM,
    LOW_PRIORITY,
)

ROLES = ("default", "researcher", "rse")


def generate_adaptive_markdown(result: ScanResult, role: str = "default") -> str:
    """Generate a role-adaptive Markdown report."""
    if role == "default":
        return generate_markdown(result)
    if role == "researcher":
        return _researcher_report(result)
    if role == "rse":
        return _rse_report(result)
    return generate_markdown(result)


def _researcher_report(result: ScanResult) -> str:
    """Researcher-focused report: plain language, citation/credit first."""
    lines: list[str] = []

    lines.append("# EVERSE Scan Report (Researcher View)")
    lines.append("")
    lines.append(f"**Repository**: {result.repo_name}")
    lines.append(f"**Date**: {result.date}")
    langs = ", ".join(result.languages) if result.languages else "Unknown"
    lines.append(f"**Language(s)**: {langs}")
    lines.append(f"**Software type**: {_tier_label(result.tier)}")
    lines.append(f"**Development stage**: {_lifecycle_label(result.lifecycle)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive summary in plain language
    lines.append("## Summary")
    lines.append("")
    total = result.total
    pct = round(result.passed / total * 100) if total else 0
    lines.append(
        f"Your project passes **{result.passed}/{total}** ({pct}%) "
        f"of the quality checks."
    )
    lines.append("")

    # Citation & credit section first (researcher priority)
    lines.append("## Making your software citable")
    lines.append("")
    lines.append(
        "If others use your software in their research, they need to cite it properly. "
        "Here is what you should set up:"
    )
    lines.append("")

    citation_checks = [c for c in result.checks if c.name in ("CITATION.cff", "codemeta.json", "Software identifiers", "LICENSE")]
    for c in citation_checks:
        icon = STATUS_ICONS[c.status]
        lines.append(f"- **{c.name}**: {icon}")
        if c.status != CheckStatus.PASS and c.recommendations:
            for rec in c.recommendations:
                lines.append(f"  - {rec}")
        if c.rsqkit_url:
            lines.append(f"  - [RSQKit guide]({c.rsqkit_url})")
    lines.append("")

    # Quick wins
    lines.append("## Quick wins (easy to fix, high impact)")
    lines.append("")
    prioritized = prioritize_checks(result.checks, result.tier, result.lifecycle, "researcher")
    quick_wins = [(c, q, p) for c, q, p in prioritized if q in (QUICK_WIN, CRITICAL_FIX)]
    if quick_wins:
        for c, q, p in quick_wins:
            rec = c.recommendations[0] if c.recommendations else c.message
            lines.append(f"1. **{c.name}**: {rec}")
            lines.append(f"   - Effort: {EFFORT_LABELS[p.effort]} | Impact: {IMPACT_LABELS[p.impact]}")
            if c.rsqkit_url:
                lines.append(f"   - [Guide]({c.rsqkit_url})")
    else:
        lines.append("No quick wins needed -- great job!")
    lines.append("")

    # Other improvements (plain language)
    others = [(c, q, p) for c, q, p in prioritized if q not in (QUICK_WIN, CRITICAL_FIX)]
    if others:
        lines.append("## Other improvements to consider")
        lines.append("")
        for c, q, p in others:
            rec = c.recommendations[0] if c.recommendations else c.message
            lines.append(f"- **{c.name}** ({priority_label(q)}): {rec}")
        lines.append("")

    # Overall status table
    lines.append("## Full checklist")
    lines.append("")
    lines.append("| Check | Status |")
    lines.append("|-------|--------|")
    for c in result.checks:
        lines.append(f"| {c.name} | {STATUS_ICONS[c.status]} |")
    lines.append("")

    # AI note
    if result.ai_intensity > 0:
        lines.append("## AI usage")
        lines.append("")
        lines.append(f"This repository shows some AI usage indicators (level {result.ai_intensity}/10).")
        lines.append("This is fine -- just make sure a human reviews AI-generated code before publishing.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*This report is tailored for researchers. For a technical/engineering view, use `--role rse`.*")
    lines.append("")

    return "\n".join(lines)


def _rse_report(result: ScanResult) -> str:
    """RSE-focused report: technical, engineering first, concise."""
    lines: list[str] = []

    lines.append("# EVERSE Scan Report (RSE View)")
    lines.append("")
    lines.append(f"**Repository**: {result.repo_name}")
    lines.append(f"**Date**: {result.date}")
    langs = ", ".join(result.languages) if result.languages else "Unknown"
    lines.append(f"**Language(s)**: {langs}")
    lines.append(f"**Tier**: {_tier_label(result.tier)}")
    lines.append(f"**Lifecycle**: {_lifecycle_label(result.lifecycle)}")
    lines.append(f"**AI Intensity**: {result.ai_intensity}/10")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Score
    lines.append("## Score")
    lines.append("")
    lines.append(f"**{result.passed}/{result.total}** passed, {result.warned} warned, {result.failed} failed")
    lines.append("")

    # Engineering checks first
    eng_checks = [c for c in result.checks if c.name in (
        "Tests", "CI/CD", "Packaging", "Static analysis", "Code review",
        "Reproducible environments", "Version control", "Structure",
        "Releasing", "Readable code",
    )]
    lines.append("## Engineering checks")
    lines.append("")
    lines.append("| Check | Status | Details |")
    lines.append("|-------|--------|---------|")
    for c in eng_checks:
        detail = c.details[0] if c.details else c.message
        lines.append(f"| {c.name} | {STATUS_ICONS[c.status]} | {detail} |")
    lines.append("")

    # Prioritized action items
    lines.append("## Prioritized action items")
    lines.append("")
    prioritized = prioritize_checks(result.checks, result.tier, result.lifecycle, "rse")
    if prioritized:
        lines.append("| # | Check | Priority | Effort | Impact | Action |")
        lines.append("|---|-------|----------|--------|--------|--------|")
        for i, (c, q, p) in enumerate(prioritized, 1):
            action = c.recommendations[0] if c.recommendations else c.message
            lines.append(f"| {i} | {c.name} | {priority_label(q)} | {EFFORT_LABELS[p.effort]} | {IMPACT_LABELS[p.impact]} | {action} |")
    else:
        lines.append("All checks passing.")
    lines.append("")

    # FAIR/metadata checks
    fair_checks = [c for c in result.checks if c.name in (
        "README", "LICENSE", "CITATION.cff", "codemeta.json",
        "Software identifiers", "Documentation", "Security",
    )]
    lines.append("## FAIR & metadata checks")
    lines.append("")
    lines.append("| Check | Status | Details |")
    lines.append("|-------|--------|---------|")
    for c in fair_checks:
        detail = c.details[0] if c.details else c.message
        lines.append(f"| {c.name} | {STATUS_ICONS[c.status]} | {detail} |")
    lines.append("")

    # Quality dimensions
    from everse_scan.reporters.markdown import _quality_dimensions
    dims = _quality_dimensions(result)
    lines.append("## Quality dimensions")
    lines.append("")
    lines.append("| Dimension | Score | Checks |")
    lines.append("|-----------|-------|--------|")
    for name, score, checks_list in dims:
        lines.append(f"| {name} | {score} | {checks_list} |")
    lines.append("")

    # AI guidance
    lines.append("## AI assessment")
    lines.append("")
    lines.append(f"Level: {result.ai_intensity}/10")
    lines.append("")
    if result.ai_indicators:
        for ind in result.ai_indicators:
            lines.append(f"- {ind}")
    else:
        lines.append("- No AI indicators found")
    lines.append("")
    lines.append(_ai_guidance(result.ai_intensity))
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*This report is tailored for RSEs. For a researcher-friendly view, use `--role researcher`.*")
    lines.append("")

    return "\n".join(lines)
