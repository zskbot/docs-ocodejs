#!/usr/bin/env python3
"""Offline checks for the read-only infrastructure control center."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "ecosystem" / "services.json"
CAPABILITIES = ROOT / "ecosystem" / "cloudflare-capabilities.json"
DASHBOARD = ROOT / "infra" / "index.html"
REQUIRED_DASHBOARD_MARKERS = (
    "Infrastructure Control Center",
    "ecosystem/services.json",
    "mode:'cors'",
    "No production mutations",
)
SECRET_RE = re.compile(r"(?:gh[pousr]_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)", re.I)

def fail(message: str) -> int:
    print(f"Infrastructure validation failed: {message}", file=sys.stderr)
    return 1

def main() -> int:
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        capabilities = json.loads(CAPABILITIES.read_text(encoding="utf-8"))
        dashboard = DASHBOARD.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return fail(str(exc))
    if registry.get("schemaVersion") != 1 or not registry.get("services"):
        return fail("service registry schema or services array invalid")
    if capabilities.get("schemaVersion") != 1 or not isinstance(capabilities.get("resources"), dict):
        return fail("Cloudflare capability snapshot schema invalid")
    ids = [service.get("id") for service in registry["services"]]
    if len(ids) != len(set(ids)) or any(not isinstance(value, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) for value in ids):
        return fail("service IDs must be unique lowercase kebab-case")
    if capabilities["resources"].get("r2", {}).get("status") != "not-enabled":
        return fail("R2 must remain explicitly marked not-enabled until independently activated")
    if capabilities["resources"].get("workersKv", {}).get("namespaceCount") != 0:
        return fail("KV inventory snapshot mismatch")
    for marker in REQUIRED_DASHBOARD_MARKERS:
        if marker not in dashboard:
            return fail(f"dashboard is missing required marker: {marker}")
    for path, content in ((REGISTRY, REGISTRY.read_text(encoding="utf-8")), (CAPABILITIES, CAPABILITIES.read_text(encoding="utf-8")), (DASHBOARD, dashboard)):
        if SECRET_RE.search(content):
            return fail(f"possible secret material found in {path.relative_to(ROOT)}")
    print(f"Infrastructure checks passed: {len(ids)} services, capability snapshot and read-only dashboard.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
