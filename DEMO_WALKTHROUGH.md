# Demo Walkthrough

This prototype is intentionally small but already runnable.

## What it does

Given a portfolio manifest, the agent:

1. Reads project metadata (repo, homepage, milestones)
2. Pulls public GitHub signals when a repo is available
3. Checks homepage reachability
4. Scores each project into `healthy`, `watch`, or `at-risk`
5. Writes both machine-readable and human-readable reports

## Demo command

```bash
gcc-impact examples/gcc_portfolio_demo.json --outdir output
```

## Example result

- Vyper → `watch` with recent GitHub activity but older releases and a large open-issue backlog
- SnarkExpress → `at-risk` because only homepage/milestone signals are available in the demo manifest
- Primus → `at-risk` for the same reason

## Why this is useful

The goal is not to auto-reject grants. The goal is to surface where human reviewers should look first, using auditable public signals instead of ad-hoc manual chasing.

## Next iteration

- Add RSS/blog/news ingestion
- Add chain milestone adapters
- Add evidence links for every signal
- Add weekly digest automation for GCC reviewers
