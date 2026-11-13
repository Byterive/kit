"""Install a group of external plugins (listed in external-plugins.json) into one project, project scope.

Usage:
    python tools/install_external.py <group> <project folder> [--dry-run]
    python tools/install_external.py --list

Runs `claude plugin install <id> --scope project` inside the project folder for every plugin in the group.
Only writes the project's .claude/settings.json; no project files are touched.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "..", "external-plugins.json")


def main(argv):
    with open(CATALOG, encoding="utf-8") as f:
        cat = json.load(f)
    if not argv or argv[0] == "--list":
        for name, members in cat["groups"].items():
            cost = sum(cat["plugins"][m]["always_on_tokens"] for m in members)
            print(f"{name:24} ~{cost:>5} tok always-on  {', '.join(members)}")
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    group, project = argv[0], argv[1]
    dry = "--dry-run" in argv
    if group not in cat["groups"]:
        print(f"unknown group {group!r}; run with --list")
        return 2
    if not os.path.isdir(project):
        print(f"no such folder: {project}")
        return 2
    failed = 0
    for name in cat["groups"][group]:
        pid = cat["plugins"][name]["id"]
        cmd = ["claude", "plugin", "install", pid, "--scope", "project"]
        print(("DRY " if dry else "") + " ".join(cmd), f"(in {project})")
        if not dry:
            r = subprocess.run(cmd, cwd=project, capture_output=True, text=True, encoding="utf-8", shell=(os.name == "nt"))
            ok = r.returncode == 0
            failed += not ok
            print("  ok" if ok else f"  FAILED: {(r.stderr or r.stdout).strip()[-300:]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
