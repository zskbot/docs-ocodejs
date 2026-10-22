#!/usr/bin/env python3
"""Validate local Markdown links and fragments in the documentation hub."""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOC_EXTENSIONS = {".md", ".mdx"}
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\((<[^>]+>|[^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
HTML_ID_RE = re.compile(r'\bid=["\']([^"\']+)["\']', re.I)


def slugify(heading: str) -> str:
    heading = re.sub(r"`([^\`]+)`", r"\1", heading)
    heading = re.sub(r"[*_~]", "", heading).strip().lower()
    heading = unicodedata.normalize("NFKD", heading)
    heading = "".join(ch for ch in heading if not unicodedata.combining(ch))
    heading = re.sub(r"[^\w -]", "", heading)
    return re.sub(r"\s+", "-", heading).strip("-")


def anchors(path: Path) -> set[str]:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()
    found = set(HTML_ID_RE.findall(content))
    seen: dict[str, int] = {}
    for line in content.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify(match.group(1))
        count = seen.get(base, 0)
        seen[base] = count + 1
        found.add(base if count == 0 else f"{base}-{count}")
    return found


def main() -> int:
    issues: list[str] = []
    docs = sorted(
        p for p in ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in DOC_EXTENSIONS
        and not any(part in {".git", "node_modules"} for part in p.parts)
    )
    for source in docs:
        try:
            content = source.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Avoid interpreting Markdown examples inside fenced code blocks as links.
        content = re.sub(r"(?ms)^\s*```.*?^\s*```\s*$", "", content)
        content = re.sub(r"(?ms)^\s*~~~.*?^\s*~~~\s*$", "", content)
        for match in LINK_RE.finditer(content):
            raw = match.group(1).strip()
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            destination = raw.split(maxsplit=1)[0].strip()
            parsed = urlsplit(destination)
            if parsed.scheme or destination.startswith("//"):
                continue
            path_part = unquote(parsed.path)
            fragment = unquote(parsed.fragment)
            if not path_part:
                target = source
            else:
                target = (source.parent / path_part).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                issues.append(f"{source.relative_to(ROOT)}: link escapes repository: {destination}")
                continue
            if not target.exists():
                issues.append(f"{source.relative_to(ROOT)}: missing target: {destination}")
                continue
            if fragment and target.is_file() and target.suffix.lower() in DOC_EXTENSIONS:
                if fragment not in anchors(target):
                    issues.append(f"{source.relative_to(ROOT)}: missing anchor: {destination}")
    if issues:
        print("Documentation link validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"Documentation links OK: scanned {len(docs)} Markdown/MDX files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
