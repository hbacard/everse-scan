"""Extended checks for M5: covers additional RSQKit tasks to reach 35+ total."""

from __future__ import annotations

import os
import re
from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus


def check_authorship(repo_path: str) -> CheckResult:
    """Check for authorship and contribution metadata."""
    path = Path(repo_path)
    details: list[str] = []

    has_citation = (path / "CITATION.cff").exists()
    has_codemeta = (path / "codemeta.json").exists()
    has_authors = (path / "AUTHORS").exists() or (path / "AUTHORS.md").exists()

    if has_citation:
        details.append("CITATION.cff found (authors field)")
    if has_codemeta:
        details.append("codemeta.json found (author field)")
    if has_authors:
        details.append("AUTHORS file found")

    if has_citation or has_codemeta or has_authors:
        return CheckResult(
            name="Authorship",
            status=CheckStatus.PASS,
            message="Authorship information found",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/authorship_and_contributions",
            category="fair",
        )
    return CheckResult(
        name="Authorship",
        status=CheckStatus.WARN,
        message="No authorship metadata found (CITATION.cff, codemeta.json, or AUTHORS)",
        details=details,
        recommendations=["Add authorship info to CITATION.cff or codemeta.json"],
        rsqkit_url="https://everse.software/RSQKit/authorship_and_contributions",
        category="fair",
    )


def check_orcid(repo_path: str) -> CheckResult:
    """Check for ORCID references in metadata files."""
    path = Path(repo_path)
    orcid_pattern = re.compile(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]")

    files_to_check = ["CITATION.cff", "codemeta.json", "README.md", "AUTHORS", "AUTHORS.md"]
    found_in: list[str] = []

    for fname in files_to_check:
        fpath = path / fname
        if fpath.exists():
            content = fpath.read_text(errors="ignore")
            if orcid_pattern.search(content):
                found_in.append(fname)

    if found_in:
        return CheckResult(
            name="ORCID",
            status=CheckStatus.PASS,
            message=f"ORCID references found in: {', '.join(found_in)}",
            details=[f"ORCID found in {f}" for f in found_in],
            rsqkit_url="https://everse.software/RSQKit/orcid_integration",
            category="fair",
        )
    return CheckResult(
        name="ORCID",
        status=CheckStatus.WARN,
        message="No ORCID references found in metadata files",
        details=["ORCID pattern not found in any metadata file"],
        recommendations=["Add ORCID to CITATION.cff authors or codemeta.json"],
        rsqkit_url="https://everse.software/RSQKit/orcid_integration",
        category="fair",
    )


def check_dependency_management(repo_path: str) -> CheckResult:
    """Check for dependency management tools (Dependabot, Renovate, etc.)."""
    path = Path(repo_path)
    details: list[str] = []
    found: list[str] = []

    dependabot = path / ".github" / "dependabot.yml"
    dependabot2 = path / ".github" / "dependabot.yaml"
    renovate = path / "renovate.json"
    renovate2 = path / ".renovaterc.json"
    renovate3 = path / ".renovaterc"

    if dependabot.exists():
        found.append("Dependabot")
        details.append(f"{dependabot.relative_to(path)} found")
    elif dependabot2.exists():
        found.append("Dependabot")
        details.append(f"{dependabot2.relative_to(path)} found")
    if any(p.exists() for p in [renovate, renovate2, renovate3]):
        found.append("Renovate")
        details.append("Renovate config found")

    if found:
        return CheckResult(
            name="Dependency management",
            status=CheckStatus.PASS,
            message=f"Dependency management configured: {', '.join(found)}",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/dependency_management",
            category="engineering",
        )
    return CheckResult(
        name="Dependency management",
        status=CheckStatus.WARN,
        message="No dependency management tool found (Dependabot, Renovate)",
        details=["No dependabot.yml, renovate.json, or .renovaterc found"],
        recommendations=["Add Dependabot: .github/dependabot.yml", "Or add Renovate: renovate.json"],
        rsqkit_url="https://everse.software/RSQKit/dependency_management",
        category="engineering",
    )


