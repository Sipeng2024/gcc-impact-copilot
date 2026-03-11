# GCC Impact Copilot

GCC Impact Copilot is an agent-ready monitoring tool for public-goods grant portfolios. It turns scattered public signals—GitHub activity, release cadence, homepage availability, and declared milestones—into a compact health report that reviewers can inspect in minutes instead of waiting for quarterly manual updates.

## Why this matters

Grant programs often rely on founder updates, ad-hoc check-ins, and spreadsheet chasing. That makes impact evaluation late, inconsistent, and hard to audit. GCC Impact Copilot creates a lightweight, repeatable monitoring layer that helps reviewers answer:

- Is the project still active?
- Are there public delivery signals we can verify ourselves?
- Which grants need follow-up now instead of at quarter end?
- Which portfolio projects deserve deeper manual review?

## MVP scope

This prototype focuses on public signals only:

- GitHub repository freshness (`pushed_at`)
- GitHub releases
- GitHub open issue volume
- GitHub stars as a rough community signal
- Homepage reachability
- Configured milestones / expected outputs

The output is a JSON report plus a readable Markdown report that can be posted into GitHub, Notion, Telegram, or a dashboard.

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

## Agent workflow

1. Load a portfolio manifest.
2. Fetch public signals from GitHub and project homepages.
3. Score each project into `healthy`, `watch`, or `at-risk`.
4. Emit a compact report with follow-up risks.
5. Hand the flagged items to a human reviewer or another agent.

## Why it fits GCC

- Real GCC problem: impact evaluation is repetitive and easy to delay.
- Agent-native: the tool gathers, summarizes, and prioritizes without pretending to replace human judgment.
- Public goods friendly: any DAO, foundation, or grants program can reuse the same workflow.
- Auditable: every score is backed by explicit public signals.

## Next steps

- Add RSS/blog/news ingestion
- Add chain activity adapters for wallet-based milestones
- Add project-specific rubrics instead of one global scorecard
- Add weekly digest automation
- Add a reviewer UI for comments and overrides

## License

MIT
