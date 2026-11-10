"""Tests for M4: adaptive reporter, diff, and prioritization."""

import pytest

from everse_scan.models import CheckResult, CheckStatus
from everse_scan.priorities import (
    CRITICAL_FIX,
    QUICK_WIN,
    STANDARD,
    classify,
    get_priority,
    prioritize_checks,
)
from everse_scan.reporters.adaptive import generate_adaptive_markdown
from everse_scan.reporters.diff import (
    compute_diff,
    generate_diff_markdown,
    load_baseline,
    save_baseline,
)
from everse_scan.scanner import scan_repo
from tests.fixtures import create_minimal_repo, create_sample_repo


@pytest.fixture
def sample_repo(tmp_path):
    return create_sample_repo(tmp_path)


@pytest.fixture
def minimal_repo(tmp_path):
    return create_minimal_repo(tmp_path)


class TestPrioritization:
    def test_get_priority_returns_values(self):
        p = get_priority("README")
        assert p.effort == 1
        assert p.impact == 3

    def test_get_priority_unknown_check(self):
        p = get_priority("Unknown check")
        assert p.effort == 2
        assert p.impact == 2

    def test_classify_fail_returns_quadrant(self):
        check = CheckResult(
            name="CITATION.cff",
            status=CheckStatus.FAIL,
            message="No CITATION.cff",
            category="fair",
        )
        quadrant = classify(check, tier="tool", lifecycle="early")
        assert quadrant in (QUICK_WIN, CRITICAL_FIX, STANDARD)

    def test_classify_pass_returns_empty(self):
        check = CheckResult(
            name="README",
            status=CheckStatus.PASS,
            message="OK",
            category="documentation",
        )
        assert classify(check) == ""

    def test_classify_security_is_critical(self):
        check = CheckResult(
            name="Security",
            status=CheckStatus.FAIL,
            message="No security",
            category="security",
        )
        assert classify(check) == CRITICAL_FIX

    def test_classify_script_tier_reduces_engineering(self):
        check = CheckResult(
            name="Tests",
            status=CheckStatus.FAIL,
            message="No tests",
            category="engineering",
        )
        q_script = classify(check, tier="script")
        # Script tier should not upgrade engineering to critical
        assert q_script != CRITICAL_FIX

    def test_prioritize_checks_sorts_by_impact(self):
        checks = [
            CheckResult(name="README", status=CheckStatus.WARN, message="low", category="documentation"),
            CheckResult(name="Security", status=CheckStatus.FAIL, message="critical", category="security"),
            CheckResult(name="CITATION.cff", status=CheckStatus.FAIL, message="fair", category="fair"),
        ]
        prioritized = prioritize_checks(checks)
        # Security (impact 4) should come first
        assert prioritized[0][0].name == "Security"

    def test_prioritize_skips_passing_checks(self):
        checks = [
            CheckResult(name="README", status=CheckStatus.PASS, message="ok"),
            CheckResult(name="Security", status=CheckStatus.FAIL, message="bad"),
        ]
        prioritized = prioritize_checks(checks)
        assert len(prioritized) == 1
        assert prioritized[0][0].name == "Security"

    def test_role_researcher_boosts_fair(self):
        check = CheckResult(
            name="CITATION.cff",
            status=CheckStatus.FAIL,
            message="missing",
            category="fair",
        )
        prioritized_default = prioritize_checks([check], role="default")
        prioritized_researcher = prioritize_checks([check], role="researcher")
        # Researcher should have higher impact for fair checks
        assert prioritized_researcher[0][2].impact >= prioritized_default[0][2].impact

    def test_role_rse_boosts_engineering(self):
        check = CheckResult(
            name="Tests",
            status=CheckStatus.FAIL,
            message="no tests",
            category="engineering",
        )
        prioritized_default = prioritize_checks([check], role="default")
        prioritized_rse = prioritize_checks([check], role="rse")
        assert prioritized_rse[0][2].impact >= prioritized_default[0][2].impact


