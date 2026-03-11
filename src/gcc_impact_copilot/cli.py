from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_project
from .loader import load_projects
from .reporting import write_json, write_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a public-signal portfolio report")
    parser.add_argument("portfolio", help="Path to portfolio JSON file")
    parser.add_argument("--outdir", default="output", help="Directory for generated reports")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    projects = load_projects(args.portfolio)
    reports = [analyze_project(project) for project in projects]

    write_json(reports, outdir / "report.json")
    write_markdown(reports, outdir / "report.md")

    print(f"Wrote {len(reports)} project reports to {outdir}")


if __name__ == "__main__":
    main()
