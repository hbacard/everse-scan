"""Check: LICENSE presence and type."""

from __future__ import annotations

import re
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

LICENSE_FILES = {"LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE.txt", "LICENCE", "LICENCE.md", "COPYING", "COPYING.md"}

SPDX_PATTERNS = {
    "MIT": r"MIT License|Permission is hereby granted, free of charge",
    "Apache-2.0": r"Apache License|Version 2\.0",
    "GPL-3.0": r"GNU GENERAL PUBLIC LICENSE|Version 3",
    "GPL-2.0": r"GNU GENERAL PUBLIC LICENSE|Version 2",
    "BSD-3-Clause": r"Redistribution and use in source and binary forms",
    "BSD-2-Clause": r"Redistribution and use in source and binary forms",
    "LGPL-3.0": r"GNU Lesser General Public License",
    "MPL-2.0": r"Mozilla Public License|Version 2\.0",
    "ISC": r"ISC License|Permission to use, copy, modify",
    "Unlicense": r"This is free and unencumbered software released into the public domain",
    # French/CEA-CNRS licenses, common on GitLab-hosted French research software
    "CeCILL": r"CeCILL",
}


def _detect_spdx(content: str) -> str | None:
    for spdx, pattern in SPDX_PATTERNS.items():
        if re.search(pattern, content, re.IGNORECASE):
            return spdx
    return None


def check_license(repo_path: str) -> CheckResult:
    path = Path(repo_path)

    license_file = None
    for name in LICENSE_FILES:
        candidate = path / name
        if candidate.exists():
            license_file = candidate
            break

    if license_file:
        content = license_file.read_text(errors="ignore")
        spdx = _detect_spdx(content)
        if spdx:
            return CheckResult(
                name="LICENSE",
                status=CheckStatus.PASS,
                message=f"License file found: {license_file.name} ({spdx})",
                details=[f"SPDX identifier: {spdx}", f"File: {license_file.name}"],
                rsqkit_url="https://everse.software/RSQKit/licensing_software",
                category="fair",
            )
        return CheckResult(
            name="LICENSE",
            status=CheckStatus.WARN,
            message=f"License file found ({license_file.name}) but type not recognized",
            details=[f"File: {license_file.name}", "Could not identify SPDX license type"],
            recommendations=["Use a standard SPDX license (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause)"],
            rsqkit_url="https://everse.software/RSQKit/licensing_software",
            category="fair",
        )

    # Check if license is mentioned in packaging files
    for pkg_file in ["pyproject.toml", "package.json", "setup.py"]:
        pkg_path = path / pkg_file
        if pkg_path.exists():
            content = pkg_path.read_text(errors="ignore").lower()
            if "license" in content:
                return CheckResult(
                    name="LICENSE",
                    status=CheckStatus.WARN,
                    message=f"License mentioned in {pkg_file} but no dedicated LICENSE file",
                    details=[f"Referenced in: {pkg_file}", "No dedicated LICENSE file at root"],
                    recommendations=["Add a dedicated LICENSE file at the repository root"],
                    rsqkit_url="https://everse.software/RSQKit/licensing_software",
                    category="fair",
                )

    return CheckResult(
        name="LICENSE",
        status=CheckStatus.FAIL,
        message="No license information found",
        details=["No LICENSE file, no license mention in packaging files"],
        recommendations=[
            "Without a license, the software is not legally reusable",
            "Add a LICENSE file (recommend MIT or Apache-2.0 for research software)",
        ],
        rsqkit_url="https://everse.software/RSQKit/licensing_software",
        category="fair",
    )
