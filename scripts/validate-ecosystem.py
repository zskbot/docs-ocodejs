#!/usr/bin/env python3
"""Validate the machine-readable repository inventory without network access."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "ecosystem" / "repositories.json"
REQUIRED = {"name", "url", "role", "criticality", "runtime", "deployment", "healthCheck", "secretPolicy"}
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[^\s'\"]{12,}"),
)


def main() -> int:
    try:
        payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid inventory JSON: {exc}", file=sys.stderr)
        return 1

    if payload.get("schemaVersion") != 1 or not isinstance(payload.get("repositories"), list):
        print("Inventory must define schemaVersion=1 and a repositories array.", file=sys.stderr)
        return 1

    seen: set[str] = set()
    issues: list[str] = []
    for index, item in enumerate(payload["repositories"]):
        label = f"repositories[{index}]"
        if not isinstance(item, dict):
            issues.append(f"{label} must be an object")
            continue
        missing = REQUIRED - item.keys()
        if missing:
            issues.append(f"{label} missing fields: {', '.join(sorted(missing))}")
            continue
        name = item["name"]
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", name):
            issues.append(f"{label}.name must be a repository-safe identifier")
        elif name.lower() in seen:
            issues.append(f"duplicate repository name: {name}")
        else:
            seen.add(name.lower())

        parsed = urlparse(str(item["url"]))
        if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parsed.path.strip("/").split("/")) != 2:
            issues.append(f"{label}.url must be an HTTPS GitHub repository URL")

        if item["criticality"] not in {"low", "medium", "high", "critical"}:
            issues.append(f"{label}.criticality is not a supported level")
        for key, value in item.items():
            if not isinstance(value, str):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(value):
                    issues.append(f"{label}.{key} resembles a credential; store secrets in the platform secret manager")

    if issues:
        print("Ecosystem inventory validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"Ecosystem inventory OK: validated {len(payload['repositories'])} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
