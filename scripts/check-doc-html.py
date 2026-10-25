#!/usr/bin/env python3
"""Lightweight stdlib checks for the static documentation homepage."""
from html.parser import HTMLParser
from pathlib import Path
import sys

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

class HomepageAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = []
        self.fragments = []
        self.missing_alt = []
        self.open_counts = {}
        self.close_counts = {}

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.open_counts[tag] = self.open_counts.get(tag, 0) + 1
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicates.append(element_id)
            self.ids.add(element_id)
        href = values.get("href", "")
        if href.startswith("#") and len(href) > 1:
            self.fragments.append(href[1:])
        if tag == "img" and "alt" not in values:
            self.missing_alt.append(values.get("src", "(image without src)"))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        self.close_counts[tag] = self.close_counts.get(tag, 0) + 1

def main():
    path = Path("index.html")
    if not path.is_file():
        print("ERROR: index.html not found", file=sys.stderr)
        return 2
    audit = HomepageAudit()
    try:
        audit.feed(path.read_text(encoding="utf-8"))
        audit.close()
    except Exception as exc:
        print(f"ERROR: HTML parser failed: {exc}", file=sys.stderr)
        return 2

    errors = []
    if audit.duplicates:
        errors.append("duplicate id attributes: " + ", ".join(sorted(set(audit.duplicates))))
    missing = sorted(set(audit.fragments) - audit.ids)
    if missing:
        errors.append("broken in-page links: " + ", ".join("#" + item for item in missing))
    if audit.missing_alt:
        errors.append("images missing alt text: " + ", ".join(audit.missing_alt))
    for tag in ("style", "script", "form"):
        opened = audit.open_counts.get(tag, 0)
        closed = audit.close_counts.get(tag, 0)
        if opened != closed:
            errors.append(f"<{tag}> count mismatch: {opened} opening / {closed} closing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"OK: index.html parsed; {len(audit.ids)} unique IDs; "
          f"{len(audit.fragments)} in-page links; style/script/form counts match.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
