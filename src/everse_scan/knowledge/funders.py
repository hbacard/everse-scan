"""Funder requirements database.

Maps funders to their software compliance requirements.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class FunderRequirement:
    id: str
    description: str
    related_check: str       # Check name in the scanner
    mandatory: bool = True  # Is this strictly required?


@dataclass(frozen=True)
class FunderProfile:
    id: str
    label: str
    requirements: list[FunderRequirement]
    url: str = ""


# Funder requirement profiles
FUNDER_PROFILES: dict[str, FunderProfile] = {
    "horizon_europe": FunderProfile(
        id="horizon_europe",
        label="Horizon Europe",
        url="https://research-and-innovation.ec.europa.eu/funding/funding-opportunities_en",
        requirements=[
            FunderRequirement("open_source_license", "Open source license (OSI-approved)", "LICENSE", True),
            FunderRequirement("doi", "Persistent identifier (DOI) for the software", "Software identifiers", True),
            FunderRequirement("citation", "CITATION.cff for proper attribution", "CITATION.cff", True),
            FunderRequirement("codemeta", "codemeta.json for machine-readable metadata", "codemeta.json", True),
            FunderRequirement("repository", "Public version control repository", "Version control", True),
            FunderRequirement("documentation", "Documentation for users and developers", "Documentation", True),
            FunderRequirement("license_file", "Dedicated LICENSE file (not just in pyproject.toml)", "LICENSE", True),
            FunderRequirement("archiving", "Archiving in Zenodo or similar", "Archiving", True),
        ],
    ),
    "nsf": FunderProfile(
        id="nsf",
        label="NSF (National Science Foundation)",
        url="https://www.nsf.gov/",
        requirements=[
            FunderRequirement("repository", "Public version control repository", "Version control", True),
            FunderRequirement("license", "Open source license", "LICENSE", True),
            FunderRequirement("documentation", "Documentation", "Documentation", True),
            FunderRequirement("citation", "CITATION.cff for attribution", "CITATION.cff", False),
            FunderRequirement("doi", "DOI for reproducibility", "Software identifiers", False),
        ],
    ),
    "wellcome": FunderProfile(
        id="wellcome",
        label="Wellcome Trust",
        url="https://wellcome.org/",
        requirements=[
            FunderRequirement("open_source_license", "Open source license", "LICENSE", True),
            FunderRequirement("doi", "Persistent identifier (DOI)", "Software identifiers", True),
            FunderRequirement("citation", "CITATION.cff", "CITATION.cff", True),
            FunderRequirement("repository", "Public repository", "Version control", True),
            FunderRequirement("documentation", "Documentation", "Documentation", True),
            FunderRequirement("tests", "Tests for reproducibility", "Tests", False),
        ],
    ),
    "rcuk": FunderProfile(
        id="rcuk",
        label="UKRI",
        url="https://www.ukri.org/",
        requirements=[
            FunderRequirement("open_source_license", "Open source license", "LICENSE", True),
            FunderRequirement("doi", "DOI", "Software identifiers", True),
            FunderRequirement("citation", "CITATION.cff", "CITATION.cff", True),
            FunderRequirement("repository", "Public repository", "Version control", True),
            FunderRequirement("documentation", "Documentation", "Documentation", True),
        ],
    ),
    "dfg": FunderProfile(
        id="dfg",
        label="DFG",
        url="https://www.dfg.de/",
        requirements=[
            FunderRequirement("repository", "Public repository", "Version control", True),
            FunderRequirement("license", "Open source license", "LICENSE", True),
            FunderRequirement("documentation", "Documentation", "Documentation", True),
            FunderRequirement("citation", "CITATION.cff", "CITATION.cff", False),
        ],
    ),
    "anr": FunderProfile(
        id="anr",
        label="ANR",
        url="https://anr.fr/",
        requirements=[
            FunderRequirement("repository", "Public repository", "Version control", True),
            FunderRequirement("license", "Open source license", "LICENSE", True),
            FunderRequirement("doi", "DOI", "Software identifiers", True),
            FunderRequirement("citation", "CITATION.cff", "CITATION.cff", True),
            FunderRequirement("documentation", "Documentation", "Documentation", True),
        ],
    ),
    "helmholtz": FunderProfile(
        id="helmholtz",
        label="Helmholtz Association",
        url="https://www.helmholtz.de/",
        requirements=[
            FunderRequirement("repository", "Public repository", "Version control", True),
            FunderRequirement("license", "Open source license", "LICENSE", True),
            FunderRequirement("citation", "CITATION.cff", "CITATION.cff", True),
            FunderRequirement("documentation", "Documentation", "Documentation", True),
        ],
    ),
}


def get_funder_profile(funder_id: str) -> Optional[FunderProfile]:
    return FUNDER_PROFILES.get(funder_id)


def list_funders() -> list[str]:
    return list(FUNDER_PROFILES.keys())
