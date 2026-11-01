#!/usr/bin/env python3
"""Read-only HTTP and MCP protocol smoke test for OCode.js Documentation MCP."""
from __future__ import annotations

import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

EXPECTED_TOOLS = {
    "search_ocodejs_docs",
    "list_ocodejs_docs",
    "get_ocodejs_document",
    "get_ocodejs_project_overview",
}


def access_headers() -> dict[str, str]:
    """Return Cloudflare Access service-token headers without exposing values."""
    client_id = os.environ.get("CF_ACCESS_CLIENT_ID", "").strip()
    client_secret = os.environ.get("CF_ACCESS_CLIENT_SECRET", "").strip()
    if bool(client_id) != bool(client_secret):
        raise RuntimeError(
            "Cloudflare Access configuration is incomplete: set both "
            "CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET."
        )
    if not client_id and os.environ.get("REQUIRE_ACCESS_TOKEN", "").lower() == "true":
        raise RuntimeError(
            "Cloudflare Access service token is required for CI. Configure the "
            "CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET GitHub Actions secrets."
        )
    if not client_id:
        print("NOTICE: no Cloudflare Access service token supplied; using unauthenticated mode.")
        return {}
    return {
        "CF-Access-Client-Id": client_id,
        "CF-Access-Client-Secret": client_secret,
    }


def request_json(
    url: str,
    payload: dict | None = None,
    auth_headers: dict[str, str] | None = None,
) -> tuple[int, dict]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Accept": "application/json",
        "User-Agent": "OCodejs-MCP-Smoke-Test",
        **(auth_headers or {}),
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, data=body, headers=headers, method="GET" if body is None else "POST")
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            with urlopen(request, timeout=20) as response:
                status = response.status
                data = json.loads(response.read().decode("utf-8"))
                if not isinstance(data, dict):
                    raise AssertionError(f"{url} returned a non-object JSON payload")
                return status, data
        except HTTPError as exc:
            last_error = exc
            if exc.code < 500 and exc.code != 429:
                if exc.code == 403:
                    server = exc.headers.get("server", "unknown")
                    ray = exc.headers.get("cf-ray", "not-provided")
                    raise RuntimeError(
                        f"{url} returned HTTP 403 (server={server}, cf-ray={ray}); "
                        "verify the exact Access application/policy and service-token "
                        "authorization. No automatic bypass is attempted."
                    ) from exc
                if exc.code in (401,):
                    raise RuntimeError(
                        f"{url} returned HTTP {exc.code}; the Access service token "
                        "may be invalid, expired, or not authorized for this application."
                    ) from exc
                raise RuntimeError(f"{url} returned HTTP {exc.code}") from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
        if attempt < 4:
            time.sleep(3)
    raise RuntimeError(f"{url} failed after 5 attempts: {last_error}")


def main() -> int:
    base = os.environ.get("MCP_URL", "https://ocodejs-docs-mcp.velclaw.workers.dev").rstrip("/")
    parsed = urlparse(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("MCP_URL must be a credential-free HTTPS origin")

    auth = access_headers()
    status, health = request_json(f"{base}/health", auth_headers=auth)
    assert 200 <= status < 300, status
    assert health.get("name") == "ocodejs-docs-mcp", health
    assert health.get("status") == "ok", health
    assert set(health.get("tools", [])) == EXPECTED_TOOLS, health.get("tools")
    print("PASS /health: Worker identity, status, and four read-only tools.")

    status, initialized = request_json(
        f"{base}/mcp",
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "ocodejs-mcp-smoke-test", "version": "1.0"},
            },
        },
        auth_headers=auth,
    )
    result = initialized.get("result", {})
    assert 200 <= status < 300, status
    assert initialized.get("jsonrpc") == "2.0" and initialized.get("id") == 1, initialized
    assert result.get("protocolVersion") == "2025-03-26", result
    assert result.get("serverInfo", {}).get("name") == "ocodejs-docs-mcp", result
    assert "tools" in result.get("capabilities", {}), result
    print("PASS initialize: MCP protocol and server identity.")

    status, listed = request_json(
        f"{base}/mcp",
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        auth_headers=auth,
    )
    tools = listed.get("result", {}).get("tools", [])
    names = {item.get("name") for item in tools}
    assert 200 <= status < 300, status
    assert listed.get("jsonrpc") == "2.0" and listed.get("id") == 2, listed
    assert names == EXPECTED_TOOLS, names
    assert all(item.get("inputSchema", {}).get("type") == "object" for item in tools), tools
    print("PASS tools/list: exact read-only tool inventory and input schemas.")
    print("MCP smoke test passed. GitHub upstream document fetches are not tested by these protocol checks.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"MCP smoke test failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
