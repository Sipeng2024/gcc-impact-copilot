# GCC Impact Copilot

GCC Impact Copilot is a reviewer-facing impact review workbench for public-goods grant portfolios. It turns scattered public signals—GitHub activity, release cadence, homepage availability, and declared milestones—into structured review input that a grant manager can inspect, verify, and follow up on.

## Positioning

Impact Copilot is **for reviewers, not crawlers**.

Its job is not to be a universal evidence collection engine. Its job is to help a human reviewer answer:

- What public evidence do we currently have?
- How does that evidence map to expected milestones?
- What looks healthy, what needs follow-up, and why?
- Which grants should a human review next?

If a broader portfolio crawler exists in the future, that system should be an upstream input to Impact Copilot, not part of the same product boundary.

## Why this matters

Grant programs often rely on founder updates, ad-hoc check-ins, and spreadsheet chasing. That makes impact evaluation late, inconsistent, and hard to audit. GCC Impact Copilot creates a lightweight review workflow that helps reviewers move from scattered evidence to structured follow-up.

## MVP scope

This prototype focuses on reviewer-visible signals:

- GitHub repository freshness (`pushed_at`)
- GitHub releases
- GitHub open issue volume
- GitHub stars as a rough community signal
- Homepage reachability
- Configured milestones / expected outputs
- Follow-up risks that a human reviewer should inspect
- Evidence trace for every visible judgment

The output is a JSON report plus a readable Markdown report that can be posted into GitHub, Notion, Telegram, or a review dashboard.

## Evidence trace shape

The core rule is simple: **every judgment should point back to explicit public evidence**.

Each report now carries:

- `signals`: reviewer-visible observations plus rationale and evidence references
- `milestone_assessments`: milestone-by-milestone mapping with supporting evidence
- `risks`: flagged follow-up items with explicit reasons and evidence

Example shape:

```json
{
  "kind": "release_days",
  "value": 265,
  "note": "Latest release 265 days ago",
  "rationale": "Recent releases are a stronger delivery signal than repository stars or issue counts.",
  "evidence_refs": [
    {
      "label": "release.published_at",
      "source": "github_api",
      "ref": "2025-06-19T10:12:00Z",
      "note": "Latest release: v0.4.2"
    },
    {
      "label": "github_repo",
      "source": "github",
      "ref": "vyperlang/vyper/releases",
      "note": "GitHub repository reference"
    }
  ]
}
```

This keeps the tool anchored as a review workbench instead of a black-box summarizer.

## Quickstart

```bash
cd gcc-impact-copilot
python -m venv .venv
source .venv/bin/activate
pip install -e .
gcc-impact examples/gcc_portfolio_demo.json --outdir output
```

If you want higher GitHub API limits:

```bash
export GITHUB_TOKEN=YOUR_TOKEN
```

## Example output

After running the CLI, you will get:

- `output/report.json`
- `output/report.md`

## Review workflow

1. Load a portfolio manifest with project context and expected milestones.
2. Read public evidence from GitHub and project homepages.
3. Map the visible signals into a compact status summary.
4. Attach evidence trace to every visible judgment.
5. Surface explicit risks and missing evidence.
6. Hand the result to a human reviewer for follow-up, override, or escalation.

## Why it fits GCC

- Real GCC problem: impact evaluation is repetitive and easy to delay.
- Reviewer-centric: it supports grant managers instead of pretending to replace them.
- Public goods friendly: any DAO, foundation, or grants program can reuse the same review workflow.
- Auditable: every judgment should be backed by explicit public evidence.

## Next steps

- Add evidence trace links for every signal
- Add milestone-to-evidence mapping beyond simple MVP heuristics
- Add reviewer comments, overrides, and follow-up states
- Add weekly digest automation for human review queues
- Keep large-scale crawling outside this repo's main product boundary

## License

MIT
