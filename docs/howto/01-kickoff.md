---
title: How to use kickoff
summary: "The project system plugin: what each command, skill, hook and agent does, the normal flow (brief, audit, kickoff, daily work, wrap-up), profiles, plugin switches, tracking tiers and upgrades."
keywords: [kickoff, bootstrap, audit, wrapup, reindex, status, profiles, hooks, upgrade]
status: draft
updated: 2026-11-14
---

# kickoff (version 1.4.6)

Keeps a project readable for Claude at low token cost: every document has frontmatter (title, summary, keywords, status, updated), each folder has a generated `INDEX.md`, files have size budgets, and `PROJECT_STATUS.md` is the one-page dashboard. A new thread reads the index and status first and opens deeper files only when needed. Repository: https://github.com/Byterive/kickoff (its `GUIDE.md` is the longer guide).

Install: `/plugin install kickoff@byterive-kit`. Python 3 (standard library only) is needed for the tools.

## Commands
| command | does | when |
|---|---|---|
| `/kickoff:kickoff <profile or custom> [--dry-run]` | git state check, brief interview, plugin set, folders, `CLAUDE.md`, status, decisions, `NEXT.md`, `.gitignore`, hooks, health check (`/kickoff:bootstrap` is an alias) | start of a project |
| `/kickoff:resume` | reads `NEXT.md` and `PROJECT_STATUS.md` (and the plan if there is one); says where you stopped and the next 3 steps; reports when the last save was only a checkpoint (knowledge capture, reindex and budget checks still pending) | start of a thread |
| `/kickoff:status` | summarises `PROJECT_STATUS.md` | quick look |
| `/kickoff:checkpoint` | light mid-session save: always `NEXT.md` (marked `saved: checkpoint`) and `PROJECT_STATUS.md`; `REQUIREMENTS.md` and `DECISIONS.md` only if something new was decided; no reindex, budget check, knowledge capture or commit; warns about uncommitted changes; ends with one line saying `/clear` then `/resume` is safe | mid-session, before `/clear` |
| `/kickoff:wrapup` | saves knowledge, appends decisions, writes `NEXT.md` (marked `saved: wrapup`), reindexes, runs the verify commands, lists changed files | end of a thread |
| `/kickoff:doctor [--repair] [--dry-run]` | OK/WARN/FAIL/INFO health check: status freshness, `CLAUDE.md` size, budgets, plugin set, stale plugin installs, risky permissions, absolute local paths in tracked files, a profile changed in the kit since the project was set up, missing companion plugins, `profile_lib.py` missing from `tools/`, and whether the contribution line is allowed for this project; `--repair` prunes stale install records | before work, after changes |
| `/kickoff:upgrade` | lists what the current version adds to an older project, adds it after your yes, never overwrites; `--refresh-tools` replaces old tool copies after saving them to `.kickoff/backup/<date>/` | after updating the plugin |
| `/kickoff:plugins list\|on\|off\|find\|preset\|choose\|undo` | per-project plugin and skill switches | any time |
| `/kickoff:audit` | read-only inventory of an existing project into `_audit/` | before kickoff on a folder that has files |
| `/kickoff:reindex` | rebuilds `INDEX.md` files and checks budgets | before commit |
| `/kickoff:profiles` | lists profiles, families and aliases | choosing a profile |
| `/kickoff:new-profile` | drafts a profile from a finished project | after a project that could be reused |
| `/kickoff:undo` | removes what bootstrap created while it is unchanged (uses `.kickoff/before.json` and `manifest.json`) | a setup went wrong |

