"""2D prioritization model: effort x impact for each check."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from everse_scan.models import CheckResult, CheckStatus, ScanResult


# Effort levels: 1 (low) -> 3 (high)
# Impact levels: 1 (low) -> 4 (critical)
@dataclass(frozen=True)
class Priority:
    effort: int          # 1=low, 2=medium, 3=high
    impact: int          # 1=low, 2=medium, 3=high, 4=critical
    category: str = ""   # fair, engineering, security, documentation


# Base priorities per check name (when the check is failing/warning)
_CHECK_PRIORITIES: dict[str, Priority] = {
    "README":                  Priority(effort=1, impact=3, category="documentation"),
    "LICENSE":                 Priority(effort=1, impact=3, category="fair"),
    "CITATION.cff":            Priority(effort=1, impact=3, category="fair"),
    "codemeta.json":           Priority(effort=2, impact=3, category="fair"),
    "Structure":               Priority(effort=2, impact=2, category="engineering"),
    "Version control":         Priority(effort=1, impact=3, category="engineering"),
    "Tests":                   Priority(effort=3, impact=3, category="engineering"),
    "Documentation":           Priority(effort=2, impact=2, category="documentation"),
    "CI/CD":                   Priority(effort=2, impact=3, category="engineering"),
    "Packaging":               Priority(effort=2, impact=2, category="engineering"),
    "Static analysis":         Priority(effort=1, impact=2, category="engineering"),
    "Security":                Priority(effort=2, impact=4, category="security"),
    "Reproducible environments": Priority(effort=2, impact=3, category="engineering"),
    "Code review":             Priority(effort=2, impact=2, category="engineering"),
    "Software identifiers":    Priority(effort=1, impact=2, category="fair"),
    "Releasing":               Priority(effort=2, impact=2, category="engineering"),
    "Readable code":           Priority(effort=1, impact=1, category="engineering"),
}

EFFORT_LABELS = {1: "Low", 2: "Medium", 3: "High"}
IMPACT_LABELS = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}

# Priority quadrants
QUICK_WIN = "quick_win"       # low effort, high+ impact
CRITICAL_FIX = "critical"     # any effort, critical impact
STANDARD = "standard"          # medium effort, medium impact
LONG_TERM = "long_term"        # high effort, any impact
LOW_PRIORITY = "low_priority"  # low impact


def get_priority(check_name: str) -> Priority:
    return _CHECK_PRIORITIES.get(check_name, Priority(effort=2, impact=2))


def classify(check: CheckResult, tier: str = "", lifecycle: str = "", role: str = "") -> str:
    """Classify a failing/warning check into a priority quadrant.

    Factors:
    - Base effort x impact from the priority table
    - Tier adjustment: tier 1 (script) reduces engineering impact
    - Lifecycle adjustment: early stage boosts fair/documentation, published boosts engineering
    - Role adjustment: researcher boosts fair, rse boosts engineering
    """
    if check.status not in (CheckStatus.WARN, CheckStatus.FAIL):
        return ""

    base = get_priority(check.name)
    effort = base.effort
    impact = base.impact

    # Tier adjustments
    if tier == "script" and base.category == "engineering":
        impact = max(1, impact - 1)

    # Lifecycle adjustments
    if lifecycle == "early" and base.category in ("fair", "documentation"):
        impact = min(4, impact + 1)
    if lifecycle == "published" and base.category == "engineering":
        impact = min(4, impact + 1)

    # Role adjustments
    if role == "researcher" and base.category == "fair":
        impact = min(4, impact + 1)
    if role == "rse" and base.category == "engineering":
        impact = min(4, impact + 1)

    # Classify into quadrant
    if impact >= 4:
        return CRITICAL_FIX
    if effort <= 1 and impact >= 3:
        return QUICK_WIN
    if effort >= 3:
        return LONG_TERM
    if impact <= 1:
        return LOW_PRIORITY
    return STANDARD


def prioritize_checks(
    checks: list[CheckResult],
    tier: str = "",
    lifecycle: str = "",
    role: str = "",
) -> list[tuple[CheckResult, str, Priority]]:
    """Return failing/warning checks sorted by priority (impact desc, effort asc)."""
    prioritized: list[tuple[CheckResult, str, Priority]] = []
    for check in checks:
        if check.status not in (CheckStatus.WARN, CheckStatus.FAIL):
            continue
        quadrant = classify(check, tier, lifecycle, role)
        base = get_priority(check.name)
        # Adjusted impact for sorting
        adj_impact = base.impact
        if tier == "script" and base.category == "engineering":
            adj_impact = max(1, adj_impact - 1)
        if lifecycle == "early" and base.category in ("fair", "documentation"):
            adj_impact = min(4, adj_impact + 1)
        if lifecycle == "published" and base.category == "engineering":
            adj_impact = min(4, adj_impact + 1)
        if role == "researcher" and base.category == "fair":
            adj_impact = min(4, adj_impact + 1)
        if role == "rse" and base.category == "engineering":
            adj_impact = min(4, adj_impact + 1)
        prioritized.append((check, quadrant, Priority(effort=base.effort, impact=adj_impact, category=base.category)))

    prioritized.sort(key=lambda x: (-x[2].impact, x[2].effort))
    return prioritized


def priority_label(quadrant: str) -> str:
    labels = {
        QUICK_WIN: "Quick win",
        CRITICAL_FIX: "Critical",
        STANDARD: "Standard",
        LONG_TERM: "Long term",
        LOW_PRIORITY: "Low priority",
    }
    return labels.get(quadrant, quadrant)
