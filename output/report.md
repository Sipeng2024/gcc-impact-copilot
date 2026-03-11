# GCC Impact Copilot Report

Reviewer-facing public evidence checks for grant portfolio projects.

## Vyper

- Status: **watch**
- Score: **55 / 100**
- Repo: `vyperlang/vyper`
- Homepage: https://vyperlang.org/
- Summary: Vyper has mixed signals and should stay on the watchlist.

### Signals

- `homepage_ok` = **True** — Homepage returned HTTP 200
  - Why it matters: Homepage reachability is a minimal public evidence check for whether reviewers can inspect project materials.
  - Evidence: `homepage` from **web** → `https://vyperlang.org/` (Homepage returned HTTP 200)
- `milestone_count` = **3** — 3 declared milestones in config
  - Why it matters: Declared milestones define what a reviewer expects to verify later.
  - Evidence: `milestone_1` from **portfolio_manifest** → `Track release cadence` (Declared milestone in portfolio manifest)
  - Evidence: `milestone_2` from **portfolio_manifest** → `Track homepage availability` (Declared milestone in portfolio manifest)
  - Evidence: `milestone_3` from **portfolio_manifest** → `Track GitHub activity` (Declared milestone in portfolio manifest)
- `push_days` = **1** — Last push 1 days ago
  - Why it matters: Recent pushes are a direct public signal of ongoing delivery activity.
  - Evidence: `repo.pushed_at` from **github_api** → `2026-03-09T19:22:21Z` (Latest repository push timestamp)
  - Evidence: `github_repo` from **github** → `vyperlang/vyper` (GitHub repository reference)
- `stars` = **5172** — GitHub stars: 5172
  - Why it matters: Stars are a rough proxy for external visibility, not proof of delivery.
  - Evidence: `repo.stargazers_count` from **github_api** → `5172` (Repository star count)
  - Evidence: `github_repo` from **github** → `vyperlang/vyper` (GitHub repository reference)
- `open_issues` = **590** — Open issues: 590
  - Why it matters: Open issue load is a weak maintainability signal and should be interpreted cautiously.
  - Evidence: `repo.open_issues_count` from **github_api** → `590` (Repository open issues count)
  - Evidence: `github_repo` from **github** → `vyperlang/vyper/issues` (GitHub repository reference)
- `release_days` = **265** — Latest release 265 days ago
  - Why it matters: Recent releases are a stronger delivery signal than repository stars or issue counts.
  - Evidence: `release.published_at` from **github_api** → `2025-06-18T20:09:23Z` (Latest release: v0.4.3  ("Buttermilk Racer"))
  - Evidence: `github_repo` from **github** → `vyperlang/vyper/releases` (GitHub repository reference)

### Milestone Mapping

- `Track release cadence` → **supported-by-evidence**
  - Rationale: A public GitHub release exists and can be reviewed against this milestone.
  - Evidence: `declared_milestone` from **portfolio_manifest** → `Track release cadence` (Expected outcome from project configuration)
  - Evidence: `supporting_release` from **github_api** → `https://github.com/vyperlang/vyper/releases/tag/v0.4.3` (Latest release page for Vyper)
- `Track homepage availability` → **supported-by-evidence**
  - Rationale: The homepage is publicly reachable, so reviewers can inspect this deliverable directly.
  - Evidence: `declared_milestone` from **portfolio_manifest** → `Track homepage availability` (Expected outcome from project configuration)
  - Evidence: `homepage` from **web** → `https://vyperlang.org/` (Homepage returned HTTP 200)
- `Track GitHub activity` → **supported-by-evidence**
  - Rationale: Recent repository activity exists and can be inspected directly by reviewers.
  - Evidence: `declared_milestone` from **portfolio_manifest** → `Track GitHub activity` (Expected outcome from project configuration)
  - Evidence: `github_repo` from **github** → `vyperlang/vyper` (GitHub repository reference)

## SnarkExpress

- Status: **at-risk**
- Score: **14 / 100**
- Homepage: https://snark.express/
- Summary: SnarkExpress has weak public signals and likely needs follow-up.

### Signals

- `homepage_ok` = **True** — Homepage returned HTTP 200
  - Why it matters: Homepage reachability is a minimal public evidence check for whether reviewers can inspect project materials.
  - Evidence: `homepage` from **web** → `https://snark.express/` (Homepage returned HTTP 200)
- `milestone_count` = **2** — 2 declared milestones in config
  - Why it matters: Declared milestones define what a reviewer expects to verify later.
  - Evidence: `milestone_1` from **portfolio_manifest** → `Track site uptime` (Declared milestone in portfolio manifest)
  - Evidence: `milestone_2` from **portfolio_manifest** → `Track publication freshness` (Declared milestone in portfolio manifest)

### Milestone Mapping

- `Track site uptime` → **needs-review**
  - Rationale: This milestone is only weakly mapped because the MVP uses generic public signals instead of milestone-specific evidence.
  - Evidence: `declared_milestone` from **portfolio_manifest** → `Track site uptime` (Expected outcome from project configuration)
- `Track publication freshness` → **needs-review**
  - Rationale: This milestone is only weakly mapped because the MVP uses generic public signals instead of milestone-specific evidence.
  - Evidence: `declared_milestone` from **portfolio_manifest** → `Track publication freshness` (Expected outcome from project configuration)

### Risks / Follow-ups

- **high** — No GitHub repository linked
  - Why flagged: A reviewer-facing workbench loses most evidence trace value without a repository source.

## Primus

- Status: **at-risk**
- Score: **14 / 100**
- Homepage: https://primuslabs.xyz/
- Summary: Primus has weak public signals and likely needs follow-up.

### Signals

- `homepage_ok` = **True** — Homepage returned HTTP 200
  - Why it matters: Homepage reachability is a minimal public evidence check for whether reviewers can inspect project materials.
  - Evidence: `homepage` from **web** → `https://primuslabs.xyz/` (Homepage returned HTTP 200)
- `milestone_count` = **2** — 2 declared milestones in config
  - Why it matters: Declared milestones define what a reviewer expects to verify later.
  - Evidence: `milestone_1` from **portfolio_manifest** → `Track site uptime` (Declared milestone in portfolio manifest)
  - Evidence: `milestone_2` from **portfolio_manifest** → `Track public updates` (Declared milestone in portfolio manifest)

### Milestone Mapping

- `Track site uptime` → **needs-review**
  - Rationale: This milestone is only weakly mapped because the MVP uses generic public signals instead of milestone-specific evidence.
  - Evidence: `declared_milestone` from **portfolio_manifest** → `Track site uptime` (Expected outcome from project configuration)
- `Track public updates` → **needs-review**
  - Rationale: This milestone is only weakly mapped because the MVP uses generic public signals instead of milestone-specific evidence.
  - Evidence: `declared_milestone` from **portfolio_manifest** → `Track public updates` (Expected outcome from project configuration)

### Risks / Follow-ups

- **high** — No GitHub repository linked
  - Why flagged: A reviewer-facing workbench loses most evidence trace value without a repository source.
