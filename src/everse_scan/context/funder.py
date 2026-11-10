"""Funder detection: identify research funders from repository metadata.

Detects funder references in:
- .zenodo.json (grants field)
- CITATION.cff (grants field)
- README.md (funder mentions)
- pyproject.toml (funding field)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FunderResult:
    funder: str  # "horizon_europe", "nsf", "wellcome", "unknown", ""
    funder_label: str  # "Horizon Europe", "NSF", "Wellcome", ""
    grant_ids: list[str] = field(default_factory=list)
    detection_sources: list[str] = field(default_factory=list)
    confidence: str = "low"  # "high", "medium", "low"

    @property
    def detected(self) -> bool:
        return bool(self.funder)


# Funder detection patterns
FUNDER_PATTERNS = {
    "horizon_europe": {
        "label": "Horizon Europe",
        "patterns": [
            r"horizon\s*europe",
            r"h2020",
            r"horizon\s*2020",
            r"european\s*union.*fund",
            r"eu\s*grant",
            r"101\d{6}",  # Horizon Europe grant numbers
            r"95\d{6}",  # H2020 grant numbers
        ],
        "grant_pattern": r"(?:101|95)\d{6}",
    },
    "nsf": {
        "label": "NSF (National Science Foundation)",
        "patterns": [
            r"national\s*science\s*foundation",
            r"\bnsf\b",
            r"nsf\s*grant",
            r"nsf\s*award",
        ],
        "grant_pattern": r"NSF[-\s]?\d{7,8}",
    },
    "wellcome": {
        "label": "Wellcome Trust",
        "patterns": [
            r"wellcome\s*trust",
            r"wellcome\s*fund",
        ],
        "grant_pattern": r"[0-9]{2,5}[A-Z]{2}",
    },
    "rcuk": {
        "label": "UK Research and Innovation (UKRI)",
        "patterns": [
            r"ukri",
            r"research\s*councils\s*uk",
            r"\brcuk\b",
            r"\bepsrc\b",
            r"\bbsrc\b",
            r"\bnerc\b",
            r"\bahrc\b",
            r"\besrc\b",
            r"\bstfc\b",
            r"\bmrc\b",
        ],
        "grant_pattern": r"[A-Z]{2,5}/[A-Z0-9]+/\d+",
    },
    "dfg": {
        "label": "DFG (Deutsche Forschungsgemeinschaft)",
        "patterns": [
            r"deutsche\s*forschungsgemeinschaft",
            r"\bdfg\b",
            r"dfg\s*grant",
        ],
        "grant_pattern": r"",
    },
    "anr": {
        "label": "ANR (Agence Nationale de la Recherche)",
        "patterns": [
            r"agence\s*nationale\s*de\s*la\s*recherche",
            r"\banr[-\s]?\d",
        ],
        "grant_pattern": r"ANR[-\s]?\d{2}[A-Z]?-\d{4}",
    },
    "nwo": {
        "label": "NWO (Dutch Research Council)",
        "patterns": [
            r"dutch\s*research\s*council",
            r"\bnwo\b",
        ],
        "grant_pattern": r"",
    },
    "mrc": {
        "label": "MRC (Medical Research Council)",
        "patterns": [
            r"medical\s*research\s*council",
        ],
        "grant_pattern": r"",
    },
    "czi": {
        "label": "Chan Zuckerberg Initiative",
        "patterns": [
            r"chan\s*zuckerberg",
            r"\bczi\b",
        ],
        "grant_pattern": r"",
    },
    "sloan": {
        "label": "Alfred P. Sloan Foundation",
        "patterns": [
            r"sloan\s*foundation",
            r"alfred\s*p\.\s*sloan",
        ],
        "grant_pattern": r"",
    },
    "helmholtz": {
        "label": "Helmholtz Association",
        "patterns": [
            r"helmholtz\s*association",
            r"\bhelmholtz\b",
        ],
        "grant_pattern": r"",
    },
}


def detect_funder(repo_path: str) -> FunderResult:
    """Detect the funder of a research software project."""
    path = Path(repo_path)
    sources: list[str] = []
    detected_funders: dict[str, list[str]] = {}
    all_text = ""

    # 1. Check .zenodo.json
    zenodo = path / ".zenodo.json"
    if zenodo.exists():
        try:
            data = json.loads(zenodo.read_text())
            grants = data.get("grants", [])
            if grants:
                sources.append(".zenodo.json (grants)")
                for g in grants:
                    grant_id = g.get("id", "") if isinstance(g, dict) else str(g)
                    funder_name = g.get("funder", "") if isinstance(g, dict) else ""
                    all_text += f" {funder_name} {grant_id}"
                    if grant_id:
                        detected_funders.setdefault("unknown", []).append(grant_id)
        except json.JSONDecodeError:
            pass

    # 2. Check CITATION.cff
    cff = path / "CITATION.cff"
    if cff.exists():
        content = cff.read_text(errors="ignore")
        if "grant" in content.lower() or "funder" in content.lower() or "funding" in content.lower():
            sources.append("CITATION.cff (grants/funding)")
            all_text += f" {content}"

    # 3. Check README.md
    readme = path / "README.md"
    if readme.exists():
        content = readme.read_text(errors="ignore")
        # Look for funder section
        for section_header in ["## Acknowledgements", "## Funding", "## Acknowledgment", "## Grant"]:
            if section_header.lower() in content.lower():
                sources.append(f"README.md ({section_header})")
        all_text += f" {content}"

    # 4. Check pyproject.toml
    pp = path / "pyproject.toml"
    if pp.exists():
        content = pp.read_text(errors="ignore")
        if "funding" in content.lower() or "grant" in content.lower():
            sources.append("pyproject.toml (funding)")
            all_text += f" {content}"

    # Match against funder patterns
    best_funder = ""
    best_label = ""
    best_confidence = "low"
    grant_ids: list[str] = []

    for funder_id, info in FUNDER_PATTERNS.items():
        for pattern in info["patterns"]:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                best_funder = funder_id
                best_label = info["label"]
                # Determine confidence
                if any(src.startswith(".zenodo.json") for src in sources) or any(
                    "CITATION.cff" in src for src in sources
                ):
                    best_confidence = "high"
                elif any("README.md" in src for src in sources):
                    best_confidence = "medium"
                else:
                    best_confidence = "low"

                # Extract grant IDs
                if info["grant_pattern"]:
                    grant_ids = re.findall(info["grant_pattern"], all_text, re.IGNORECASE)
                break
        if best_funder:
            break

    return FunderResult(
        funder=best_funder,
        funder_label=best_label,
        grant_ids=grant_ids,
        detection_sources=sources,
        confidence=best_confidence,
    )
