---
title: How to use guidebook
summary: "Plain-language guide plugin: what it reads and writes, the init, status, update and serve commands, the safety rules, and how it works with kickoff."
keywords: [guidebook, guide, documentation, plain-language, html, kickoff]
status: draft
updated: 2026-11-14
---

# guidebook (version 0.2.1, early)

Reads a project and writes guides for different readers (for example a client, a new teammate or a maintainer), builds them as web pages, and refreshes them when the project changes. It reads the project and never changes it; it writes only `.guidebook/`, `docs/guide-src/` and the built `docs/guide/`. Repository: https://github.com/Byterive/guidebook.

## Install and needs
`/plugin install guidebook@byterive-kit`. Python 3.10+ and `pip install markdown`. Claude Code is optional: without it guidebook writes deterministic pages (`--no-model`); with it, the model steps send scrubbed project text to Claude through `claude -p` and cache the answers in `<project>/.guidebook/cache`. `--no-model` sends nothing.

## Command
`/guidebook:guide <subcommand>`, or from a clone `python bin/guidebook <subcommand> <project folder>`. The plugin command runs `bin/guidebook`, so the plugin installs in Claude Code only (not in claude.ai chat or Cowork).
| subcommand | does | result |
|---|---|---|
| `init` | reads the project and proposes guide versions with reasons (writes nothing); after your approval (`--yes`) writes `.guidebook/guide.json` and builds the first guide; `--dry-run` lists every file | the proposal, then `docs/guide/index.html` |
| `status` | checks whether the guide is fresh | fresh or stale and why; exit code 1 when stale (information, not an error) |
| `update` | refreshes only what changed; `--no-model`, `--dry-run`, `--max-calls N` | pages written, proposals, model calls made, HTML rebuilt |
| `serve` | local site at http://127.0.0.1:8765 with a "Check and update" button | a browsable guide |

Pages land in `docs/guide-src/<version>/` and the web version in `docs/guide/`. If you edited a generated page and its sources changed too, the new text goes to `<page>.proposed.md` and your page is left alone.

## New in 0.2.0: four task pages
Besides status, decisions and reference pages, the guide gets one page each for How to run, Setup (under `1-start/`), and Data, Troubleshooting (under `4-reference/`), built from the matching sections of `PROJECT_STATUS.md`.
- Each page shows a CONFIRMED, GUESSED or UNKNOWN badge. A section that says UNKNOWN becomes a page that shows "UNKNOWN, question: ...". A project with no such heading gets no page.
- Steps are numbered and each is followed by "What you should see" (or "not known").
- Troubleshooting is a table: what you see, why, what to do.
- The home page of the quick-start version gets a short box (up to 5 items) built from How to run and Setup, shown only when both are confirmed.
- Only the changed section's page is rewritten.

## Rules it keeps
- Skips secrets, `.env*`, keys and git-ignored files, and scrubs emails, tokens and private paths before anything is stored, sent or written.
- Unknown stays "not known". Status words are PASSED, FAILED, DOUBTFUL, UNTESTED and UNKNOWN.

## With kickoff
`/kickoff:kickoff` can set up a guide, `/kickoff:wrapup` refreshes it and `/kickoff:doctor` checks it (see [01](01-kickoff.md)). The contract is `docs/kickoff-contract.md` in the guidebook repository.
