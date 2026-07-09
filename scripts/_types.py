from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CheckResult:
    passed: bool
    detail: str
    count: int | None = None


@dataclass
class Report:
    passed: bool
    prompt: str
    tag_count: int
    checks: dict[str, CheckResult]
