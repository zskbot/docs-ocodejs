#!/usr/bin/env python3
"""Read-only documentation corpus builder for public ecosystem repositories."""
from __future__ import annotations
import csv, hashlib, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

REPOSITORIES = [
    "Velclaw/VelCli", "zskbot/X-BO", "OCodejs/OCodejs", "Velclaw/OCodejs",
    "Velclaw/VelclawHost", "Velclaw/velclaw-deploy", "Velclaw/Oauth",
    "Velclaw/docs.velclaw.ai", "Velclaw/VELCLAW",
    "Velclaw/Velclaw-velclaw-docs-ui-reference", "Velclaw/Velclaw-OCodejs",
]
DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".adoc", ".asciidoc", ".txt", ".html", ".htm"}
SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", "coverage"}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token|password|private[_-]?key)\s*[:=]\s*['\"]?([A-Za-z0-9_./+=-]{28,})"),
]
PLACEHOLDER_WORDS = ("example", "placeholder", "your_", "replace_me", "changeme", "dummy", "redacted")

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def suspicious_secret(data):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            candidate = match.group(1) if match.lastindex else match.group(0)
            if not any(word in candidate.lower() for word in PLACEHOLDER_WORDS):
                return True
    return False

def git_output(repo_dir, *args):
    return subprocess.check_output(["git", "-C", str(repo_dir), *args], text=True).strip()

def main():
    output = Path(os.environ.get("AUDIT_OUTPUT", "audit-output")).resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    extracted = output / "source-docs"
    extracted.mkdir()
    rows, summaries, skipped = [], [], []
    total_files = total_docs = included_docs = binary_files = 0

    with tempfile.TemporaryDirectory(prefix="ecosystem-audit-") as temp_name:
        temp = Path(temp_name)
        for repo in REPOSITORIES:
            slug = repo.replace("/", "__")
            checkout = temp / slug
            print("Cloning " + repo, flush=True)
            subprocess.run(["git", "clone", "--depth=1", "--no-tags",
                            "https://github.com/" + repo + ".git", str(checkout)],
                           check=True, stdout=subprocess.DEVNULL)
            commit = git_output(checkout, "rev-parse", "HEAD")
            branch = git_output(checkout, "branch", "--show-current") or "default"
            target_root = extracted / slug
            target_root.mkdir(parents=True, exist_ok=True)
            repo_files = repo_docs = repo_included = repo_skipped = 0

            for root, dirs, files in os.walk(checkout):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                for name in sorted(files):
                    source = Path(root) / name
                    rel = source.relative_to(checkout)
                    if ".git" in rel.parts:
                        continue
                    if source.is_symlink():
                        target = os.readlink(source)
                        target_bytes = target.encode("utf-8", errors="replace")
                        rows.append({
                            "repository": repo, "branch": branch, "commit": commit,
                            "path": rel.as_posix(), "size_bytes": len(target_bytes),
                            "sha256": hashlib.sha256(target_bytes).hexdigest(),
                            "is_document": "false", "included_in_corpus": "false",
                            "skip_reason": "symlink not followed",
                        })
                        total_files += 1
                        repo_files += 1
                        continue
                    try:
                        size = source.stat().st_size
                        digest = sha256_file(source)
                        with source.open("rb") as handle:
                            head = handle.read(8192)
                    except OSError:
                        continue
                    ext = source.suffix.lower()
                    is_doc = ext in DOC_EXTENSIONS
                    is_binary = b"\x00" in head
                    if is_binary:
                        binary_files += 1
                    include, reason = False, ""
                    if is_doc and not is_binary:
                        total_docs += 1
                        repo_docs += 1
                        if size > 20 * 1024 * 1024:
                            reason = "document exceeds 20 MiB safety limit"
                            repo_skipped += 1
                        else:
                            raw = source.read_bytes()
                            if suspicious_secret(raw):
                                reason = "secret-like content; excluded from corpus"
                                skipped.append(repo + ":" + rel.as_posix())
                                repo_skipped += 1
                            else:
                                destination = target_root / rel
                                destination.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copyfile(source, destination)
                                include = True
                                included_docs += 1
                                repo_included += 1
                    rows.append({
                        "repository": repo, "branch": branch, "commit": commit,
                        "path": rel.as_posix(), "size_bytes": size, "sha256": digest,
                        "is_document": str(is_doc).lower(),
                        "included_in_corpus": str(include).lower(), "skip_reason": reason,
                    })
                    total_files += 1
                    repo_files += 1
            summaries.append((repo, branch, commit, repo_files, repo_docs, repo_included, repo_skipped))

    with (output / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "repository", "branch", "commit", "path", "size_bytes", "sha256",
            "is_document", "included_in_corpus", "skip_reason"])
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Ecosystem Audit Artifact", "",
        "Generated by the read-only documentation corpus workflow.", "",
        "- Repositories cloned: " + str(len(REPOSITORIES)),
        "- Total files inventoried: " + str(total_files),
        "- Text-document files detected: " + str(total_docs),
        "- Documents included in corpus: " + str(included_docs),
        "- Documents excluded by secret-like pattern checks: " + str(len(skipped)),
        "- Binary files seen in source trees: " + str(binary_files), "",
        "Secret screening is heuristic, not a guarantee. Matched values are never logged.",
        "", "## Per-repository results", "",
        "| Repository | Branch | Commit | Files | Docs | Included | Skipped |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for repo, branch, commit, files, docs, included, excluded in summaries:
        lines.append("| [" + repo + "](https://github.com/" + repo + ") | " +
                     branch + " | " + commit + " | " + str(files) + " | " +
                     str(docs) + " | " + str(included) + " | " + str(excluded) + " |")
    lines += [
        "", "## Provenance and limitations", "",
        "- manifest.csv records repository, branch, commit, path, size and SHA-256.",
        "- source-docs.zip contains text documentation only, preserving original paths.",
        "- Binary assets and source-code files are inventoried but not placed in the corpus.",
        "- Review upstream licenses before redistributing source documents.",
        "- The secret scanner can miss secrets; review artifacts privately before sharing.",
        "- Source repositories are not modified; no production deploy, merge or database write occurs.",
    ]
    (output / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with zipfile.ZipFile(output / "source-docs.zip", "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(extracted.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(output).as_posix())
    print("Audit complete: " + str(total_files) + " files inventoried; " +
          str(included_docs) + " docs included; " + str(len(skipped)) + " docs excluded.", flush=True)

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print("Audit failed during a subprocess; no secret values were printed.", file=sys.stderr)
        sys.exit(exc.returncode or 1)