class TestAdaptiveReporter:
    def test_default_role_matches_markdown(self, sample_repo):
        result = scan_repo(str(sample_repo))
        from everse_scan.reporters.markdown import generate_markdown

        default_output = generate_adaptive_markdown(result, "default")
        markdown_output = generate_markdown(result)
        assert default_output == markdown_output

    def test_researcher_report_has_citation_section(self, sample_repo):
        result = scan_repo(str(sample_repo))
        output = generate_adaptive_markdown(result, "researcher")
        assert "# EVERSE Scan Report (Researcher View)" in output
        assert "citable" in output.lower()

    def test_rse_report_has_engineering_section(self, sample_repo):
        result = scan_repo(str(sample_repo))
        output = generate_adaptive_markdown(result, "rse")
        assert "# EVERSE Scan Report (RSE View)" in output
        assert "Engineering checks" in output
        assert "Prioritized action items" in output

    def test_researcher_report_has_quick_wins(self, sample_repo):
        result = scan_repo(str(sample_repo))
        output = generate_adaptive_markdown(result, "researcher")
        assert "Quick wins" in output

    def test_rse_report_has_quality_dimensions(self, sample_repo):
        result = scan_repo(str(sample_repo))
        output = generate_adaptive_markdown(result, "rse")
        assert "Quality dimensions" in output

    def test_researcher_report_mentions_role_switch(self, sample_repo):
        result = scan_repo(str(sample_repo))
        output = generate_adaptive_markdown(result, "researcher")
        assert "--role rse" in output


class TestDiffReporter:
    def test_save_and_load_baseline(self, sample_repo, tmp_path):
        result = scan_repo(str(sample_repo))
        baseline_path = str(tmp_path / "baseline.json")
        save_baseline(result, baseline_path)

        loaded = load_baseline(baseline_path)
        assert loaded["repo_name"] == "sample-python"
        assert loaded["summary"]["total"] >= 17

    def test_compute_diff_no_change(self, sample_repo):
        result = scan_repo(str(sample_repo))
        baseline = result.to_dict()
        diff = compute_diff(baseline, result)
        assert diff.delta == 0
        assert len(diff.improvements) == 0
        assert len(diff.regressions) == 0

    def test_compute_diff_with_improvement(self, sample_repo):
        result = scan_repo(str(sample_repo))
        baseline = result.to_dict()

        # Simulate improvement: change a FAIL/WARN to PASS
        for check in baseline["checks"]:
            if check["status"] == "fail":
                check["status"] = "pass"
                break

        diff = compute_diff(baseline, result)
        # Current has fewer passes than baseline now (baseline was improved)
        # So current should have regressions
        assert len(diff.regressions) > 0

    def test_compute_diff_improvement_in_current(self, sample_repo):
        result = scan_repo(str(sample_repo))
        baseline = result.to_dict()

        # Modify current result to have one more PASS
        from everse_scan.models import CheckStatus

        for check in result.checks:
            if check.status == CheckStatus.WARN:
                check.status = CheckStatus.PASS
                break

        diff = compute_diff(baseline, result)
        assert len(diff.improvements) > 0
        assert diff.delta > 0

    def test_diff_markdown_has_progress_report(self, sample_repo):
        result = scan_repo(str(sample_repo))
        baseline = result.to_dict()
        md = generate_diff_markdown(baseline, result)
        assert "Progress Report" in md
        assert "was" in md

    def test_diff_markdown_shows_improvements_section(self, sample_repo):
        result = scan_repo(str(sample_repo))
        baseline = result.to_dict()
        md = generate_diff_markdown(baseline, result)
        assert "## Improvements" in md
        assert "## Regressions" in md

    def test_diff_with_simulated_baseline(self, sample_repo, tmp_path):
        """Full workflow: save baseline, make changes, re-scan, diff."""
        result = scan_repo(str(sample_repo))

        # Save baseline
        baseline_path = str(tmp_path / "baseline.json")
        save_baseline(result, baseline_path)

        # Simulate improvement in current
        from everse_scan.models import CheckStatus

        for check in result.checks:
            if check.status == CheckStatus.WARN:
                check.status = CheckStatus.PASS
                break

        # Generate diff
        baseline = load_baseline(baseline_path)
        md = generate_diff_markdown(baseline, result)

        assert "Progress Report" in md
        assert "Improvements" in md
        # Should show the check that improved
        assert any(name in md for name, _, _ in compute_diff(baseline, result).improvements)

    def test_diff_score_displayed(self, sample_repo):
        result = scan_repo(str(sample_repo))
        baseline = result.to_dict()
        md = generate_diff_markdown(baseline, result)
        # Should contain "X/Y (was Z/W)" pattern
        assert "/17" in md or "/" in md
        assert "was" in md
