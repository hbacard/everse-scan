"""Data models for everse-scan."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CheckStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    NA = "na"


@dataclass
class AIIntensityProfile:
    """Self-determined AI intensity profile (from ai-intensity.yaml).

    This is NOT an evaluation — it is a self-determination by the project's
    users via the AI Intensity Q&A skill. everse-scan reads it neutrally.
    See: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
    """

    found: bool = False
    current: int | None = None
    desired: int | None = None
    authorized: int | None = None
    sustainable: int | None = None
    current_usage: str = ""
    desired_intensity: str = ""
    authorized_intensity: str = ""
    review_capacity: str = ""
    determined_by: str = ""
    date: str = ""

    def to_dict(self) -> dict:
        return {
            "found": self.found,
            "current": self.current,
            "desired": self.desired,
            "authorized": self.authorized,
            "sustainable": self.sustainable,
            "current_usage": self.current_usage,
            "desired_intensity": self.desired_intensity,
            "authorized_intensity": self.authorized_intensity,
            "review_capacity": self.review_capacity,
            "determined_by": self.determined_by,
            "date": self.date,
        }


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
    primary_language: str | None = None
    tier: str = ""
    tier_justification: str = ""
    tier_checks_adjusted: list[str] = field(default_factory=list)
    lifecycle: str = ""
    lifecycle_justification: str = ""
    ai_intensity_profile: AIIntensityProfile = field(default_factory=AIIntensityProfile)
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
            "ai_intensity_profile": self.ai_intensity_profile.to_dict(),
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
