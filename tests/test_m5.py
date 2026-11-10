"""Tests for M5: FAIR integrations, extended checks, knowledge base."""

import json

import pytest

from everse_scan.checks.extended import (
    check_api_docs,
    check_archiving,
    check_authorship,
    check_changelog,
    check_code_of_conduct,
    check_containers,
    check_contribution_guide,
    check_data_management,
    check_dependency_management,
    check_env_sustainability,
    check_future_proofing,
    check_issue_templates,
    check_orcid,
    check_quality_model,
    check_reproducibility_checklist,
    check_secret_management,
    check_software_peer_review,
    check_sustainability_plan,
    check_workflow_files,
)
from everse_scan.integrations.cffconvert import check_cffconvert
from everse_scan.integrations.codemeta import check_codemeta_validation
from everse_scan.integrations.howfairis import check_howfairis
from everse_scan.knowledge.rsqkit import (
    TASKS,
    TOOLS_BY_LANGUAGE,
    get_covered_tasks,
    get_task,
    get_tools,
    get_uncovered_tasks,
    tasks_by_category,
)
from everse_scan.models import CheckStatus
from everse_scan.scanner import scan_repo
from tests.fixtures import create_minimal_repo, create_sample_repo


@pytest.fixture
def sample_repo(tmp_path):
    return create_sample_repo(tmp_path)


@pytest.fixture
def minimal_repo(tmp_path):
    return create_minimal_repo(tmp_path)


class TestKnowledgeBase:
    def test_has_35_plus_tasks(self):
        assert len(TASKS) >= 35

    def test_get_task(self):
        t = get_task("readme")
        assert t is not None
        assert t.name == "Creating good README"

    def test_get_task_unknown(self):
        assert get_task("nonexistent") is None

    def test_covered_tasks(self):
        covered = get_covered_tasks()
        assert len(covered) >= 35

    def test_uncovered_tasks(self):
        uncovered = get_uncovered_tasks()
        # Most tasks should be covered now
        assert len(uncovered) <= 5

    def test_tasks_by_category(self):
        eng = tasks_by_category("engineering")
        assert len(eng) > 0
        fair = tasks_by_category("fair")
        assert len(fair) > 0

    def test_tools_by_language(self):
        python_tools = TOOLS_BY_LANGUAGE.get("Python", {})
        assert "testing" in python_tools
        assert "pytest" in python_tools["testing"]

    def test_get_tools(self):
        r_tools = get_tools("R", "testing")
        assert "testthat" in r_tools

    def test_get_tools_unknown_language(self):
        assert get_tools("UnknownLang", "testing") == []


