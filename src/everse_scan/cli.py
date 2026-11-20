"""CLI entry point for everse-scan."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from everse_scan import __version__
from everse_scan.reporters.adaptive import ROLES, generate_adaptive_markdown
from everse_scan.reporters.diff import (
    generate_diff_markdown,
    load_baseline,
    save_baseline,
)
from everse_scan.reporters.json import generate_json
from everse_scan.scanner import scan_repo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="everse-scan",
        description="Scan a research software repository for EVERSE/RSQKit compliance.",
    )
    parser.add_argument(
        "repo",
        help="Path to the repository to scan (local path or git URL)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout for json, everse-scan-report.md for markdown)",
    )
    parser.add_argument(
        "--role",
        choices=ROLES,
        default="default",
        help="Adapt report tone and priorities to a role (default: balanced)",
    )
    parser.add_argument(
        "--save",
        metavar="BASELINE_FILE",
        help="Save the scan result as a baseline JSON file for later comparison",
    )
    parser.add_argument(
        "--diff",
        metavar="BASELINE_FILE",
        help="Compare current scan with a previously saved baseline and show progress",
    )
    parser.add_argument(
        "--use",
        nargs="*",
        default=None,
        metavar="INTEGRATION",
        help="Enable external integrations (howfairis, cffconvert, codemeta). Use without args for all.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"everse-scan {__version__}",
    )

    args = parser.parse_args(argv)

    repo_path = args.repo

    # Handle remote git URLs (GitHub, GitLab, self-hosted, etc.)
    if "://" in repo_path or repo_path.startswith("git@"):
        import subprocess
        import tempfile

        repo_name = repo_path.rstrip("/").split("/")[-1].replace(".git", "")
        tmp_dir = tempfile.mkdtemp(prefix="everse-scan-")
        clone_path = str(Path(tmp_dir) / repo_name)
        try:
            subprocess.run(
                ["git", "clone", repo_path, clone_path],
                check=True,
                capture_output=True,
                timeout=60,
            )
            result = scan_repo(clone_path, use_integrations=args.use is not None)
        finally:
            import shutil

            shutil.rmtree(tmp_dir, ignore_errors=True)
    else:
        if not Path(repo_path).exists():
            print(f"Error: repository path '{repo_path}' does not exist", file=sys.stderr)
            return 1
        result = scan_repo(repo_path, use_integrations=args.use is not None)

    # Save baseline if requested
    if args.save:
        save_baseline(result, args.save)
        print(f"Baseline saved to {args.save}", file=sys.stderr)

    # Diff mode: compare with baseline and show progress report
    if args.diff:
        if not Path(args.diff).exists():
            print(f"Error: baseline file '{args.diff}' not found", file=sys.stderr)
            return 1
        baseline = load_baseline(args.diff)
        diff_output = generate_diff_markdown(baseline, result)

        # In diff mode, also save the current scan as new baseline if --save is also given
        # Otherwise just output the diff
        if args.output:
            Path(args.output).write_text(diff_output)
            print(f"Diff report saved to {args.output}", file=sys.stderr)
        else:
            print(diff_output)

        delta = result.passed - baseline.get("summary", {}).get("passed", 0)
        print(
            f"\nProgress: {result.passed}/{result.total} "
            f"(was {baseline.get('summary', {}).get('passed', 0)}/{baseline.get('summary', {}).get('total', 0)}), "
            f"delta {delta:+d}",
            file=sys.stderr,
        )
        return 0

    # Generate output
    if args.format == "json":
        output = generate_json(result)
        if args.output:
            Path(args.output).write_text(output)
            print(f"Report saved to {args.output}", file=sys.stderr)
        else:
            print(output)
    elif args.format == "markdown":
        output = generate_adaptive_markdown(result, args.role)
        output_path = args.output or "everse-scan-report.md"
        Path(output_path).write_text(output)
        print(f"Report saved to {output_path}", file=sys.stderr)
        print(
            f"\nSummary: {result.passed}/{result.total} passed, {result.warned} warned, {result.failed} failed",
            file=sys.stderr,
        )
    elif args.format == "both":
        json_output = generate_json(result)
        md_output = generate_adaptive_markdown(result, args.role)
        json_path = args.output or "everse-scan-report.json"
        md_path = str(Path(json_path).with_suffix(".md"))
        Path(json_path).write_text(json_output)
        Path(md_path).write_text(md_output)
        print(f"JSON report saved to {json_path}", file=sys.stderr)
        print(f"Markdown report saved to {md_path}", file=sys.stderr)
        print(
            f"\nSummary: {result.passed}/{result.total} passed, {result.warned} warned, {result.failed} failed",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
