from __future__ import annotations

import json
from pathlib import Path

from .analyzer import project_report_to_dict
from .models import ProjectReport


def write_json(reports: list[ProjectReport], path: str | Path) -> None:
    payload = {"reports": [project_report_to_dict(report) for report in reports]}
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def write_markdown(reports: list[ProjectReport], path: str | Path) -> None:
    lines: list[str] = []
    lines.append("# GCC Impact Copilot Report")
    lines.append("")
    lines.append("Reviewer-facing public evidence checks for grant portfolio projects.")
    lines.append("")
    for report in sorted(reports, key=lambda item: item.score, reverse=True):
        lines.append(f"## {report.project.name}")
        lines.append("")
        lines.append(f"- Status: **{report.status}**")
        lines.append(f"- Score: **{report.score} / 100**")
        if report.project.repo:
            lines.append(f"- Repo: `{report.project.repo}`")
        if report.project.homepage:
            lines.append(f"- Homepage: {report.project.homepage}")
        lines.append(f"- Summary: {report.summary}")
        lines.append("")
        lines.append("### Signals")
        lines.append("")
        for signal in report.signals:
            lines.append(f"- `{signal.kind}` = **{signal.value}** — {signal.note}")
            lines.append(f"  - Why it matters: {signal.rationale}")
            for evidence in signal.evidence_refs:
                lines.append(
                    f"  - Evidence: `{evidence.label}` from **{evidence.source}** → `{evidence.ref}` ({evidence.note})"
                )
        if report.milestone_assessments:
            lines.append("")
            lines.append("### Milestone Mapping")
            lines.append("")
            for item in report.milestone_assessments:
                lines.append(f"- `{item.milestone}` → **{item.status}**")
                lines.append(f"  - Rationale: {item.rationale}")
                for evidence in item.evidence_refs:
                    lines.append(
                        f"  - Evidence: `{evidence.label}` from **{evidence.source}** → `{evidence.ref}` ({evidence.note})"
                    )
        if report.risks:
            lines.append("")
            lines.append("### Risks / Follow-ups")
            lines.append("")
            for risk in report.risks:
                lines.append(f"- **{risk.level}** — {risk.message}")
                lines.append(f"  - Why flagged: {risk.rationale}")
                for evidence in risk.evidence_refs:
                    lines.append(
                        f"  - Evidence: `{evidence.label}` from **{evidence.source}** → `{evidence.ref}` ({evidence.note})"
                    )
        lines.append("")
    Path(path).write_text("\n".join(lines).rstrip() + "\n")