class TestExtendedChecks:
    def test_authorship_pass(self, sample_repo):
        result = check_authorship(str(sample_repo))
        assert result.status == CheckStatus.PASS

    def test_authorship_warn(self, minimal_repo):
        result = check_authorship(str(minimal_repo))
        assert result.status == CheckStatus.WARN

    def test_orcid_warn(self, sample_repo):
        result = check_orcid(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_dependency_management_warn(self, sample_repo):
        result = check_dependency_management(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_containers_warn(self, sample_repo):
        result = check_containers(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_workflow_files_na(self, sample_repo):
        result = check_workflow_files(str(sample_repo))
        assert result.status == CheckStatus.NA

    def test_api_docs_warn(self, sample_repo):
        result = check_api_docs(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_changelog_pass(self, sample_repo):
        result = check_changelog(str(sample_repo))
        assert result.status == CheckStatus.PASS

    def test_changelog_warn(self, minimal_repo):
        result = check_changelog(str(minimal_repo))
        assert result.status == CheckStatus.WARN

    def test_contribution_guide_warn(self, sample_repo):
        result = check_contribution_guide(str(sample_repo))
        assert result.status == CheckStatus.WARN

    def test_code_of_conduct_warn(self, sample_repo):
        result = check_code_of_conduct(str(sample_repo))
        assert result.status == CheckStatus.WARN

    def test_issue_templates_warn(self, sample_repo):
        result = check_issue_templates(str(sample_repo))
        assert result.status == CheckStatus.WARN

    def test_secret_management(self, sample_repo):
        result = check_secret_management(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_data_management_warn(self, sample_repo):
        result = check_data_management(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_reproducibility_checklist_warn(self, sample_repo):
        result = check_reproducibility_checklist(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_archiving_warn(self, sample_repo):
        result = check_archiving(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_future_proofing(self, sample_repo):
        result = check_future_proofing(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_sustainability_plan_warn(self, sample_repo):
        result = check_sustainability_plan(str(sample_repo))
        assert result.status in (CheckStatus.WARN, CheckStatus.PASS)

    def test_env_sustainability(self, sample_repo):
        result = check_env_sustainability(str(sample_repo))
        assert result.status in (CheckStatus.NA, CheckStatus.WARN, CheckStatus.PASS)

    def test_software_peer_review_na(self, sample_repo):
        result = check_software_peer_review(str(sample_repo))
        assert result.status == CheckStatus.NA

    def test_quality_model_na(self, sample_repo):
        result = check_quality_model(str(sample_repo))
        assert result.status in (CheckStatus.NA, CheckStatus.WARN, CheckStatus.PASS)


class TestHowfairisIntegration:
    def test_returns_5_principles(self, sample_repo):
        results = check_howfairis(str(sample_repo))
        assert len(results) == 5
        names = [r.name for r in results]
        assert "FAIR: repository" in names
        assert "FAIR: license" in names
        assert "FAIR: registry" in names
        assert "FAIR: citation" in names
        assert "FAIR: checklist" in names

    def test_repository_principle_pass(self, sample_repo):
        results = check_howfairis(str(sample_repo))
        repo_check = next(r for r in results if r.name == "FAIR: repository")
        assert repo_check.status == CheckStatus.PASS

    def test_citation_principle(self, sample_repo):
        results = check_howfairis(str(sample_repo))
        citation_check = next(r for r in results if r.name == "FAIR: citation")
        assert citation_check.status == CheckStatus.PASS


class TestCffconvertIntegration:
    def test_valid_citation(self, sample_repo):
        result = check_cffconvert(str(sample_repo))
        assert result.name == "CITATION.cff validation"
        assert result.status in (CheckStatus.PASS, CheckStatus.WARN)

    def test_no_citation(self, minimal_repo):
        result = check_cffconvert(str(minimal_repo))
        assert result.status == CheckStatus.FAIL


class TestCodemetaIntegration:
    def test_no_codemeta(self, sample_repo):
        result = check_codemeta_validation(str(sample_repo))
        assert result.status == CheckStatus.FAIL

    def test_no_codemeta_minimal(self, minimal_repo):
        result = check_codemeta_validation(str(minimal_repo))
        assert result.status == CheckStatus.FAIL

    def test_valid_codemeta(self, tmp_path):
        repo = tmp_path / "cm-repo"
        repo.mkdir()
        (repo / "codemeta.json").write_text(
            json.dumps(
                {
                    "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
                    "@type": "SoftwareSourceCode",
                    "name": "Test",
                    "author": [{"@type": "Person", "name": "Test"}],
                    "license": "MIT",
                    "version": "1.0.0",
                    "url": "https://example.com",
                    "identifier": "https://doi.org/10.0001/test",
                    "description": "Test software",
                    "codeRepository": "https://github.com/test/test",
                    "dateCreated": "2024-01-01",
                }
            )
        )
        result = check_codemeta_validation(str(repo))
        assert result.status == CheckStatus.PASS


class TestScannerWithIntegrations:
    def test_scan_without_integrations(self, sample_repo):
        result = scan_repo(str(sample_repo))
        assert result.total >= 35
        # No FAIR: checks
        assert not any(c.name.startswith("FAIR:") for c in result.checks)

    def test_scan_with_integrations(self, sample_repo):
        result = scan_repo(str(sample_repo), use_integrations=True)
        assert result.total >= 42  # 35 native + 5 howfairis + cffconvert + codemeta
        # FAIR checks present
        fair_checks = [c for c in result.checks if c.name.startswith("FAIR:")]
        assert len(fair_checks) == 5
        # Validation checks present
        val_checks = [c for c in result.checks if "validation" in c.name]
        assert len(val_checks) == 2

    def test_extended_checks_present(self, sample_repo):
        result = scan_repo(str(sample_repo))
        names = {c.name for c in result.checks}
        assert "Authorship" in names
        assert "Changelog" in names
        assert "Contribution guidelines" in names
        assert "Secret management" in names
        assert "Archiving" in names