def check_containers(repo_path: str) -> CheckResult:
    """Check for containerization (Dockerfile, docker-compose)."""
    path = Path(repo_path)
    details: list[str] = []
    found: list[str] = []

    dockerfile = path / "Dockerfile"
    dockerfile_alt = path / "docker" / "Dockerfile"
    compose = path / "docker-compose.yml"
    compose_alt = path / "docker-compose.yaml"
    compose2 = path / "compose.yml"

    if dockerfile.exists():
        found.append("Dockerfile")
        details.append("Dockerfile found at root")
    elif dockerfile_alt.exists():
        found.append("Dockerfile")
        details.append("Dockerfile found in docker/")
    if any(p.exists() for p in [compose, compose_alt, compose2]):
        found.append("docker-compose")
        details.append("docker-compose file found")

    if found:
        return CheckResult(
            name="Containerization",
            status=CheckStatus.PASS,
            message=f"Container support: {', '.join(found)}",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/containerization",
            category="engineering",
        )
    return CheckResult(
        name="Containerization",
        status=CheckStatus.WARN,
        message="No containerization files found",
        details=["No Dockerfile or docker-compose found"],
        recommendations=["Add a Dockerfile for reproducible deployment"],
        rsqkit_url="https://everse.software/RSQKit/containerization",
        category="engineering",
    )


def check_workflow_files(repo_path: str) -> CheckResult:
    """Check for computational workflow files (Snakemake, Nextflow, CWL, Galaxy)."""
    path = Path(repo_path)
    found: list[str] = []
    details: list[str] = []

    workflow_patterns = [
        ("**/*.smk", "Snakemake"),
        ("**/Snakefile", "Snakemake"),
        ("**/*.nf", "Nextflow"),
        ("**/*.cwl", "Common Workflow Language"),
        ("**/*.ga", "Galaxy"),
        ("**/*.nf", "Nextflow"),
        ("**/*.dag", "DAGman"),
    ]

    for pattern, tool in workflow_patterns:
        matches = list(path.glob(pattern))
        if matches:
            found.append(tool)
            details.append(f"{tool}: {len(matches)} file(s)")

    if found:
        return CheckResult(
            name="Computational workflows",
            status=CheckStatus.PASS,
            message=f"Workflow files found: {', '.join(set(found))}",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/computational_workflows",
            category="engineering",
        )
    return CheckResult(
        name="Computational workflows",
        status=CheckStatus.NA,
        message="No computational workflow files found (may not be applicable)",
        details=["No .smk, .nf, .cwl, .ga files found"],
        rsqkit_url="https://everse.software/RSQKit/computational_workflows",
        category="engineering",
    )


def check_api_docs(repo_path: str) -> CheckResult:
    """Check for API documentation (OpenAPI/Swagger, auto-generated docs)."""
    path = Path(repo_path)
    found: list[str] = []
    details: list[str] = []

    api_files = [
        "openapi.yaml", "openapi.json",
        "swagger.yaml", "swagger.json",
        "openapi.yml",
    ]
    for f in api_files:
        if (path / f).exists():
            found.append(f)
            details.append(f"{f} found")

    docs_dirs = [path / "docs", path / "doc"]
    for d in docs_dirs:
        if d.is_dir():
            for p in d.iterdir():
                if p.name in ("api.md", "api.rst", "api.txt"):
                    found.append(str(p.relative_to(path)))
                    details.append(f"API docs: {p.relative_to(path)}")

    if found:
        return CheckResult(
            name="API documentation",
            status=CheckStatus.PASS,
            message=f"API documentation found: {', '.join(found)}",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/api_documentation",
            category="engineering",
        )
    return CheckResult(
        name="API documentation",
        status=CheckStatus.WARN,
        message="No API documentation found (OpenAPI/Swagger or docs/api)",
        details=["No openapi.yaml/json, swagger.yaml/json, or docs/api.md found"],
        recommendations=["Add API documentation (OpenAPI spec or docs/api.md)"],
        rsqkit_url="https://everse.software/RSQKit/api_documentation",
        category="engineering",
    )


