#!/usr/bin/env python3
"""Manage the byterive-kit marketplace from kit.json (single source of truth).

  python tools/kit.py sources local|github   rewrite .claude-plugin/marketplace.json (local = file:// git repos, github = Byterive/<repo>)
  python tools/kit.py status                 git state of every plugin repo (branch, uncommitted files, remote)
  python tools/kit.py validate               claude plugin validate on every plugin repo and on this marketplace, plus the withheld check
  maintainer commands (contract, gate, facts, decisions, state) exist only in the maintainer's working copy, not in the release
  python tools/kit.py withheld               only the withheld check: no withheld plugin is listed in marketplace.json and each withheld repo is private on GitHub
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cfg = json.loads((ROOT / "kit.json").read_text(encoding="utf-8"))
# Private, git-ignored list of plugins that must stay out of the marketplace and out of public view (kit.private.json).
_priv = ROOT / "kit.private.json"
if _priv.exists():
    cfg["withheld"] = json.loads(_priv.read_text(encoding="utf-8")).get("withheld", [])


def local(p):
    """Plugin repos sit next to this folder: <plugins folder>/<name>."""
    return str(ROOT.parent / p["name"])


def sources(mode):
    out = []
    for p in cfg["plugins"]:
        if mode == "local":
            src = {"source": "url", "url": "file:///" + Path(local(p)).as_posix()}
        else:
            src = {"source": "github", "repo": p["repo"]}
        out.append({"name": p["name"], "description": p["description"], "source": src})
    mk = {"name": cfg["marketplace"], "description": cfg.get("description", cfg["owner"] + " plugins for Claude Code"), "owner": {"name": cfg["owner"]},
          "plugins": out}
    (ROOT / ".claude-plugin" / "marketplace.json").write_text(json.dumps(mk, indent=2) + "\n", encoding="utf-8")
    cfg["mode"] = mode
    public = {k: v for k, v in cfg.items() if k != "withheld"}  # the withheld list lives only in kit.private.json
    (ROOT / "kit.json").write_text(json.dumps(public, indent=2) + "\n", encoding="utf-8")
    print(f"marketplace.json written ({mode}, {len(out)} plugins)")


def git(path, *a):
    return subprocess.run(["git", "-C", path, *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


def status():
    for p in cfg["plugins"]:
        path = local(p)
        if not Path(path).exists():
            print(f"MISSING {p['name']}  {path}")
            continue
        dirty = len(git(path, "status", "--short").splitlines())
        remote = git(path, "remote", "get-url", "origin") or "no remote"
        print(f"{p['name']:<22} {git(path, 'branch', '--show-current'):<6} {dirty} uncommitted  {remote}")


def withheld_check():
    """Withheld plugins must not be listed in marketplace.json and their GitHub repos must stay private. Returns the number of problems."""
    listed = {p["name"] for p in json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["plugins"]}
    bad = 0
    for w in cfg.get("withheld", []):
        if w["name"] in listed or w["name"] in {p["name"] for p in cfg["plugins"]}:
            print(f"FAIL withheld {w['name']}: listed in the marketplace")
            bad += 1
            continue
        try:
            r = subprocess.run(["gh", "api", f"repos/{w['repo']}", "--jq", ".private"], capture_output=True, text=True, timeout=30)
            out = (r.stdout or "").strip()
        except (OSError, subprocess.TimeoutExpired):
            out = ""
        if out == "false":
            print(f"FAIL withheld {w['name']}: the GitHub repo {w['repo']} is PUBLIC")
            bad += 1
        else:
            print(f"PASS withheld {w['name']}: not listed" + (", repo private" if out == "true" else ", repo visibility not checked (gh unavailable or not logged in)"))
    return bad


def validate():
    bad = withheld_check()
    for path in [local(p) for p in cfg["plugins"]] + [str(ROOT)]:
        r = subprocess.run(["claude", "plugin", "validate", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
        ok = "Validation passed" in (r.stdout or "")
        bad += not ok
        print(("PASS " if ok else "FAIL ") + Path(path).name)
    if (ROOT / "tools" / "contract.py").exists():
        rc = subprocess.run([sys.executable, str(ROOT / "tools" / "contract.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(("PASS " if rc.returncode == 0 else "FAIL ") + "contract: " + (rc.stdout.strip().splitlines() or [""])[-1])
        bad += rc.returncode != 0
    sys.exit(1 if bad else 0)


cmd = sys.argv[1] if len(sys.argv) > 1 else ""
if cmd == "sources" and len(sys.argv) > 2 and sys.argv[2] in ("local", "github"):
    sources(sys.argv[2])
elif cmd == "status":
    status()
elif cmd == "withheld":
    sys.exit(1 if withheld_check() else 0)
elif cmd == "validate":
    validate()
elif cmd in ("facts", "decisions", "state", "contract", "gate"):
    tool = ROOT / "tools" / ("facts.py" if cmd in ("facts", "decisions", "state") else cmd + ".py")
    if not tool.exists():
        sys.exit(f"{cmd}: maintainer command, not part of this release")
    sys.exit(subprocess.call([sys.executable, str(tool)] + (sys.argv[1:] if cmd in ("facts", "decisions", "state") else sys.argv[2:])))
else:
    sys.exit(__doc__)
