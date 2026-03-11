from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import asdict
from typing import Any

from .github_api import iso_to_days, parse_repo, safe_get_json
from .models import Project, ProjectReport, Signal


STATUS_BANDS = [
    (75, "healthy"),
    (45, "watch"),
    (0, "at-risk"),
]


def _url_ok(url: str | None) -> tuple[bool, str]:
    if not url:
        return False, "No public homepage provided"
    request = urllib.request.Request(url, headers={"User-Agent": "gcc-impact-copilot"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return 200 <= response.status < 400, f"Homepage returned HTTP {response.status}"
    except urllib.error.URLError as error:
        return False, f"Homepage check failed: {error.reason}"


def _status(score: int) -> str:
    for threshold, label in STATUS_BANDS:
        if score >= threshold:
            return label
    return "at-risk"


def _score_signal(kind: str, value: Any) -> int:
    if kind == "push_days":
        if value <= 14:
            return 24
        if value <= 30:
            return 16
        if value <= 90:
            return 8
        return 0
    if kind == "release_days":
        if value <= 30:
            return 15
        if value <= 90:
            return 10
        if value <= 180:
            return 4
        return 0
    if kind == "open_issues":
        if value <= 20:
            return 10
        if value <= 60:
            return 6
        return 3
    if kind == "stars":
        if value >= 1000:
            return 10
        if value >= 100:
            return 7
        if value >= 10:
            return 4
        return 1
    if kind == "homepage_ok":
        return 6 if value else 0
    if kind == "milestone_count":
        return min(value * 4, 12)
    return 0


def analyze_project(project: Project) -> ProjectReport:
    signals: list[Signal] = []
    risks: list[str] = []
    score = 0

    homepage_ok, homepage_note = _url_ok(project.homepage)
    signals.append(Signal("homepage_ok", homepage_ok, homepage_note))
    score += _score_signal("homepage_ok", homepage_ok)

    signals.append(
        Signal(
            "milestone_count",
            len(project.milestones),
            f"{len(project.milestones)} declared milestones in config",
        )
    )
    score += _score_signal("milestone_count", len(project.milestones))

    if project.repo:
        owner, repo_name = parse_repo(project.repo)
        repo_data, repo_error = safe_get_json(f"/repos/{owner}/{repo_name}")
        if repo_error:
            risks.append(repo_error)
        else:
            push_days = iso_to_days(repo_data["pushed_at"])
            signals.append(Signal("push_days", push_days, f"Last push {push_days} days ago"))
            score += _score_signal("push_days", push_days)

            stars = repo_data["stargazers_count"]
            signals.append(Signal("stars", stars, f"GitHub stars: {stars}"))
            score += _score_signal("stars", stars)

            open_issues = repo_data["open_issues_count"]
            signals.append(Signal("open_issues", open_issues, f"Open issues: {open_issues}"))
            score += _score_signal("open_issues", open_issues)

            releases, release_error = safe_get_json(f"/repos/{owner}/{repo_name}/releases?per_page=1")
            if release_error:
                risks.append(release_error)
            elif releases:
                release_days = iso_to_days(releases[0]["published_at"])
                signals.append(
                    Signal("release_days", release_days, f"Latest release {release_days} days ago")
                )
                score += _score_signal("release_days", release_days)
            else:
                risks.append("No GitHub releases found")
    else:
        risks.append("No GitHub repository linked")

    status = _status(score)

    if status == "healthy":
        summary = f"{project.name} shows strong public activity signals and looks healthy."
    elif status == "watch":
        summary = f"{project.name} has mixed signals and should stay on the watchlist."
    else:
        summary = f"{project.name} has weak public signals and likely needs follow-up."

    if not homepage_ok:
        risks.append("Homepage is missing or unavailable")

    return ProjectReport(
        project=project,
        score=score,
        status=status,
        signals=signals,
        risks=risks,
        summary=summary,
    )


def project_report_to_dict(report: ProjectReport) -> dict[str, Any]:
    data = asdict(report)
    data["signals"] = [asdict(signal) for signal in report.signals]
    return data