def check_changelog(repo_path: str) -> CheckResult:
    """Check for CHANGELOG file."""
    path = Path(repo_path)
    changelog_files = ["CHANGELOG.md", "CHANGELOG.txt", "CHANGELOG", "CHANGES.md", "CHANGES"]

    for f in changelog_files:
        if (path / f).exists():
            content = (path / f).read_text(errors="ignore")
            has_entries = len([l for l in content.splitlines() if l.strip().startswith("##") or l.strip().startswith("-")]) > 0
            return CheckResult(
                name="Changelog",
                status=CheckStatus.PASS if has_entries else CheckStatus.WARN,
                message=f"Changelog found: {f}" + ("" if has_entries else " (but may be empty)"),
                details=[f"File: {f}", f"Has entries: {has_entries}"],
                rsqkit_url="https://everse.software/RSQKit/changelog",
                category="documentation",
            )

    return CheckResult(
        name="Changelog",
        status=CheckStatus.WARN,
        message="No changelog file found",
        details=["No CHANGELOG.md, CHANGES.md, or similar found"],
        recommendations=["Add a CHANGELOG.md to track version history"],
        rsqkit_url="https://everse.software/RSQKit/changelog",
        category="documentation",
    )


def check_contribution_guide(repo_path: str) -> CheckResult:
    """Check for CONTRIBUTING file."""
    path = Path(repo_path)
    for f in ["CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING.txt", ".github/CONTRIBUTING.md"]:
        if (path / f).exists():
            return CheckResult(
                name="Contribution guidelines",
                status=CheckStatus.PASS,
                message=f"Contribution guide found: {f}",
                details=[f"File: {f}"],
                rsqkit_url="https://everse.software/RSQKit/contribution_guidelines",
                category="documentation",
            )
    return CheckResult(
        name="Contribution guidelines",
        status=CheckStatus.WARN,
        message="No CONTRIBUTING.md found",
        details=["No CONTRIBUTING.md or .github/CONTRIBUTING.md found"],
        recommendations=["Add CONTRIBUTING.md with guidelines for contributors"],
        rsqkit_url="https://everse.software/RSQKit/contribution_guidelines",
        category="documentation",
    )


def check_code_of_conduct(repo_path: str) -> CheckResult:
    """Check for CODE_OF_CONDUCT file."""
    path = Path(repo_path)
    for f in ["CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.txt", ".github/CODE_OF_CONDUCT.md"]:
        if (path / f).exists():
            return CheckResult(
                name="Code of conduct",
                status=CheckStatus.PASS,
                message=f"Code of conduct found: {f}",
                details=[f"File: {f}"],
                rsqkit_url="https://everse.software/RSQKit/code_of_conduct",
                category="documentation",
            )
    return CheckResult(
        name="Code of conduct",
        status=CheckStatus.WARN,
        message="No CODE_OF_CONDUCT.md found",
        details=["No CODE_OF_CONDUCT.md found"],
        recommendations=["Add CODE_OF_CONDUCT.md (see Contributor Covenant)"],
        rsqkit_url="https://everse.software/RSQKit/code_of_conduct",
        category="documentation",
    )


def check_issue_templates(repo_path: str) -> CheckResult:
    """Check for issue templates."""
    path = Path(repo_path)
    template_dir = path / ".github" / "ISSUE_TEMPLATE"
    if template_dir.is_dir():
        templates = list(template_dir.glob("*.md")) + list(template_dir.glob("*.yml")) + list(template_dir.glob("*.yaml"))
        if templates:
            return CheckResult(
                name="Issue templates",
                status=CheckStatus.PASS,
                message=f"Issue templates found: {len(templates)}",
                details=[f"Templates: {', '.join(t.name for t in templates)}"],
                rsqkit_url="https://everse.software/RSQKit/issue_templates",
                category="documentation",
            )
    return CheckResult(
        name="Issue templates",
        status=CheckStatus.WARN,
        message="No issue templates found",
        details=["No .github/ISSUE_TEMPLATE/ directory or templates"],
        recommendations=["Add issue templates in .github/ISSUE_TEMPLATE/"],
        rsqkit_url="https://everse.software/RSQKit/issue_templates",
        category="documentation",
    )


