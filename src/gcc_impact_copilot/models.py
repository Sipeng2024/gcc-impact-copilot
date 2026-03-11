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
class Signal:
    kind: str
    value: Any
    note: str


@dataclass(slots=True)
class ProjectReport:
    project: Project
    score: int
    status: str
    signals: list[Signal]
    risks: list[str]
    summary: str
