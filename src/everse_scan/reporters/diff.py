"""Diff reporter: compare current scan with a baseline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from everse_scan.models import CheckStatus, ScanResult
from everse_scan.reporters.markdown import STATUS_ICONS


@dataclass
class DiffResult:
    baseline_passed: int
    current_passed: int
    baseline_total: int
    current_total: int
    improvements: list[tuple[str, CheckStatus, CheckStatus]]  # name, old_status, new_status
    regressions: list[tuple[str, CheckStatus, CheckStatus]]
    unchanged_failures: list[str]
    newly_na: list[str]

    @property
    def delta(self) -> int:
        return self.current_passed - self.baseline_passed

    @property
    def improved(self) -> bool:
        return self.delta > 0

    @property
    def regressed(self) -> bool:
        return len(self.regressions) > 0


def load_baseline(path: str) -> dict:
    """Load a baseline JSON scan result from file."""
    return json.loads(Path(path).read_text())


def compute_diff(baseline: dict, current: ScanResult) -> DiffResult:
    """Compute the diff between a baseline scan dict and current ScanResult."""
    baseline_checks: dict[str, str] = {}
    for c in baseline.get("checks", []):
        baseline_checks[c["name"]] = c["status"]

    current_checks: dict[str, CheckStatus] = {c.name: c.status for c in current.checks}

    improvements: list[tuple[str, CheckStatus, CheckStatus]] = []
    regressions: list[tuple[str, CheckStatus, CheckStatus]] = []
    unchanged_failures: list[str] = []
    newly_na: list[str] = []

    status_order = {CheckStatus.FAIL: 0, CheckStatus.WARN: 1, CheckStatus.NA: 2, CheckStatus.PASS: 3}
    status_map = {"pass": CheckStatus.PASS, "warn": CheckStatus.WARN, "fail": CheckStatus.FAIL, "na": CheckStatus.NA}

    all_names = set(baseline_checks.keys()) | set(current_checks.keys())
    for name in all_names:
        old_str = baseline_checks.get(name)
        new = current_checks.get(name)

        if old_str is None or new is None:
            continue

        old = status_map.get(old_str, CheckStatus.NA)

        if old == new:
            if new in (CheckStatus.FAIL, CheckStatus.WARN):
                unchanged_failures.append(name)
            continue

        if new == CheckStatus.NA and old != CheckStatus.NA:
            newly_na.append(name)
            continue

        old_rank = status_order.get(old, 0)
        new_rank = status_order.get(new, 0)

        if new_rank > old_rank:
            improvements.append((name, old, new))
        elif new_rank < old_rank:
            regressions.append((name, old, new))

    return DiffResult(
        baseline_passed=baseline.get("summary", {}).get("passed", 0),
        current_passed=current.passed,
        baseline_total=baseline.get("summary", {}).get("total", 0),
        current_total=current.total,
        improvements=improvements,
        regressions=regressions,
        unchanged_failures=unchanged_failures,
        newly_na=newly_na,
    )


def generate_diff_markdown(baseline: dict, current: ScanResult) -> str:
    """Generate a Markdown diff report comparing baseline to current scan."""
    diff = compute_diff(baseline, current)
    lines: list[str] = []

    lines.append("# EVERSE Scan — Progress Report")
    lines.append("")
    lines.append(f"**Repository**: {current.repo_name}")
    lines.append(f"**Current date**: {current.date}")
    baseline_date = baseline.get("date", "unknown")
    lines.append(f"**Baseline date**: {baseline_date}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Score delta
    lines.append("## Score")
    lines.append("")
    if diff.delta > 0:
        lines.append(
            f"### {diff.current_passed}/{diff.current_total} (was {diff.baseline_passed}/{diff.baseline_total})"
        )
        lines.append("")
        lines.append(f"**+{diff.delta} improvement(s)**")
    elif diff.delta < 0:
        lines.append(
            f"### {diff.current_passed}/{diff.current_total} (was {diff.baseline_passed}/{diff.baseline_total})"
        )
        lines.append("")
        lines.append(f"**{diff.delta} regression(s)**")
    else:
        lines.append(
            f"### {diff.current_passed}/{diff.current_total} (was {diff.baseline_passed}/{diff.baseline_total})"
        )
        lines.append("")
        lines.append("**No score change** (but individual checks may have improved/regressed)")
    lines.append("")

    # Improvements
    lines.append("## Improvements")
    lines.append("")
    if diff.improvements:
        for name, old, new in diff.improvements:
            lines.append(f"- **{name}**: {STATUS_ICONS[old]} -> {STATUS_ICONS[new]}")
    else:
        lines.append("- None")
    lines.append("")

    # Regressions
    lines.append("## Regressions")
    lines.append("")
    if diff.regressions:
        for name, old, new in diff.regressions:
            lines.append(f"- **{name}**: {STATUS_ICONS[old]} -> {STATUS_ICONS[new]}")
    else:
        lines.append("- None")
    lines.append("")

    # Unchanged failures
    if diff.unchanged_failures:
        lines.append("## Still failing")
        lines.append("")
        for name in diff.unchanged_failures:
            check = next((c for c in current.checks if c.name == name), None)
            if check:
                rec = check.recommendations[0] if check.recommendations else check.message
                lines.append(f"- **{name}**: {rec}")
        lines.append("")

    # Next steps
    lines.append("## Recommended next steps")
    lines.append("")
    from everse_scan.priorities import (
        EFFORT_LABELS,
        IMPACT_LABELS,
        prioritize_checks,
        priority_label,
    )

    prioritized = prioritize_checks(
        [c for c in current.checks if c.name in diff.unchanged_failures],
        current.tier,
        current.lifecycle,
    )
    if prioritized:
        for c, q, p in prioritized[:5]:
            rec = c.recommendations[0] if c.recommendations else c.message
            lines.append(f"1. **{c.name}** ({priority_label(q)}): {rec}")
            lines.append(f"   - Effort: {EFFORT_LABELS[p.effort]} | Impact: {IMPACT_LABELS[p.impact]}")
    else:
        lines.append("- All previously failing checks are now resolved!")
    lines.append("")

    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def save_baseline(result: ScanResult, path: str) -> None:
    """Save a scan result as a baseline JSON file."""
    Path(path).write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