## Profiles and plugin sets
Built in, as families (a main profile plus secondaries that add only what differs; a secondary says `extends: <main>` and its tools merge with the main's):
- `backend` (secondaries `backend-go`, `backend-python`, `backend-rust`, `backend-node`; the old name `go-backend` is an alias of `backend-go`)
- `frontend` (`frontend-react`, `frontend-vue`)
- `data-research` (`trading-research` extends it)
- `utility` (`personal-utilities` extends it)
- stand-alone: `unity`, `netsuite`, `mobile-app`, `desktop-app`, `claude-plugin`, `custom`

Every profile has a plugin preset (`kit/presets/<profile>.json`, `{"keep": [...]}`), a `.gitignore` (`kit/gitignore/`) and a `## VS Code` section. Some also have a `## Companion plugins` section (see below). Plugin sets: **minimal** (only the always-keep list), **recommended** (the profile preset, default), **full** (keep all), or **select**. Everything else is turned off for that project only, in the git-ignored `.claude/settings.local.json`; `/kickoff:plugins undo` restores the previous state.

The always-keep list is only `kickoff`. To keep other plugins on in every project, put `{"keep": ["plugin-name"]}` in `~/.claude/kickoff/always.json` (per machine).

**Custom profile:** `/kickoff:kickoff custom` interviews you (at most 6 questions) and writes `.kickoff/profile.md` and `.kickoff/presets/custom.json`. Give it a name and it is also saved to `~/.claude/kickoff/profiles/<name>/` for reuse. Lookup order: project, user folder, plugin.

### Companion plugins
Some profiles list companion plugins: unity lists `unity` (Unity's own skills, third-party) and `unity-game-kit` (ours); frontend and desktop-app list `frontend-design`. They are third-party or separate plugins, optional and not endorsed or required by kickoff. Setup checks whether each is installed and offers the install command only after your yes for that plugin; nothing is installed automatically and kickoff works without them.

## Plugin and skill switches by hand
`python tools/proj_toggle.py list|on|off <names>|find <term>|preset <profile> --tier <t>|pick|localize|undo` (add `--dry-run` to preview). A turned-off plugin is removed; a turned-off skill is blocked but still listed. Changes apply in a new session (terminal: `/reload-plugins`). `localize` moves older choices out of the shared `settings.json`. Not available in Cowork projects.

## Skills (Claude picks them from your words)
project-bootstrap ("set up this project"), project-audit ("audit this project"), index-and-budget ("reindex", "check budgets"), wrap-up-thread ("wrap up", "hand over"), trading-test-logger (right after a backtest, trading-research profile).

## Hooks (automatic)
| event | does |
|---|---|
| Stop | rebuilds `INDEX.md` files when the folder has `PROJECT_STATUS.md`; never blocks |
| PreToolUse (Bash, PowerShell) | blocks `rm -rf` and `Remove-Item -Recurse -Force`; Claude must show what would be deleted and get your yes |
| PreToolUse (Bash, PowerShell) | blocks commits and pull requests that add Claude co-author or "Generated with" lines, unless the project chose Yes at setup (`.kickoff/attribution.json`) |

The Stop hook (`reindex_if_project.py`) is a local Python process with a 60 s limit and its output discarded. Each hook can be turned off on its own: `KICKOFF_DISABLED_HOOKS=reindex,coauthor,rmrf` (comma list in the environment or in `.claude/settings.json` env). `rmrf` blocks recursive forced deletes (Claude must show what would be deleted and get your yes); `coauthor` blocks commits and pull requests with a Claude co-author or "Generated with" line.

## Agents (call by name: "use the verifier agent to check this")
| agent | tools | does |
|---|---|---|
| `verifier` | Read, Grep, Glob, Bash | runs the repo's build, test and lint commands from `CLAUDE.md` and reports PASS, FAIL or NOT VERIFIED with real output; edits nothing |
| `backtest-skeptic` | Read, Grep, Glob | reviews a backtest or ML result for look-ahead, leakage, missing fees, small samples and overfitting; proposes PASSED, DOUBTFUL or FAILED |
| `netsuite-engineer` | Read, Grep, Glob, Edit, Write, Bash | sandbox-first NetSuite scripts, searches and workflows, with documentation and a rollback plan; never touches production |

## Optional tracking
Tiers in `.kickoff/fields.json`: `none` (default), `fields` (status, deadline and next keys in frontmatter) and `plan` (adds a shared `.kickoff/plan.json` with phases, steps, planned and actual dates and priority). Choose with `/kickoff:upgrade --fields none|fields|plan`; fill the plan with `python tools/plan.py init --profile <p>`. `/kickoff:wrapup` records status and evidence through `plan.py`; planned dates, priority and structure are yours. `/kickoff:resume` and `/kickoff:status` read the live plan; `/kickoff:doctor` validates it and warns about late steps. An older tier name in `fields.json` is read as `fields` (or `plan` when the file has `"plan": true`). Contracts: `kit/FIELDS_CONTRACT.md` and `kit/PLAN_SCHEMA.md` in the kickoff repo.

## Clarity rule and status sections
`/kickoff:upgrade` appends one marked block to `CLAUDE.md` and creates `REQUIREMENTS.md`: when a phase starts, a requirement is added or anything new needs a decision, Claude asks first with a numbered brief (options, recommendation, question), waits for an answer per number and records what it changes. On by default; `--clarity no` opts out. It is advice to Claude, not a blocking hook. `--sections yes` adds How to run, Setup, Data and Troubleshooting to `PROJECT_STATUS.md`, pre-filled from the README and repo and marked GUESSED. Choices are kept in `.kickoff/options.json`.

## Safety built in
- Kickoff starts with `git status`: uncommitted work means commit (or confirm a backup) first.
- The starter `.claude/settings.json` denies reading `.env*`, `secrets/`, `*.pem` and `*.key`.
- `CLAUDE.md` gets "How to verify" (real build, test and lint commands found in the repo, never invented), "Never do in this repo" and "Mistakes Claude made before", and is capped at 200 lines.
- Wrap-up runs the verify commands and ends with 3 things to try next time.
- After a history rewrite: `python tools/fix_hashes.py --map FILE [--apply]` fixes hash references.
- The release archive of the plugin leaves out the maintainer's working files (`_audit/`, `.kickoff/`, `.github/`, status and decision files): they are `export-ignore` in `.gitattributes`; `kit/` ships.

## Optional guide
`/kickoff:kickoff` can ask "Build a plain-language guide? No / Local" and writes `.kickoff/guide.json`. If the guidebook plugin is installed (see [13](13-guidebook.md)), wrap-up refreshes the guide and doctor checks it. A guide failure never fails kickoff or wrap-up.

## Normal flow
1. New folder: copy `kit/PROJECT_BRIEF.template.md` to `PROJECT_BRIEF.md` and fill it in (or let `/kickoff:kickoff` interview you).
2. Folder with files: `/kickoff:audit` first.
3. `/kickoff:kickoff <profile>`. After the profile is chosen, setup also offers (each after your yes, each optional): `.vscode/extensions.json` from the profile's VS Code section (merged, never overwritten, never installs anything); missing companion plugins (the install command runs only after you agree for that plugin); a plain-language guide; tracking fields; and the **Claude contribution line** question: "Add the Claude contribution line to commits and PRs? No (default) / Yes". Yes writes `.kickoff/attribution.json` and the `Git:` rule in `CLAUDE.md` (`python kit/tools/attribution.py <project> --set yes|no`); no git hook is installed; existing projects switch it by running that tool by hand (`/kickoff:upgrade` does not offer it).
4. Each thread: `/kickoff:resume` at the start, `/kickoff:wrapup` at the end.
5. Older projects: `/kickoff:upgrade` (dry run first).

## Tests
`python kit/tools/smoke_test.py` scaffolds a throwaway project and runs every suite. Others in `kit/tools/`: `test_hooks.py`, `test_plan.py`, `test_safety.py`, `test_privacy.py`, `test_upgrade143.py`, `test_families.py`, and the linter `check_profiles.py`. Each exits 1 on any failure. The workflow in the kickoff repo runs the smoke test on Windows and Linux (it passed on both for commit 212262c; it does not ship with the plugin). Full change list: `CHANGES.md` in the kickoff repo.
