"""Data models for everse-scan."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class CheckStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    NA = "na"


@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    message: str
    details: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    rsqkit_url: str = ""
    category: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "recommendations": self.recommendations,
            "rsqkit_url": self.rsqkit_url,
            "category": self.category,
        }


@dataclass
class ScanResult:
    repo_path: str
    repo_name: str
    date: str
    languages: list[str] = field(default_factory=list)
    primary_language: Optional[str] = None
    tier: str = ""
    tier_justification: str = ""
    tier_checks_adjusted: list[str] = field(default_factory=list)
    lifecycle: str = ""
    lifecycle_justification: str = ""
    ai_intensity: int = 0
    ai_indicators: list[str] = field(default_factory=list)
    funder: str = ""
    funder_label: str = ""
    funder_grant_ids: list[str] = field(default_factory=list)
    funder_confidence: str = "low"
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for c in self.checks if c.status == CheckStatus.PASS)

    @property
    def warned(self) -> int:
        return sum(1 for c in self.checks if c.status == CheckStatus.WARN)

    @property
    def failed(self) -> int:
        return sum(1 for c in self.checks if c.status == CheckStatus.FAIL)

    @property
    def total(self) -> int:
        return len(self.checks)

    def to_dict(self) -> dict:
        return {
            "repo_path": self.repo_path,
            "repo_name": self.repo_name,
            "date": self.date,
            "languages": self.languages,
            "primary_language": self.primary_language,
            "tier": self.tier,
            "tier_justification": self.tier_justification,
            "tier_checks_adjusted": self.tier_checks_adjusted,
            "lifecycle": self.lifecycle,
            "lifecycle_justification": self.lifecycle_justification,
            "ai_intensity": self.ai_intensity,
            "ai_indicators": self.ai_indicators,
            "funder": self.funder,
            "funder_label": self.funder_label,
            "funder_grant_ids": self.funder_grant_ids,
            "funder_confidence": self.funder_confidence,
            "summary": {
                "total": self.total,
                "passed": self.passed,
                "warned": self.warned,
                "failed": self.failed,
            },
            "checks": [c.to_dict() for c in self.checks],
        }
