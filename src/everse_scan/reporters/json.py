"""JSON reporter for everse-scan."""

from __future__ import annotations

import json

from everse_scan.models import ScanResult


def generate_json(result: ScanResult) -> str:
    """Generate a JSON report from scan results."""
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
