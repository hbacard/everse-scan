"""CLI entry point for everse-scan."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from everse_scan import __version__
from everse_scan.scanner import scan_repo
from everse_scan.reporters.json import generate_json
from everse_scan.reporters.markdown import generate_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="everse-scan",
        description="Scan a research software repository for EVERSE/RSQKit compliance.",
    )
    parser.add_argument(
        "repo",
        help="Path to the repository to scan (local path or GitHub URL)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout for json, everse-scan-report.md for markdown)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"everse-scan {__version__}",
    )

    args = parser.parse_args(argv)

    repo_path = args.repo

    # Handle GitHub URLs
    if repo_path.startswith("https://github.com/") or repo_path.startswith("git@github.com:"):
        import subprocess
        import tempfile
        repo_name = repo_path.rstrip("/").split("/")[-1].replace(".git", "")
        tmp_dir = tempfile.mkdtemp(prefix="everse-scan-")
        clone_path = str(Path(tmp_dir) / repo_name)
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_path, clone_path],
                check=True,
                capture_output=True,
                timeout=60,
            )
            result = scan_repo(clone_path)
        finally:
            import shutil
            shutil.rmtree(tmp_dir, ignore_errors=True)
    else:
        if not Path(repo_path).exists():
            print(f"Error: repository path '{repo_path}' does not exist", file=sys.stderr)
            return 1
        result = scan_repo(repo_path)

    # Generate output
    if args.format == "json":
        output = generate_json(result)
        if args.output:
            Path(args.output).write_text(output)
            print(f"Report saved to {args.output}", file=sys.stderr)
        else:
            print(output)
    elif args.format == "markdown":
        output = generate_markdown(result)
        output_path = args.output or "everse-scan-report.md"
        Path(output_path).write_text(output)
        print(f"Report saved to {output_path}", file=sys.stderr)
        print(f"\nSummary: {result.passed}/{result.total} passed, "
              f"{result.warned} warned, {result.failed} failed", file=sys.stderr)
    elif args.format == "both":
        json_output = generate_json(result)
        md_output = generate_markdown(result)
        json_path = args.output or "everse-scan-report.json"
        md_path = str(Path(json_path).with_suffix(".md"))
        Path(json_path).write_text(json_output)
        Path(md_path).write_text(md_output)
        print(f"JSON report saved to {json_path}", file=sys.stderr)
        print(f"Markdown report saved to {md_path}", file=sys.stderr)
        print(f"\nSummary: {result.passed}/{result.total} passed, "
              f"{result.warned} warned, {result.failed} failed", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
