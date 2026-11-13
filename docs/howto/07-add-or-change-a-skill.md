---
title: How to add or change a skill, command, agent, hook or plugin
summary: "Step-by-step for changing a Byterive plugin or adding a new one: folder shapes, the plugin manifest, the marketplace entry, validation, version bump, how-to update and commit."
keywords: [add skill, new plugin, command, agent, hook, validate, marketplace]
status: draft
updated: 2026-11-10
---

# Add or change a skill, command, agent, hook or plugin

Each plugin is its own git repository next to the `kit` folder; `kit` lists them in `kit.json` and generates `.claude-plugin/marketplace.json`.

## 1. Pick the home
| it is about | put it in |
|---|---|
| project structure, status, indexes, hand-over | kickoff |
| plain-language guides | guidebook |
| Unity games | unity-game-kit |
| something only one project needs | that project's `.claude/skills/`, not a plugin |
| a new area | a new plugin (section 4) |

## 2. Shapes
```
<plugin>/skills/<skill-name>/SKILL.md        (+ references/, scripts/ if needed)
<plugin>/commands/<name>.md                  (slash command)
<plugin>/agents/<name>.md                    (subagent)
<plugin>/hooks/hooks.json                    (+ the script it runs)
```
`SKILL.md` starts with:
```yaml
---
name: skill-name
description: What it does. Use when <the words or situation that should trigger it>.
---
```
The description decides when Claude uses the skill: say what it does and when, in one or two sentences. Keep the body short; move long detail into `references/` files the skill points to.

Command files: frontmatter `description:` and optional `argument-hint:`; the body is the prompt and `$ARGUMENTS` is what you typed after the command. Agent files: frontmatter `name:`, `description:` (when to use it) and optional `tools:`; the body is the agent's system prompt. Hook scripts: use `${CLAUDE_PLUGIN_ROOT}` for paths and keep them fast and silent when they do not apply.

## 3. From another folder or the internet
- Read every file before copying (no unknown scripts).
- Third-party: record source, commit and licence in the plugin's `THIRD_PARTY.md` first, and keep the upstream LICENSE.

## 4. New plugin
Create a repository `Byterive/<name>` with `.claude-plugin/plugin.json`:
```json
{ "name": "<name>", "version": "0.1.0", "description": "<one sentence>", "author": { "name": "Junaid Iqbal", "url": "https://byterive.com" }, "homepage": "https://byterive.com", "repository": "https://github.com/Byterive/<name>", "license": "MIT" }
```
Add it to `kit.json`, run `python tools/kit.py sources github`, add a row to `README.md` and a numbered how-to in `docs/howto/`. Add a LICENSE ("Copyright (c) 2026 Junaid Iqbal (Byterive)") and a README.

## 5. Finish
1. `python tools/kit.py validate` (in the kit folder) checks every plugin and the marketplace.
2. Try it: `claude --plugin-dir <path to the plugin>` in a test folder.
3. Raise `version` in `plugin.json` if behaviour changed.
4. Update the plugin's how-to in the same commit.
5. Commit in the plugin's own repository, push, then `/plugin marketplace update byterive-kit`.
