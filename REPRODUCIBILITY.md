# Reproducibility Checklist

This document explains how to reproduce an `everse-scan` run and its output
report. Following these steps should yield the same scan results for a given
commit of a target repository and a given version of `everse-scan` (1.0.0).

## 1. Environment

- **Python**: 3.12 or 3.13
- **Package**: `everse-scan` pinned by version (see `pyproject.toml`, `uv.lock`)
- **Dependencies**: declared in `pyproject.toml`; exact versions in `uv.lock` /
  `pdm.lock`

Pin the tool version and recreate the environment exactly:

```bash
# With uv
uv pip install -e ".[dev]" --exact  # resolves from uv.lock

# With pdm
pdm install -d --frozen
```

<details>
<summary>Container (fully pinned runtime)</summary>

```bash
docker build -t everse-scan:0.5.0 .
docker run --rm -v "$PWD:/work" everse-scan:0.5.0 . --format both -o report
```

</details>

## 2. Inputs

- The target repository at a **specific commit/tag**: record the git SHA with
  the report for later comparison.
- For remote scans, the exact URL (a clone is made at scan time — note the
  date, as remote repositories can change).

## 3. Scan commands

```bash
# Reproducible report for a local repository
everse-scan ./my-repo --format both -o report

# JSON only (machine-readable, best for diffing)
everse-scan ./my-repo --format json -o scan
```

## 4. Expected outputs

- `report.md` / `report.json` — the full scan report (deterministic checks).
- Checks with `--use` (howfairis, cffconvert, codemeta validator) depend on
  those external tools' versions — record them if you enable integrations.
- Report header records the repository, date, and detected tier/lifecycle.

## 5. Verification

1. Re-run the scan on the **same commit** with the **same version** of
   `everse-scan`.
2. Compare the JSON output: `everse-scan` results should be identical
   (`git diff` or `diff`).
3. Use the built-in diff to track change over time:

   ```bash
   everse-scan ./my-repo --save baseline.json --format json
   # ... make changes to the repository ...
   everse-scan ./my-repo --diff baseline.json
   ```

## Checklist

- [ ] Python version recorded (3.12/3.13)
- [ ] `everse-scan` version recorded (`--version`)
- [ ] Target repository commit/tag recorded
- [ ] Lockfile used (uv.lock / pdm.lock)
- [ ] Scan command and CLI options recorded
- [ ] Output saved to a file (`-o report`)
- [ ] JSON output retained for machine comparison
- [ ] External integrations (`--use`) documented if enabled