def check_secret_management(repo_path: str) -> CheckResult:
    """Check for secret management practices (.env in .gitignore, pre-commit hooks)."""
    path = Path(repo_path)
    details: list[str] = []
    score = 0

    gitignore = path / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(errors="ignore").lower()
        if ".env" in content:
            score += 1
            details.append(".env in .gitignore")
        if "secret" in content or "credentials" in content:
            score += 1
            details.append("secrets/credentials in .gitignore")

    precommit = path / ".pre-commit-config.yaml"
    if precommit.exists():
        content = precommit.read_text(errors="ignore").lower()
        if "secrets" in content or "gitleaks" in content or "trufflehog" in content:
            score += 1
            details.append("Secret scanning in pre-commit hooks")

    if score >= 2:
        return CheckResult(
            name="Secret management",
            status=CheckStatus.PASS,
            message=f"Good secret management practices ({score} indicators)",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/secret_management",
            category="security",
        )
    elif score == 1:
        return CheckResult(
            name="Secret management",
            status=CheckStatus.WARN,
            message=f"Partial secret management ({score} indicator(s))",
            details=details,
            recommendations=["Add .env to .gitignore", "Add gitleaks to pre-commit hooks"],
            rsqkit_url="https://everse.software/RSQKit/secret_management",
            category="security",
        )
    return CheckResult(
        name="Secret management",
        status=CheckStatus.WARN,
        message="No secret management practices found",
        details=["No .env in .gitignore, no secret scanning hooks"],
        recommendations=["Add .env to .gitignore", "Add gitleaks pre-commit hook"],
        rsqkit_url="https://everse.software/RSQKit/secret_management",
        category="security",
    )


def check_data_management(repo_path: str) -> CheckResult:
    """Check for data management plan or data documentation."""
    path = Path(repo_path)
    dmp_files = ["DATA_MANAGEMENT_PLAN.md", "DMP.md", "data_management.md", "docs/dmp.md", "docs/DATA_MANAGEMENT_PLAN.md"]

    for f in dmp_files:
        if (path / f).exists():
            return CheckResult(
                name="Data management plan",
                status=CheckStatus.PASS,
                message=f"Data management plan found: {f}",
                details=[f"File: {f}"],
                rsqkit_url="https://everse.software/RSQKit/data_management",
                category="reproducibility",
            )

    data_dir = path / "data"
    if data_dir.is_dir():
        readme = data_dir / "README.md"
        if readme.exists():
            return CheckResult(
                name="Data management plan",
                status=CheckStatus.WARN,
                message="Data directory with README found (partial DMP)",
                details=["data/README.md found"],
                rsqkit_url="https://everse.software/RSQKit/data_management",
                category="reproducibility",
            )

    return CheckResult(
        name="Data management plan",
        status=CheckStatus.WARN,
        message="No data management plan found",
        details=["No DMP.md or DATA_MANAGEMENT_PLAN.md found"],
        recommendations=["Add a data management plan (DMP.md) if your software uses/produces data"],
        rsqkit_url="https://everse.software/RSQKit/data_management",
        category="reproducibility",
    )


def check_reproducibility_checklist(repo_path: str) -> CheckResult:
    """Check for reproducibility checklist or checklist file."""
    path = Path(repo_path)
    checklist_files = [
        "REPRODUCIBILITY.md", "reproducibility.md",
        "CHECKLIST.md", "checklist.md",
        "docs/reproducibility.md",
    ]

    for f in checklist_files:
        if (path / f).exists():
            return CheckResult(
                name="Reproducibility checklist",
                status=CheckStatus.PASS,
                message=f"Reproducibility checklist found: {f}",
                details=[f"File: {f}"],
                rsqkit_url="https://everse.software/RSQKit/reproducibility_checklist",
                category="reproducibility",
            )

    return CheckResult(
        name="Reproducibility checklist",
        status=CheckStatus.WARN,
        message="No reproducibility checklist found",
        details=["No REPRODUCIBILITY.md or CHECKLIST.md found"],
        recommendations=["Add a reproducibility checklist documenting how to reproduce results"],
        rsqkit_url="https://everse.software/RSQKit/reproducibility_checklist",
        category="reproducibility",
    )


