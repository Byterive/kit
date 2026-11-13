#!/usr/bin/env python3
"""Check documentation/code budgets (stdlib only). Exit code 1 on any violation.

Usage: python tools/check_budgets.py [project_root] [--profile NAME]
Budgets come from tools/budgets.json (optionally overridden per profile).
Checks: frontmatter present + required fields non-empty, md length, md files per
folder, code file length. No micro-limits on headings/paragraphs/comments.
"""
import json
import os
import re
import sys

args = [a for a in sys.argv[1:]]
profile = None
if "--profile" in args:
    i = args.index("--profile")
    profile = args[i + 1]
    del args[i:i + 2]
ROOT = os.path.abspath(args[0]) if args else os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
BASE_SKIP = {".git", "node_modules", "Library", "Temp", "Logs", "obj", "bin",
             "__pycache__", ".venv", "venv", "vendor", "_inbox"}


def load():
    with open(os.path.join(HERE, "budgets.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    if profile:
        ov = cfg.get("profile_overrides", {}).get(profile, {})
        for k, v in ov.items():
            cfg[k] = (cfg.get(k, []) + v) if isinstance(v, list) else v
    return cfg


def main():
    cfg = load()
    skip = BASE_SKIP | set(cfg.get("skip_dirs", []))
    errors = []
    for cur, dirnames, files in os.walk(ROOT):
        rel_cur = os.path.relpath(cur, ROOT).replace(os.sep, "/")
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")
                       and (rel_cur == "." and d or f"{rel_cur}/{d}") not in skip]
        mds = [f for f in files if f.endswith(".md") and f != "INDEX.md"]
        if len(mds) > cfg["max_md_per_folder"]:
            errors.append(f"{rel_cur}: {len(mds)} .md files (max {cfg['max_md_per_folder']}); "
                          "split into subfolders")
        for f in files:
            path = os.path.join(cur, f)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            ext = os.path.splitext(f)[1].lower()
            if f.endswith(".md") and f != "INDEX.md":
                check_md(path, rel, f, cfg, errors)
            elif ext in cfg["code_extensions"]:
                n = count_lines(path)
                if n > cfg["max_code_lines"]:
                    errors.append(f"{rel}: {n} lines (max {cfg['max_code_lines']}); split the file")
    if errors:
        print("BUDGET VIOLATIONS:")
        for e in errors:
            print("  - " + e)
        sys.exit(1)
    print("check_budgets: OK")


def count_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def check_md(path, rel, name, cfg, errors):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    lines = text.count("\n") + 1
    if lines > cfg["max_md_lines"]:
        errors.append(f"{rel}: {lines} lines (max {cfg['max_md_lines']}); split or condense")
    if name in cfg.get("exempt_files", []):
        return
    m = FM.match(text)
    if not m:
        errors.append(f"{rel}: missing frontmatter")
        return
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for field in cfg["required_frontmatter"]:
        if not meta.get(field):
            errors.append(f"{rel}: frontmatter field '{field}' missing or empty")


if __name__ == "__main__":
    main()
