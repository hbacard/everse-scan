"""Test fixtures: sample repo structures."""

import subprocess
from pathlib import Path


def create_sample_repo(base: Path, name: str = "sample-python") -> Path:
    """Create a sample Python repo with good practices for testing."""
    repo = base / name
    repo.mkdir(parents=True, exist_ok=True)

    # Init git
    subprocess.run(["git", "init"],check=False, cwd=str(repo), capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"],check=False, cwd=str(repo), capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"],check=False, cwd=str(repo), capture_output=True)

    # README.md
    (repo / "README.md").write_text(
        "# Sample Python Project\n\n"
        "A sample project for testing everse-scan.\n\n"
        "## Installation\n\n```\npip install sample\n```\n\n"
        "## Usage\n\n```\npython -m sample\n```\n\n"
        "## License\n\nMIT\n"
    )

    # LICENSE
    (repo / "LICENSE").write_text(
        "MIT License\n\n"
        "Copyright (c) 2024 Test User\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy "
        'of this software and associated documentation files (the "Software"), to deal '
        "in the Software without restriction, including without limitation the rights "
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
        "copies of the Software, and to permit persons to whom the Software is "
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all "
        "copies or substantial portions of the Software.\n\n"
        'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.'
    )

    # CITATION.cff
    (repo / "CITATION.cff").write_text(
        "cff-version: 1.2.0\n"
        "title: Sample Python Project\n"
        "message: Please cite this software\n"
        "authors:\n"
        "  - family-names: User\n"
        "    given-names: Test\n"
        "date-released: 2024-01-01\n"
        "version: 0.1.0\n"
    )

    # pyproject.toml
    (repo / "pyproject.toml").write_text(
        "[build-system]\n"
        'requires = ["hatchling"]\n'
        'build-backend = "hatchling.build"\n\n'
        "[project]\n"
        'name = "sample"\n'
        'version = "0.1.0"\n'
        'description = "A sample project"\n'
        'license = {text = "MIT"}\n\n'
        "[tool.ruff]\n"
        "line-length = 88\n\n"
        "[tool.pytest.ini_options]\n"
        'testpaths = ["tests"]\n'
    )

    # src layout
    src_pkg = repo / "src" / "sample"
    src_pkg.mkdir(parents=True, exist_ok=True)
    (src_pkg / "__init__.py").write_text('"""Sample package."""\n__version__ = "0.1.0"\n')
    (src_pkg / "main.py").write_text(
        '"""Main module."""\n\n\ndef hello():\n    """Return greeting."""\n    return "Hello, World!"\n'
    )

    # tests
    tests_dir = repo / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("")
    (tests_dir / "test_main.py").write_text(
        '"""Tests for main module."""\n'
        "from sample.main import hello\n\n\n"
        "def test_hello():\n"
        '    """Test hello function."""\n'
        '    assert hello() == "Hello, World!"\n'
    )

    # docs
    docs_dir = repo / "docs"
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "index.md").write_text("# Documentation\n\nSample docs.\n")
    (docs_dir / "guide.md").write_text("# Guide\n\nUsage guide.\n")

    # .gitignore
    (repo / ".gitignore").write_text("__pycache__/\n*.pyc\n.venv/\nvenv/\nnode_modules/\ndist/\nbuild/\n.env\n")

    # CI
    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    (workflows / "test.yml").write_text(
        "name: Tests\n"
        "on: [push, pull_request]\n"
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    strategy:\n"
        "      matrix:\n"
        "        python-version: ['3.11', '3.12', '3.13']\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: actions/setup-python@v5\n"
        "      - run: pip install -e .[dev]\n"
        "      - run: ruff check .\n"
        "      - run: pytest\n"
    )

    # CHANGELOG
    (repo / "CHANGELOG.md").write_text("# Changelog\n\n## 0.1.0\n\n- Initial release\n")

    # Commit
    subprocess.run(["git", "add", "-A"], check=False, cwd=str(repo), capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=False, cwd=str(repo), capture_output=True)
    subprocess.run(["git", "tag", "v0.1.0"], check=False, cwd=str(repo), capture_output=True)

    return repo


def create_minimal_repo(base: Path, name: str = "minimal") -> Path:
    """Create a minimal repo with almost nothing for testing failures."""
    repo = base / name
    repo.mkdir(parents=True, exist_ok=True)

    # Just a single Python file, no git, no config
    (repo / "script.py").write_text("print('hello')\n")

    return repo