def check_archiving(repo_path: str) -> CheckResult:
    """Check for software archiving indicators (Zenodo, Software Heritage)."""
    path = Path(repo_path)
    details: list[str] = []
    found: list[str] = []

    zenodo = path / ".zenodo.json"
    if zenodo.exists():
        found.append("Zenodo")
        details.append(".zenodo.json found")

    readme = path / "README.md"
    if readme.exists():
        content = readme.read_text(errors="ignore").lower()
        if "zenodo" in content or "doi.org" in content or "badge" in content:
            found.append("Zenodo DOI in README")
            details.append("Zenodo/DOI reference in README")
        if "softwareheritage.org" in content or "swh:" in content:
            found.append("Software Heritage")
            details.append("Software Heritage reference in README")

    if found:
        return CheckResult(
            name="Archiving",
            status=CheckStatus.PASS,
            message=f"Archiving indicators found: {', '.join(found)}",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/archiving_software",
            category="sustainability",
        )
    return CheckResult(
        name="Archiving",
        status=CheckStatus.WARN,
        message="No software archiving indicators found",
        details=["No .zenodo.json, no Zenodo DOI in README, no Software Heritage reference"],
        recommendations=["Create .zenodo.json", "Archive on Zenodo after first release"],
        rsqkit_url="https://everse.software/RSQKit/archiving_software",
        category="sustainability",
    )


def check_future_proofing(repo_path: str) -> CheckResult:
    """Check for future proofing indicators (dependency pinning, maintenance plan)."""
    path = Path(repo_path)
    details: list[str] = []
    score = 0

    lockfiles = ["uv.lock", "poetry.lock", "package-lock.json", "yarn.lock", "Cargo.lock", "Gemfile.lock", "go.sum", "renv.lock"]
    found_locks = [f for f in lockfiles if (path / f).exists()]
    if found_locks:
        score += 1
        details.append(f"Lockfiles: {', '.join(found_locks)}")

    gitignore = path / ".gitignore"
    if gitignore.exists():
        score += 1
        details.append(".gitignore present")

    tests_dir = path / "tests"
    if tests_dir.is_dir():
        score += 1
        details.append("Tests directory present")

    if score >= 3:
        return CheckResult(
            name="Future proofing",
            status=CheckStatus.PASS,
            message=f"Good future proofing ({score}/3 indicators)",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/future_proofing",
            category="sustainability",
        )
    elif score >= 1:
        return CheckResult(
            name="Future proofing",
            status=CheckStatus.WARN,
            message=f"Partial future proofing ({score}/3 indicators)",
            details=details,
            recommendations=["Add lockfiles for dependency pinning", "Add .gitignore", "Add tests"],
            rsqkit_url="https://everse.software/RSQKit/future_proofing",
            category="sustainability",
        )
    return CheckResult(
        name="Future proofing",
        status=CheckStatus.WARN,
        message="Limited future proofing indicators",
        details=details or ["No lockfiles, .gitignore, or tests found"],
        recommendations=["Add lockfiles, .gitignore, and tests"],
        rsqkit_url="https://everse.software/RSQKit/future_proofing",
        category="sustainability",
    )


def check_sustainability_plan(repo_path: str) -> CheckResult:
    """Check for software sustainability plan."""
    path = Path(repo_path)
    plan_files = [
        "SUSTAINABILITY.md", "sustainability_plan.md",
        "docs/sustainability.md", "SUSTAINABILITY_PLAN.md",
    ]

    for f in plan_files:
        if (path / f).exists():
            return CheckResult(
                name="Software sustainability plan",
                status=CheckStatus.PASS,
                message=f"Sustainability plan found: {f}",
                details=[f"File: {f}"],
                rsqkit_url="https://everse.software/RSQKit/software_sustainability_plan",
                category="sustainability",
            )
    return CheckResult(
        name="Software sustainability plan",
        status=CheckStatus.WARN,
        message="No sustainability plan found",
        details=["No SUSTAINABILITY.md or similar found"],
        recommendations=["Add a sustainability plan (SUSTAINABILITY.md)"],
        rsqkit_url="https://everse.software/RSQKit/software_sustainability_plan",
        category="sustainability",
    )


