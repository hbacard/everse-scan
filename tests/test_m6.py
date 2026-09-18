"""Tests for M6: Funder compliance detection and reporting."""

import json
from pathlib import Path

import pytest

from everse_scan.context.funder import detect_funder, FunderResult
from everse_scan.knowledge.funders import (
    FUNDER_PROFILES, get_funder_profile, list_funders,
    FunderProfile, FunderRequirement,
)
from everse_scan.reporters.funder import generate_funder_section
from everse_scan.scanner import scan_repo
from everse_scan.models import CheckStatus

from tests.fixtures import create_sample_repo


@pytest.fixture
def sample_repo(tmp_path):
    return create_sample_repo(tmp_path)


class TestFunderDetection:
    def test_no_funder_detected(self, sample_repo):
        result = detect_funder(str(sample_repo))
        assert result.detected is False

    def test_horizon_europe_from_zenodo(self, tmp_path):
        repo = tmp_path / "he-repo"
        repo.mkdir()
        (repo / ".zenodo.json").write_text(json.dumps({
            "grants": [
                {"id": "101095456", "funder": "European Commission"}
            ]
        }))
        result = detect_funder(str(repo))
        assert result.detected is True
        assert result.funder == "horizon_europe"
        assert result.confidence == "high"

    def test_horizon_europe_from_readme(self, tmp_path):
        repo = tmp_path / "he-readme"
        repo.mkdir()
        (repo / "README.md").write_text(
            "# Project\n\n"
            "## Acknowledgements\n\n"
            "This project has received funding from Horizon Europe "
            "under grant agreement No 101095456.\n"
        )
        result = detect_funder(str(repo))
        assert result.detected is True
        assert result.funder == "horizon_europe"
        assert result.confidence == "medium"

    def test_nsf_from_readme(self, tmp_path):
        repo = tmp_path / "nsf-repo"
        repo.mkdir()
        (repo / "README.md").write_text(
            "# Project\n\n"
            "## Funding\n\n"
            "This work was supported by the NSF under grant NSF-1234567.\n"
        )
        result = detect_funder(str(repo))
        assert result.detected is True
        assert result.funder == "nsf"

    def test_wellcome_from_readme(self, tmp_path):
        repo = tmp_path / "wellcome-repo"
        repo.mkdir()
        (repo / "README.md").write_text(
            "# Project\n\n"
            "## Funding\n\n"
            "Supported by the Wellcome Trust.\n"
        )
        result = detect_funder(str(repo))
        assert result.detected is True
        assert result.funder == "wellcome"

    def test_dfg_from_readme(self, tmp_path):
        repo = tmp_path / "dfg-repo"
        repo.mkdir()
        (repo / "README.md").write_text(
            "# Project\n\n"
            "Funded by DFG (Deutsche Forschungsgemeinschaft).\n"
        )
        result = detect_funder(str(repo))
        assert result.detected is True
        assert result.funder == "dfg"

    def test_anr_from_readme(self, tmp_path):
        repo = tmp_path / "anr-repo"
        repo.mkdir()
        (repo / "README.md").write_text(
            "# Project\n\n"
            "Funded by ANR-23-CE46-0001.\n"
        )
        result = detect_funder(str(repo))
        assert result.detected is True
        assert result.funder == "anr"

    def test_grant_ids_extracted(self, tmp_path):
        repo = tmp_path / "he-grant"
        repo.mkdir()
        (repo / ".zenodo.json").write_text(json.dumps({
            "grants": [{"id": "101095456", "funder": "EC"}]
        }))
        result = detect_funder(str(repo))
        assert "101095456" in result.grant_ids

    def test_helmholtz_from_readme(self, tmp_path):
        repo = tmp_path / "hf-repo"
        repo.mkdir()
        (repo / "README.md").write_text(
            "# Project\n\n"
            "Supported by the Helmholtz Association.\n"
        )
        result = detect_funder(str(repo))
        assert result.detected is True
        assert result.funder == "helmholtz"


class TestFunderProfiles:
    def test_list_funders(self):
        funders = list_funders()
        assert "horizon_europe" in funders
        assert "nsf" in funders
        assert "wellcome" in funders

    def test_get_horizon_profile(self):
        profile = get_funder_profile("horizon_europe")
        assert profile is not None
        assert profile.label == "Horizon Europe"
        assert len(profile.requirements) > 0

    def test_horizon_has_doi_requirement(self):
        profile = get_funder_profile("horizon_europe")
        doi_req = [r for r in profile.requirements if r.id == "doi"]
        assert len(doi_req) == 1
        assert doi_req[0].mandatory is True

    def test_get_unknown_funder(self):
        assert get_funder_profile("nonexistent") is None

    def test_all_profiles_have_requirements(self):
        for funder_id, profile in FUNDER_PROFILES.items():
            assert len(profile.requirements) > 0, f"{funder_id} has no requirements"


class TestFunderReporter:
    def test_no_funder_section(self, sample_repo):
        result = scan_repo(str(sample_repo))
        from everse_scan.context.funder import FunderResult
        funder = FunderResult(funder="", funder_label="")
        section = generate_funder_section(result, funder)
        assert "No funder detected" in section

    def test_horizon_compliance_section(self, tmp_path):
        repo = tmp_path / "he-compliance"
        repo.mkdir()
        (repo / ".zenodo.json").write_text(json.dumps({
            "grants": [{"id": "101095456", "funder": "European Commission"}]
        }))
        (repo / "README.md").write_text("# Project\n\nFunded by Horizon Europe.\n")
        (repo / ".gitignore").write_text("*.pyc\n")

        result = scan_repo(str(repo))
        from everse_scan.context.funder import FunderResult
        funder = FunderResult(
            funder="horizon_europe",
            funder_label="Horizon Europe",
            grant_ids=["101095456"],
            detection_sources=[".zenodo.json"],
            confidence="high",
        )
        section = generate_funder_section(result, funder)
        assert "Horizon Europe" in section
        assert "Funder Compliance" in section
        assert "Requirements for" in section
        assert "Compliance" in section
        # Should show missing requirements (no LICENSE, no CITATION.cff, etc.)
        assert "Missing" in section or "FAIL" in section

    def test_funder_in_scan_result(self, tmp_path):
        repo = tmp_path / "he-scan"
        repo.mkdir()
        (repo / ".zenodo.json").write_text(json.dumps({
            "grants": [{"id": "101095456", "funder": "EC"}]
        }))
        (repo / "README.md").write_text("# Project\n")
        result = scan_repo(str(repo))
        assert result.funder == "horizon_europe"
        assert result.funder_label == "Horizon Europe"
        assert "101095456" in result.funder_grant_ids

    def test_funder_in_json_output(self, tmp_path):
        repo = tmp_path / "he-json"
        repo.mkdir()
        (repo / ".zenodo.json").write_text(json.dumps({
            "grants": [{"id": "101095456", "funder": "EC"}]
        }))
        (repo / "README.md").write_text("# Project\n")
        result = scan_repo(str(repo))
        data = result.to_dict()
        assert data["funder"] == "horizon_europe"
        assert data["funder_label"] == "Horizon Europe"

    def test_funder_in_markdown_report(self, tmp_path):
        from everse_scan.reporters.markdown import generate_markdown
        repo = tmp_path / "he-md"
        repo.mkdir()
        (repo / ".zenodo.json").write_text(json.dumps({
            "grants": [{"id": "101095456", "funder": "EC"}]
        }))
        (repo / "README.md").write_text("# Project\n")
        result = scan_repo(str(repo))
        md = generate_markdown(result)
        assert "Horizon Europe" in md
        assert "Funder Compliance" in md
