from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

GITHUB_API = "https://api.github.com"
DEFAULT_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "gcc-impact-copilot",
}


def _headers() -> dict[str, str]:
    headers = dict(DEFAULT_HEADERS)
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_json(path: str) -> Any:
    request = urllib.request.Request(f"{GITHUB_API}{path}", headers=_headers())
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def safe_get_json(path: str) -> tuple[Any | None, str | None]:
    try:
        return get_json(path), None
    except urllib.error.HTTPError as error:
        return None, f"GitHub API error {error.code} on {path}"
    except urllib.error.URLError as error:
        return None, f"GitHub API unavailable: {error.reason}"


def parse_repo(repo: str) -> tuple[str, str]:
    if repo.startswith("https://github.com/"):
        repo = urllib.parse.urlparse(repo).path.strip("/")
    owner, name = repo.split("/", 1)
    return owner, name


def iso_to_days(iso_value: str) -> int:
    dt = datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return max((now - dt).days, 0)
