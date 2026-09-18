"""Check: Software identifiers (DOI, Zenodo)."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus


def check_software_identifiers(repo_path: str) -> CheckResult:
    path = Path(repo_path)

    has_zenodo = (path / ".zenodo.json").exists()
    has_doi_in_readme = False
    has_doi_in_citation = False

    readme = path / "README.md"
    if readme.exists():
        content = readme.read_text(errors="ignore").lower()
        if "doi.org" in content or "zenodo" in content:
            has_doi_in_readme = True

    citation = path / "CITATION.cff"
    if citation.exists():
        content = citation.read_text(errors="ignore").lower()
        if "doi" in content:
            has_doi_in_citation = True

    details = [
        f".zenodo.json: {'yes' if has_zenodo else 'no'}",
        f"DOI in README: {'yes' if has_doi_in_readme else 'no'}",
        f"DOI in CITATION.cff: {'yes' if has_doi_in_citation else 'no'}",
    ]

    score = sum([has_zenodo, has_doi_in_readme, has_doi_in_citation])

    recs = []
    if not has_zenodo:
        recs.append("Add .zenodo.json to control Zenodo deposition metadata")
    if not has_doi_in_readme:
        recs.append("Add a DOI badge to README (from Zenodo after first release)")

    if score >= 2:
        status = CheckStatus.PASS
        msg = "Software identifiers present"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = "Partial software identifiers"
    else:
        status = CheckStatus.WARN
        msg = "No software identifiers (DOI, Zenodo) found"

    return CheckResult(
        name="Software identifiers",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/software_identifiers",
        category="fair",
    )
