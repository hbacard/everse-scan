"""Check: Packaging configuration."""

from __future__ import annotations

import json
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus


def _check_pyproject(path: Path) -> dict[str, object]:
    info: dict[str, object] = {
        "has_build_system": False,
        "has_name": False,
        "has_version": False,
        "has_scripts": False,
        "deps": 0,
    }
    pp = path / "pyproject.toml"
    if pp.exists():
        content = pp.read_text(errors="ignore")
        info["has_build_system"] = "[build-system]" in content
        info["has_name"] = "name" in content.split("[project]", 1)[-1] if "[project]" in content else False
        info["has_version"] = "version" in content.split("[project]", 1)[-1] if "[project]" in content else False
        info["has_scripts"] = "[project.scripts]" in content
        info["deps"] = content.count("=") if "dependencies" in content else 0
    return info


def _check_package_json(path: Path) -> dict[str, object]:
    info: dict[str, object] = {"has_name": False, "has_version": False, "has_main": False, "has_bin": False}
    pj = path / "package.json"
    if pj.exists():
        try:
            data = json.loads(pj.read_text(errors="ignore"))
            info["has_name"] = bool(data.get("name"))
            info["has_version"] = bool(data.get("version"))
            info["has_main"] = bool(data.get("main") or data.get("exports"))
            info["has_bin"] = bool(data.get("bin"))
        except json.JSONDecodeError:
            pass
    return info


def check_packaging(repo_path: str, language: str | None = None) -> CheckResult:
    path = Path(repo_path)

    packaging_found = []
    details = []
    recs = []
    score = 0

    if language == "Python" or language is None:
        pp_info = _check_pyproject(path)
        if (path / "pyproject.toml").exists():
            packaging_found.append("pyproject.toml")
            score += sum([pp_info["has_build_system"], pp_info["has_name"], pp_info["has_version"]])
            details.append(
                f"pyproject.toml: build-system={pp_info['has_build_system']}, "
                f"name={pp_info['has_name']}, version={pp_info['has_version']}, "
                f"scripts={pp_info['has_scripts']}"
            )
        if (path / "setup.py").exists():
            packaging_found.append("setup.py")
            score += 1
            details.append("setup.py: present (consider migrating to pyproject.toml)")
        if (path / "Dockerfile").exists():
            packaging_found.append("Dockerfile")
            score += 1
            details.append("Dockerfile: present")

    if language == "JavaScript/TypeScript" or language is None:
        pj_info = _check_package_json(path)
        if (path / "package.json").exists():
            packaging_found.append("package.json")
            score += sum([pj_info["has_name"], pj_info["has_version"], pj_info["has_main"]])
            details.append(
                f"package.json: name={pj_info['has_name']}, "
                f"version={pj_info['has_version']}, main={pj_info['has_main']}"
            )

    if language in ("R", None) and (path / "DESCRIPTION").exists():
        packaging_found.append("DESCRIPTION")
        score += 2
        details.append("DESCRIPTION: present")

    if language in ("Julia", None) and (path / "Project.toml").exists():
        packaging_found.append("Project.toml")
        score += 2
        details.append("Project.toml: present")

    if language in ("Rust", None) and (path / "Cargo.toml").exists():
        packaging_found.append("Cargo.toml")
        score += 2
        details.append("Cargo.toml: present")

    if language in ("C/C++", None) and (path / "CMakeLists.txt").exists():
        packaging_found.append("CMakeLists.txt")
        score += 2
        details.append("CMakeLists.txt: present")

    if not packaging_found:
        return CheckResult(
            name="Packaging",
            status=CheckStatus.FAIL,
            message="No packaging configuration found",
            details=["No pyproject.toml, package.json, Cargo.toml, DESCRIPTION, or other packaging file"],
            recommendations=["Create a packaging file appropriate for your language"],
            rsqkit_url="https://everse.software/RSQKit/packaging_software",
            category="quality",
        )

    if score >= 3:
        status = CheckStatus.PASS
        msg = f"Packaging well configured ({', '.join(packaging_found)})"
    elif score >= 1:
        status = CheckStatus.WARN
        msg = f"Packaging present but incomplete ({', '.join(packaging_found)})"
        recs.append("Add missing packaging metadata (name, version, dependencies)")
    else:
        status = CheckStatus.WARN
        msg = f"Packaging file present but minimal ({', '.join(packaging_found)})"

    if (path / "setup.py").exists() and not (path / "pyproject.toml").exists():
        recs.append("Migrate from setup.py to pyproject.toml (modern Python standard)")

    return CheckResult(
        name="Packaging",
        status=status,
        message=msg,
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/packaging_software",
        category="quality",
    )
