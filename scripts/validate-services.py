#!/usr/bin/env python3
"""Validate the service registry offline; never contact external services."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "ecosystem" / "services.json"
REQUIRED = {
    "id", "name", "role", "platform", "status", "source", "publicUrl",
    "healthUrl", "healthSemantics", "dataStores", "authentication", "evidence", "notes",
}
STATUSES = {
    "workflow-passed-not-live-verified",
    "deployment-reported-not-live-verified",
    "blocked-before-project-creation",
    "preview-pending",
    "runtime-verified",
    "production-verified",
}
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[^\s'\"]{12,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def valid_https_url(value: object) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password


def main() -> int:
    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid service registry JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(payload, dict) or payload.get("schemaVersion") != 1:
        print("Service registry must define schemaVersion=1.", file=sys.stderr)
        return 1
    services = payload.get("services")
    if not isinstance(services, list) or not services:
        print("Service registry must contain a non-empty services array.", file=sys.stderr)
        return 1

    issues: list[str] = []
    seen: set[str] = set()
    for index, service in enumerate(services):
        label = f"services[{index}]"
        if not isinstance(service, dict):
            issues.append(f"{label} must be an object")
            continue
        missing = REQUIRED - service.keys()
        if missing:
            issues.append(f"{label} missing fields: {', '.join(sorted(missing))}")
            continue

        identifier = service["id"]
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            issues.append(f"{label}.id must be a lowercase kebab-case identifier")
        elif identifier in seen:
            issues.append(f"duplicate service id: {identifier}")
        else:
            seen.add(identifier)

        if service["status"] not in STATUSES:
            issues.append(f"{label}.status is not a supported evidence status")
        for field in ("source", "publicUrl", "healthUrl"):
            if not valid_https_url(service[field]):
                issues.append(f"{label}.{field} must be null or a credential-free HTTPS URL")

        for field in ("dataStores", "evidence"):
            if not isinstance(service[field], list) or not all(isinstance(item, str) and item.strip() for item in service[field]):
                issues.append(f"{label}.{field} must be an array of non-empty strings")
        for field in ("name", "role", "platform", "healthSemantics", "authentication", "notes"):
            if not isinstance(service[field], str) or not service[field].strip():
                issues.append(f"{label}.{field} must be a non-empty string")

        for field, value in service.items():
            values = value if isinstance(value, list) else [value]
            for item in values:
                if not isinstance(item, str):
                    continue
                for pattern in SECRET_PATTERNS:
                    if pattern.search(item):
                        issues.append(f"{label}.{field} resembles a credential; use the platform secret manager")

    if issues:
        print("Service registry validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"Service registry OK: validated {len(services)} services.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
