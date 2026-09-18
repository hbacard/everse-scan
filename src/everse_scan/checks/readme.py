"""Check: README presence and quality."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus


def check_readme(repo_path: str) -> CheckResult:
    path = Path(repo_path)
    readme_md = path / "README.md"
    readme_rst = path / "README.rst"

    readme_file = readme_md if readme_md.exists() else (readme_rst if readme_rst.exists() else None)

    if not readme_file:
        return CheckResult(
            name="README",
            status=CheckStatus.FAIL,
            message="No README.md or README.rst found at repository root",
            rsqkit_url="https://everse.software/RSQKit/creating_good_readme",
            category="documentation",
            recommendations=[
                "Create a README.md with: project name, description, installation, usage, license",
            ],
        )

    content = readme_file.read_text(errors="ignore").strip()
    has_description = len(content) > 100
    has_installation = any(w in content.lower() for w in ["install", "setup", "getting started", "prerequisite"])
    has_usage = any(w in content.lower() for w in ["usage", "example", "how to use", "quickstart"])
    has_license = any(w in content.lower() for w in ["license", "licence", "mit", "apache", "gpl", "bsd"])
    has_badges = "![[" in content or "badge" in content.lower()

    details = []
    if has_description:
        details.append("Description present")
    else:
        details.append("Description too short or missing")
    if has_installation:
        details.append("Installation instructions present")
    else:
        details.append("Installation instructions missing")
    if has_usage:
        details.append("Usage examples present")
    else:
        details.append("Usage examples missing")
    if has_license:
        details.append("License mentioned")
    else:
        details.append("License not mentioned")
    if has_badges:
        details.append("Badges present")
    else:
        details.append("No badges found")

    score = sum([has_description, has_installation, has_usage, has_license])

    if score >= 4:
        status = CheckStatus.PASS
    elif score >= 2:
        status = CheckStatus.WARN
    else:
        status = CheckStatus.FAIL

    recs = []
    if not has_installation:
        recs.append("Add an 'Installation' section")
    if not has_usage:
        recs.append("Add a 'Usage' section with examples")
    if not has_license:
        recs.append("Mention the license in the README")
    if not has_badges:
        recs.append("Consider adding badges (CI, license, coverage)")

    return CheckResult(
        name="README",
        status=status,
        message=f"README found: {readme_file.name}, quality score {score}/4",
        details=details,
        recommendations=recs,
        rsqkit_url="https://everse.software/RSQKit/creating_good_readme",
        category="documentation",
    )
