"""Check: Reproducible environments (lockfiles, containers)."""

from __future__ import annotations

from pathlib import Path

from everse_scan.models import CheckResult, CheckStatus

LOCKFILES = {
    "uv.lock": ("uv", "Python"),
    "poetry.lock": ("poetry", "Python"),
    "requirements.txt": ("pip", "Python"),
    "Pipfile.lock": ("pipenv", "Python"),
    "package-lock.json": ("npm", "JavaScript/TypeScript"),
    "yarn.lock": ("yarn", "JavaScript/TypeScript"),
    "pnpm-lock.yaml": ("pnpm", "JavaScript/TypeScript"),
    "Cargo.lock": ("cargo", "Rust"),
    "go.sum": ("go", "Go"),
    "renv.lock": ("renv", "R"),
    "Manifest.toml": ("Pkg", "Julia"),
    "Gemfile.lock": ("bundler", "Ruby"),
}

CONTAINER_FILES = {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}


def _is_pinned_requirements(path: Path) -> bool:
    """Check if requirements.txt has pinned versions."""
    content = path.read_text(errors="ignore")
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]
    if not lines:
        return False
    pinned = sum(1 for l in lines if "==" in l)
    return pinned >= len(lines) * 0.5


def check_reproducible_envs(repo_path: str, language: str | None = None) -> CheckResult:
    path = Path(repo_path)

    found_lockfiles: list[str] = []
    lockfile_tools: list[str] = []
    found_containers: list[str] = []

    for fname, (tool, lang) in LOCKFILES.items():
        fpath = path / fname
        if fpath.exists():
            found_lockfiles.append(fname)
            lockfile_tools.append(tool)

    for cname in CONTAINER_FILES:
        if (path / cname).exists():
            found_containers.append(cname)

    # Check if requirements.txt is pinned
    req_path = path / "requirements.txt"
    requirements_pinned = False
    if req_path.exists():
        requirements_pinned = _is_pinned_requirements(req_path)
        if "requirements.txt" not in found_lockfiles:
            found_lockfiles.append("requirements.txt")
            lockfile_tools.append("pip")

    has_nix = (path / "flake.nix").exists() or (path / "shell.nix").exists()
    if has_nix:
        found_lockfiles.append("flake.nix / shell.nix")
        lockfile_tools.append("nix")

    details = [
        f"Lockfiles: {', '.join(found_lockfiles) if found_lockfiles else 'none'}",
        f"Container files: {', '.join(found_containers) if found_containers else 'none'}",
        f"Nix: {'yes' if has_nix else 'no'}",
    ]
    if req_path.exists():
        details.append(f"requirements.txt pinned: {'yes' if requirements_pinned else 'no'}")

    if found_lockfiles or found_containers or has_nix:
        score = sum([bool(found_lockfiles), bool(found_containers), has_nix,
                     requirements_pinned or "uv.lock" in found_lockfiles or "poetry.lock" in found_lockfiles])
        if score >= 2:
            status = CheckStatus.PASS
            msg = f"Reproducible environment configured ({', '.join(found_lockfiles + found_containers)})"
        else:
            status = CheckStatus.WARN
            msg = f"Partial reproducible environment ({', '.join(found_lockfiles + found_containers)})"
        recs = []
        if req_path.exists() and not requirements_pinned:
            recs.append("Pin dependencies in requirements.txt (use == instead of >=)")
    else:
        status = CheckStatus.WARN
        msg = "No lockfile or container configuration found"
        recs = [
            "Add a lockfile for reproducible installs (uv.lock for Python, package-lock.json for JS)",
            "Or use a Dockerfile / Nix flake for full environment reproducibility",
        ]

    return CheckResult(
        name="Reproducible environments",
        status=status,
        message=msg,
        details=details,
        recommendations=recs if 'recs' in dir() else [],
        rsqkit_url="https://everse.software/RSQKit/reproducible_software_environments",
        category="quality",
    )
