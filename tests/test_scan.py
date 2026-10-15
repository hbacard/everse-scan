"""Tests for everse-scan."""

import json

import pytest

from everse_scan.context.lifecycle import LIFECYCLE_EARLY, detect_lifecycle
from everse_scan.context.tier import TIER_SCRIPT, TIER_TOOL, detect_tier
from everse_scan.languages.detector import detect_languages
from everse_scan.models import CheckStatus
from everse_scan.reporters.json import generate_json
from everse_scan.reporters.markdown import generate_markdown
from everse_scan.scanner import scan_repo
from tests.fixtures import create_minimal_repo, create_sample_repo


@pytest.fixture
def sample_repo(tmp_path):
    return create_sample_repo(tmp_path)


@pytest.fixture
def minimal_repo(tmp_path):
    return create_minimal_repo(tmp_path)


class TestLanguageDetector:
    def test_detect_python(self, sample_repo):
        info = detect_languages(str(sample_repo))
        assert "Python" in info.languages
        assert info.primary == "Python"

    def test_detect_no_language(self, minimal_repo):
        info = detect_languages(str(minimal_repo))
        # .py file should still be detected
        assert "Python" in info.languages


class TestTierDetection:
    def test_sample_repo_is_tool(self, sample_repo):
        result = detect_tier(str(sample_repo))
        assert result.tier in (TIER_TOOL, "infrastructure")

    def test_minimal_repo_is_script(self, minimal_repo):
        result = detect_tier(str(minimal_repo))
        assert result.tier == TIER_SCRIPT


class TestLifecycleDetection:
    def test_sample_repo_early(self, sample_repo):
        result = detect_lifecycle(str(sample_repo))
        # With 1 commit and 1 tag, could be early or maintenance
        assert result.stage in (LIFECYCLE_EARLY, "maintenance", "active_dev")


class TestScanner:
    def test_scan_returns_result(self, sample_repo):
        result = scan_repo(str(sample_repo))
        assert result.repo_name == "sample-python"
        assert result.primary_language == "Python"
        assert len(result.checks) >= 17
        assert result.total >= 17

    def test_scan_has_all_checks(self, sample_repo):
        result = scan_repo(str(sample_repo))
        check_names = {c.name for c in result.checks}
        # Core 17 checks must be present
        expected_core = {
            "README",
            "LICENSE",
            "CITATION.cff",
            "codemeta.json",
            "Structure",
            "Version control",
            "Tests",
            "Documentation",
            "CI/CD",
            "Packaging",
            "Static analysis",
            "Security",
            "Reproducible environments",
            "Code review",
            "Software identifiers",
            "Releasing",
            "Readable code",
        }
        assert expected_core.issubset(check_names)

    def test_scan_passes_good_repo(self, sample_repo):
        result = scan_repo(str(sample_repo))
        assert result.passed > 0
        # README should pass
        readme_check = next(c for c in result.checks if c.name == "README")
        assert readme_check.status == CheckStatus.PASS

    def test_scan_fails_minimal_repo(self, minimal_repo):
        result = scan_repo(str(minimal_repo))
        assert result.failed > 0
        # README should fail
        readme_check = next(c for c in result.checks if c.name == "README")
        assert readme_check.status == CheckStatus.FAIL


class TestJSONReporter:
    def test_json_output_valid(self, sample_repo):
        result = scan_repo(str(sample_repo))
        json_str = generate_json(result)
        data = json.loads(json_str)
        assert data["repo_name"] == "sample-python"
        assert "checks" in data
        assert len(data["checks"]) >= 17
        assert "summary" in data
        assert data["summary"]["total"] >= 17

    def test_json_has_tier_and_lifecycle(self, sample_repo):
        result = scan_repo(str(sample_repo))
        data = json.loads(generate_json(result))
        assert data["tier"] != ""
        assert data["lifecycle"] != ""


class TestMarkdownReporter:
    def test_markdown_has_sections(self, sample_repo):
        result = scan_repo(str(sample_repo))
        md = generate_markdown(result)
        assert "# EVERSE Scan Report" in md
        assert "## 1. Executive Summary" in md
        assert "## 2. Prioritized Action Plan" in md
        assert "## 3. Technical Details by Task" in md
        assert "## 4. AI Usage Determination" in md

    def test_markdown_has_all_checks(self, sample_repo):
        result = scan_repo(str(sample_repo))
        md = generate_markdown(result)
        for c in result.checks:
            assert c.name in md

    def test_markdown_has_quality_dimensions(self, sample_repo):
        result = scan_repo(str(sample_repo))
        md = generate_markdown(result)
        assert "Quality Dimensions" in md
        assert "Reproducibility" in md
        assert "Maintainability" in md
        assert "Findability" in md

    def test_markdown_has_tier(self, sample_repo):
        result = scan_repo(str(sample_repo))
        md = generate_markdown(result)
        assert "Tier" in md
        assert "tier" in md.lower() or "Script" in md or "Tool" in md or "Infrastructure" in md
