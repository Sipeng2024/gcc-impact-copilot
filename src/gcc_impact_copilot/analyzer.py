from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import asdict
from typing import Any

from .github_api import iso_to_days, parse_repo, safe_get_json
from .models import EvidenceRef, MilestoneAssessment, Project, ProjectReport, Risk, Signal


STATUS_BANDS = [
    (75, "healthy"),
    (45, "watch"),
    (0, "at-risk"),
]


def _url_ok(url: str | None) -> tuple[bool, str, int | None]:
    if not url:
        return False, "No public homepage provided", None
    request = urllib.request.Request(url, headers={"User-Agent": "gcc-impact-copilot"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return 200 <= response.status < 400, f"Homepage returned HTTP {response.status}", response.status
    except urllib.error.URLError as error:
        return False, f"Homepage check failed: {error.reason}", None


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


def _repo_ref(project: Project, suffix: str = "") -> EvidenceRef:
    repo = project.repo or "unknown"
    return EvidenceRef(
        label="github_repo",
        source="github",
        ref=f"{repo}{suffix}",
        note="GitHub repository reference",
    )


def _homepage_ref(project: Project, note: str) -> EvidenceRef:
    return EvidenceRef(
        label="homepage",
        source="web",
        ref=project.homepage or "missing",
        note=note,
    )


def analyze_project(project: Project) -> ProjectReport:
    signals: list[Signal] = []
    milestone_assessments: list[MilestoneAssessment] = []
    risks: list[Risk] = []
    score = 0

    homepage_ok, homepage_note, homepage_status = _url_ok(project.homepage)
    homepage_ref = _homepage_ref(project, homepage_note)
    signals.append(
        Signal(
            kind="homepage_ok",
            value=homepage_ok,
            note=homepage_note,
            rationale="Homepage reachability is a minimal public evidence check for whether reviewers can inspect project materials.",
            evidence_refs=[homepage_ref],
        )
    )
    score += _score_signal("homepage_ok", homepage_ok)

    milestone_refs = [
        EvidenceRef(
            label=f"milestone_{index + 1}",
            source="portfolio_manifest",
            ref=milestone,
            note="Declared milestone in portfolio manifest",
        )
        for index, milestone in enumerate(project.milestones)
    ]
    signals.append(
        Signal(
            kind="milestone_count",
            value=len(project.milestones),
            note=f"{len(project.milestones)} declared milestones in config",
            rationale="Declared milestones define what a reviewer expects to verify later.",
            evidence_refs=milestone_refs,
        )
    )
    score += _score_signal("milestone_count", len(project.milestones))

    repo_data = None
    latest_release = None
    if project.repo:
        owner, repo_name = parse_repo(project.repo)
        repo_data, repo_error = safe_get_json(f"/repos/{owner}/{repo_name}")
        if repo_error:
            risks.append(
                Risk(
                    level="high",
                    message=repo_error,
                    rationale="The reviewer cannot inspect repository evidence if the repository lookup fails.",
                    evidence_refs=[_repo_ref(project)],
                )
            )
        else:
            push_days = iso_to_days(repo_data["pushed_at"])
            signals.append(
                Signal(
                    "push_days",
                    push_days,
                    f"Last push {push_days} days ago",
                    "Recent pushes are a direct public signal of ongoing delivery activity.",
                    [
                        EvidenceRef(
                            label="repo.pushed_at",
                            source="github_api",
                            ref=repo_data["pushed_at"],
                            note="Latest repository push timestamp",
                        ),
                        _repo_ref(project),
                    ],
                )
            )
            score += _score_signal("push_days", push_days)

            stars = repo_data["stargazers_count"]
            signals.append(
                Signal(
                    "stars",
                    stars,
                    f"GitHub stars: {stars}",
                    "Stars are a rough proxy for external visibility, not proof of delivery.",
                    [
                        EvidenceRef(
                            label="repo.stargazers_count",
                            source="github_api",
                            ref=str(stars),
                            note="Repository star count",
                        ),
                        _repo_ref(project),
                    ],
                )
            )
            score += _score_signal("stars", stars)

            open_issues = repo_data["open_issues_count"]
            signals.append(
                Signal(
                    "open_issues",
                    open_issues,
                    f"Open issues: {open_issues}",
                    "Open issue load is a weak maintainability signal and should be interpreted cautiously.",
                    [
                        EvidenceRef(
                            label="repo.open_issues_count",
                            source="github_api",
                            ref=str(open_issues),
                            note="Repository open issues count",
                        ),
                        _repo_ref(project, "/issues"),
                    ],
                )
            )
            score += _score_signal("open_issues", open_issues)

            releases, release_error = safe_get_json(f"/repos/{owner}/{repo_name}/releases?per_page=1")
            if release_error:
                risks.append(
                    Risk(
                        level="medium",
                        message=release_error,
                        rationale="Release evidence could not be fetched, so release cadence is unknown.",
                        evidence_refs=[_repo_ref(project, "/releases")],
                    )
                )
            elif releases:
                latest_release = releases[0]
                release_days = iso_to_days(latest_release["published_at"])
                signals.append(
                    Signal(
                        "release_days",
                        release_days,
                        f"Latest release {release_days} days ago",
                        "Recent releases are a stronger delivery signal than repository stars or issue counts.",
                        [
                            EvidenceRef(
                                label="release.published_at",
                                source="github_api",
                                ref=latest_release["published_at"],
                                note=f"Latest release: {latest_release['name'] or latest_release['tag_name']}",
                            ),
                            _repo_ref(project, "/releases"),
                        ],
                    )
                )
                score += _score_signal("release_days", release_days)
            else:
                risks.append(
                    Risk(
                        level="medium",
                        message="No GitHub releases found",
                        rationale="Without releases, reviewers need other evidence that milestones are being delivered.",
                        evidence_refs=[_repo_ref(project, "/releases")],
                    )
                )
    else:
        risks.append(
            Risk(
                level="high",
                message="No GitHub repository linked",
                rationale="A reviewer-facing workbench loses most evidence trace value without a repository source.",
                evidence_refs=[],
            )
        )

    for milestone in project.milestones:
        milestone_evidence = [
            EvidenceRef(
                label="declared_milestone",
                source="portfolio_manifest",
                ref=milestone,
                note="Expected outcome from project configuration",
            )
        ]
        rationale = "This milestone is only weakly mapped because the MVP uses generic public signals instead of milestone-specific evidence."
        status = "needs-review"

        milestone_lower = milestone.lower()
        if "release" in milestone_lower and latest_release:
            status = "supported-by-evidence"
            rationale = "A public GitHub release exists and can be reviewed against this milestone."
            milestone_evidence.append(
                EvidenceRef(
                    label="supporting_release",
                    source="github_api",
                    ref=latest_release["html_url"],
                    note=f"Latest release page for {project.name}",
                )
            )
        elif "homepage" in milestone_lower and homepage_ok:
            status = "supported-by-evidence"
            rationale = "The homepage is publicly reachable, so reviewers can inspect this deliverable directly."
            milestone_evidence.append(homepage_ref)
        elif ("github" in milestone_lower or "activity" in milestone_lower) and repo_data:
            status = "supported-by-evidence"
            rationale = "Recent repository activity exists and can be inspected directly by reviewers."
            milestone_evidence.append(_repo_ref(project))

        milestone_assessments.append(
            MilestoneAssessment(
                milestone=milestone,
                status=status,
                rationale=rationale,
                evidence_refs=milestone_evidence,
            )
        )

    status = _status(score)

    if status == "healthy":
        summary = f"{project.name} shows strong public activity signals and looks healthy."
    elif status == "watch":
        summary = f"{project.name} has mixed signals and should stay on the watchlist."
    else:
        summary = f"{project.name} has weak public signals and likely needs follow-up."

    if not homepage_ok:
        risks.append(
            Risk(
                level="medium",
                message="Homepage is missing or unavailable",
                rationale="If the homepage is unavailable, reviewers lose a direct public evidence surface.",
                evidence_refs=[_homepage_ref(project, f"HTTP status {homepage_status}" if homepage_status else homepage_note)],
            )
        )

    return ProjectReport(
        project=project,
        score=score,
        status=status,
        signals=signals,
        milestone_assessments=milestone_assessments,
        risks=risks,
        summary=summary,
    )


def project_report_to_dict(report: ProjectReport) -> dict[str, Any]:
    data = asdict(report)
    data["signals"] = [asdict(signal) for signal in report.signals]
    data["milestone_assessments"] = [asdict(item) for item in report.milestone_assessments]
    data["risks"] = [asdict(risk) for risk in report.risks]
    return data
