#!/usr/bin/env python3
"""Agent Plugins 1.0.0 conformance checker for this package.

Checks the normative requirements from https://agent-plugins.org/specification
that a JSON Schema alone cannot express. Schema validation (ajv) and Agent
Skills validation (skills-ref) run alongside this in CI.

Exit 0 = conformant. Exit 1 = at least one violation.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"

# Section 5.2 - the manifest schema is closed.
MANIFEST_FIELDS = {
    "$schema", "name", "version", "description",
    "author", "homepage", "repository", "license", "keywords", "extensions",
}
# Section 5.5 / "Name constraints".
NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
# Section 8 - reverse-domain namespace.
NS_RE = re.compile(r"^[a-z0-9-]+(?:\.[a-z0-9-]+)+$")

LOOPBACK = {"localhost", "127.0.0.1", "::1", "[::1]"}

errors: list[str] = []
checks: list[str] = []


def ok(msg: str) -> None:
    checks.append(msg)


def bad(msg: str) -> None:
    errors.append(msg)


# --- Section 4.1: path safety -------------------------------------------------
def check_path_safety() -> None:
    resolved_root = ROOT.resolve()
    symlinks = 0
    escaping = []
    for p in ROOT.rglob("*"):
        if ".git" in p.parts:
            continue
        if p.is_symlink():
            symlinks += 1
            try:
                target = p.resolve(strict=False)
            except OSError:
                escaping.append(str(p))
                continue
            if not str(target).startswith(str(resolved_root) + "/"):
                escaping.append(f"{p} -> {target}")
    if escaping:
        bad(f"4.1 path safety: paths resolve outside the plugin root: {escaping}")
    else:
        ok(f"4.1 every package path resolves inside the plugin root ({symlinks} symlinks)")


# --- Section 5: manifest ------------------------------------------------------
def check_manifest() -> dict:
    path = ROOT / "plugin.json"
    if not path.is_file():
        bad("5.1 plugin.json MUST exist as a regular file in the plugin root")
        return {}
    try:
        m = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        bad(f"5.2 plugin.json MUST be valid JSON: {e}")
        return {}
    if not isinstance(m, dict):
        bad("5.2 plugin.json MUST contain a top-level object")
        return {}
    ok("5.1 plugin.json present at the plugin root and is a JSON object")

    unknown = set(m) - MANIFEST_FIELDS
    if unknown:
        bad(f"5.2 closed schema: unknown top-level field(s) {sorted(unknown)}")
    else:
        ok("5.2 manifest uses only the 10 permitted top-level fields")

    if m.get("$schema") != PLUGIN_SCHEMA:
        bad(f"5.3 $schema MUST be {PLUGIN_SCHEMA}")
    else:
        ok("5.3 $schema is the canonical 1.0.0 plugin schema")

    name = m.get("name")
    if not isinstance(name, str) or not name:
        bad("5.3 name is REQUIRED and MUST be a non-empty string")
    elif not (1 <= len(name) <= 64) or not NAME_RE.match(name):
        bad(f"5.5 name {name!r} violates the name constraints")
    else:
        ok(f"5.5 name {name!r} satisfies length, charset, edge and repetition rules")

    # Section 8.1
    ext = m.get("extensions")
    if ext is not None:
        if not isinstance(ext, dict):
            bad("8.1 extensions MUST be an object")
        else:
            for ns, val in ext.items():
                if not NS_RE.match(ns):
                    bad(f"8.1 extension namespace {ns!r} is not reverse-domain")
                elif not isinstance(val, dict):
                    bad(f"8.1 extensions[{ns!r}] MUST be an object")
            else:
                ok(f"8.1 extensions keyed by reverse-domain namespace(s): {sorted(ext)}")
    return m


# --- Sections 6 + 7.1: component discovery and skills -------------------------
def check_skills() -> None:
    skills = ROOT / "skills"
    if not skills.exists():
        ok("6 skills/ absent - not an error")
        return
    if not skills.is_dir():
        bad("6 skills/ exists but is not a directory")
        return

    discovered = [d for d in sorted(skills.iterdir())
                  if d.is_dir() and (d / "SKILL.md").is_file()]
    ok(f"7.1 {len(discovered)} skill(s) discoverable as immediate children of skills/")

    # Anything deeper is silently ignored by conformant clients - catch author error.
    buried = [p for p in skills.rglob("SKILL.md")
              if p.parent.parent != skills]
    if buried:
        bad(f"7.1 SKILL.md found below the immediate-child depth; clients MUST NOT "
            f"recurse, so these would never load: {[str(p) for p in buried]}")
    else:
        ok("7.1 no SKILL.md buried below immediate-child depth")

    stray = [d.name for d in skills.iterdir()
             if d.is_dir() and not (d / "SKILL.md").is_file()]
    if stray:
        bad(f"7.1 directories in skills/ without SKILL.md (will not load): {stray}")


# --- Section 7.2: MCP configuration -------------------------------------------
def check_mcp() -> None:
    path = ROOT / "mcp.json"
    if not path.exists():
        ok("6 mcp.json absent - not an error")
        return
    if not path.is_file():
        bad("6 mcp.json exists but is not a regular file")
        return
    try:
        c = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        bad(f"7.2.1 mcp.json MUST be valid JSON: {e}")
        return

    if set(c) - {"$schema", "mcpServers"}:
        bad(f"7.2.1 mcp.json permits no other top-level fields; found {sorted(c)}")
    elif c.get("$schema") != MCP_SCHEMA:
        bad(f"7.2.1 mcp.json $schema MUST be {MCP_SCHEMA}")
    else:
        ok("7.2.1 mcp.json has exactly $schema + mcpServers, canonical schema id")

    servers = c.get("mcpServers")
    if not isinstance(servers, dict):
        bad("7.2.1 mcpServers MUST be an object")
        return

    for sname, s in servers.items():
        t = s.get("type")
        if t in ("streamable-http", "sse"):
            url = s.get("url", "")
            u = urlparse(url)
            if u.scheme not in ("http", "https"):
                bad(f"7.2 server {sname!r}: url MUST be an absolute http(s) URL")
            elif u.scheme != "https" and u.hostname not in LOOPBACK:
                bad(f"7.2 server {sname!r}: HTTPS is REQUIRED for non-loopback URLs")
            else:
                ok(f"7.2 server {sname!r}: {t} over {u.scheme} to {u.hostname}")
            for hk, hv in (s.get("headers") or {}).items():
                if not isinstance(hv, str):
                    bad(f"7.2 server {sname!r}: header {hk!r} MUST be a string")
        elif t == "stdio":
            cmd = s.get("command", "")
            if not cmd:
                bad(f"7.2 server {sname!r}: command is REQUIRED")
            elif not (cmd.startswith("./") or "/" not in cmd):
                bad(f"7.2 server {sname!r}: command MUST be a bare executable token "
                    f"or a ./-prefixed plugin-relative path, got {cmd!r}")
            if "${" in cmd:
                bad(f"7.2 server {sname!r}: placeholders MUST NOT appear in command")
            for k in (s.get("env") or {}):
                if k in ("PLUGIN_ROOT", "PLUGIN_DATA"):
                    bad(f"9.1 server {sname!r}: env MUST NOT define {k}")
            ok(f"7.2 server {sname!r}: stdio config checked")
        else:
            bad(f"7.2 server {sname!r}: type MUST be stdio, streamable-http or sse")


# --- No embedded credentials --------------------------------------------------
def check_no_secrets() -> None:
    pat = re.compile(r"sk_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}")
    hits = []
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or not p.is_file():
            continue
        try:
            text = p.read_text(errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue
        if pat.search(text):
            hits.append(str(p.relative_to(ROOT)))
    if hits:
        bad(f"no portable field exists for credentials; possible secret in: {hits}")
    else:
        ok("no embedded credentials found in the package")


def main() -> int:
    check_path_safety()
    check_manifest()
    check_skills()
    check_mcp()
    check_no_secrets()

    print("Agent Plugins 1.0.0 conformance\n" + "=" * 60)
    for c in checks:
        print(f"  PASS  {c}")
    if errors:
        print()
        for e in errors:
            print(f"  FAIL  {e}")
        print(f"\n{len(errors)} violation(s).")
        return 1
    print(f"\n{len(checks)} checks passed. Package is conformant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
