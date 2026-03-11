from __future__ import annotations

import json
from pathlib import Path

from .models import Project


def load_projects(path: str | Path) -> list[Project]:
    data = json.loads(Path(path).read_text())
    projects: list[Project] = []
    for item in data["projects"]:
        projects.append(
            Project(
                name=item["name"],
                repo=item.get("repo"),
                homepage=item.get("homepage"),
                description=item.get("description", ""),
                tags=item.get("tags", []),
                milestones=item.get("milestones", []),
            )
        )
    return projects
