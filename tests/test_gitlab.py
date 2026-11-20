"""Tests for GitLab-hosted repository support (non-GitHub layouts)."""

import pytest

from everse_scan.checks.cicd import check_cicd
from everse_scan.checks.documentation import check_documentation
from everse_scan.checks.license import check_license
from everse_scan.checks.structure import check_structure
from everse_scan.checks.tests import check_tests
from everse_scan.checks.version_control import check_version_control
from everse_scan.languages.detector import detect_languages
from everse_scan.models import CheckStatus
from tests.fixtures import create_gitlab_cpp_repo


@pytest.fixture
def gitlab_cpp_repo(tmp_path):
    return create_gitlab_cpp_repo(tmp_path)


class TestGitLabLanguage:
    def test_cpp_primary_despite_doxygen_js(self, gitlab_cpp_repo):
        info = detect_languages(str(gitlab_cpp_repo))
        # Generated doxygen JS and cmake-build-debug artifacts must not skew detection
        assert "C/C++" in info.languages
        assert info.primary == "C/C++"

    def test_cmakes_packaging(self, gitlab_cpp_repo):
        # CMakeLists.txt is the packaging signal for C++ projects
        from everse_scan.checks.packaging import check_packaging

        result = check_packaging(str(gitlab_cpp_repo), "C/C++")
        assert result.status in (CheckStatus.PASS, CheckStatus.WARN)


class TestGitLabCICD:
    def test_gitlab_ci_test_job_detected(self, gitlab_cpp_repo):
        result = check_cicd(str(gitlab_cpp_repo))
        assert any("Test job: yes" in d for d in result.details)
        # GitLab CI with a test job should not be scored as the weakest tier
        assert "GitLab CI" in result.message or "GitLab CI" in " ".join(result.details)


class TestGitLabLicense:
    def test_cecill_license_recognized(self, gitlab_cpp_repo):
        result = check_license(str(gitlab_cpp_repo))
        assert result.status == CheckStatus.PASS
        assert "CeCILL" in result.message


class TestGitLabVersionControl:
    def test_commit_count(self, gitlab_cpp_repo):
        result = check_version_control(str(gitlab_cpp_repo))
        assert any("Commits: 3" in d for d in result.details)

    def test_tags_detected(self, gitlab_cpp_repo):
        result = check_version_control(str(gitlab_cpp_repo))
        assert any("Tags/releases: 1" in d for d in result.details)


class TestGitLabStructure:
    def test_structure_not_fail(self, gitlab_cpp_repo):
        result = check_structure(str(gitlab_cpp_repo))
        assert result.status != CheckStatus.FAIL

    def test_documentation_dir_detected(self, gitlab_cpp_repo):
        result = check_structure(str(gitlab_cpp_repo))
        assert result.status != CheckStatus.FAIL
        docs_check = check_documentation(str(gitlab_cpp_repo), "C/C++")
        assert any("yes (documentation/)" in d for d in docs_check.details)


class TestGitLabTests:
    def test_cpp_tests_detected(self, gitlab_cpp_repo):
        result = check_tests(str(gitlab_cpp_repo), "C/C++")
        assert result.status in (CheckStatus.PASS, CheckStatus.WARN)
        assert any("Google Test" in d for d in result.details)
