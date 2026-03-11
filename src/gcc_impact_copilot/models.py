from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Project:
    name: str
    repo: str | None = None
    homepage: str | None = None
    description: str = ""
    tags: list[str] = field(default_factory=list)
    milestones: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceRef:
    label: str
    source: str
    ref: str
    note: str


@dataclass(slots=True)
class Signal:
    kind: str
    value: Any
    note: str
    rationale: str
    evidence_refs: list[EvidenceRef] = field(default_factory=list)


@dataclass(slots=True)
class MilestoneAssessment:
    milestone: str
    status: str
    rationale: str
    evidence_refs: list[EvidenceRef] = field(default_factory=list)


@dataclass(slots=True)
class Risk:
    level: str
    message: str
    rationale: str
    evidence_refs: list[EvidenceRef] = field(default_factory=list)


@dataclass(slots=True)
class ProjectReport:
    project: Project
    score: int
    status: str
    signals: list[Signal]
    milestone_assessments: list[MilestoneAssessment]
    risks: list[Risk]
    summary: str