def check_env_sustainability(repo_path: str) -> CheckResult:
    """Check for environmental sustainability practices."""
    path = Path(repo_path)
    details: list[str] = []
    score = 0

    ci_files = list((path / ".github" / "workflows").glob("*.yml")) if (path / ".github" / "workflows").is_dir() else []
    for ci in ci_files:
        content = ci.read_text(errors="ignore").lower()
        if "cache" in content:
            score += 1
            details.append(f"CI caching in {ci.name}")

    dockerfile = path / "Dockerfile"
    if dockerfile.exists():
        content = dockerfile.read_text(errors="ignore").lower()
        if "multi-stage" in content or "as builder" in content or "as build" in content:
            score += 1
            details.append("Multi-stage Docker build (smaller images)")

    green_computing_files = ["GREEN_COMPUTING.md", ".github/green-software.yml"]
    for f in green_computing_files:
        if (path / f).exists():
            score += 1
            details.append(f"{f} found")

    if score >= 1:
        return CheckResult(
            name="Environmental sustainability",
            status=CheckStatus.PASS if score >= 2 else CheckStatus.WARN,
            message=f"Environmental practices: {score} indicator(s)",
            details=details,
            rsqkit_url="https://everse.software/RSQKit/improving_environmental_sustainability",
            category="sustainability",
        )
    return CheckResult(
        name="Environmental sustainability",
        status=CheckStatus.NA,
        message="No environmental sustainability indicators found (may not be applicable)",
        details=["No CI caching, multi-stage Docker, or green computing files"],
        rsqkit_url="https://everse.software/RSQKit/improving_environmental_sustainability",
        category="sustainability",
    )


def check_software_peer_review(repo_path: str) -> CheckResult:
    """Check for software peer review indicators (JOSS, rOpenSci, etc.)."""
    path = Path(repo_path)
    details: list[str] = []

    # Check for JOSS paper
    paper_dir = path / "paper"
    if paper_dir.is_dir():
        if any(paper_dir.glob("*.tex")) or any(paper_dir.glob("paper.md")):
            return CheckResult(
                name="Software peer review",
                status=CheckStatus.PASS,
                message="JOSS paper found (peer review indicator)",
                details=["paper/ directory with .tex or .md found"],
                rsqkit_url="https://everse.software/RSQKit/software_peer_review",
                category="quality",
            )

    # Check README for review badges
    readme = path / "README.md"
    if readme.exists():
        content = readme.read_text(errors="ignore").lower()
        if "joss" in content or "ropensci" in content or "peer-reviewed" in content:
            return CheckResult(
                name="Software peer review",
                status=CheckStatus.PASS,
                message="Peer review badge/reference found in README",
                details=["JOSS/rOpenSci/peer-reviewed reference in README"],
                rsqkit_url="https://everse.software/RSQKit/software_peer_review",
                category="quality",
            )

    return CheckResult(
        name="Software peer review",
        status=CheckStatus.NA,
        message="No peer review indicators found (optional practice)",
        details=["No JOSS paper, rOpenSci badge, or peer review reference"],
        rsqkit_url="https://everse.software/RSQKit/software_peer_review",
        category="quality",
    )


def check_quality_model(repo_path: str) -> CheckResult:
    """Check for software quality model adoption (ISO 25010, SQOCE, etc.)."""
    path = Path(repo_path)
    quality_files = [
        "QUALITY.md", "quality_model.md",
        "docs/quality.md", ".github/quality.yml",
    ]

    for f in quality_files:
        if (path / f).exists():
            return CheckResult(
                name="Software quality model",
                status=CheckStatus.PASS,
                message=f"Quality model documentation found: {f}",
                details=[f"File: {f}"],
                rsqkit_url="https://everse.software/RSQKit/software_quality_models",
                category="quality",
            )

    # Check for quality badges in README
    readme = path / "README.md"
    if readme.exists():
        content = readme.read_text(errors="ignore").lower()
        if any(q in content for q in ["iso 25010", "sqoce", "quality model", "quality badge"]):
            return CheckResult(
                name="Software quality model",
                status=CheckStatus.PASS,
                message="Quality model reference found in README",
                details=["Quality model reference in README"],
                rsqkit_url="https://everse.software/RSQKit/software_quality_models",
                category="quality",
            )

    return CheckResult(
        name="Software quality model",
        status=CheckStatus.NA,
        message="No software quality model adoption found (optional)",
        details=["No QUALITY.md or quality model references"],
        rsqkit_url="https://everse.software/RSQKit/software_quality_models",
        category="quality",
    )
