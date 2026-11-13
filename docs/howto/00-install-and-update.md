---
title: How to install and update the Byterive plugins
summary: Add the byterive-kit marketplace, install each plugin at the right scope (user, project, local), update, uninstall, and fix common problems.
keywords: [install, update, marketplace, scope, uninstall]
status: draft
updated: 2026-11-10
---

# Install and update

## 1. Add the marketplace (once per machine)
In a Claude Code session:
```
/plugin marketplace add Byterive/kit
```
or from a terminal: `claude plugin marketplace add Byterive/kit`. The marketplace is called **byterive-kit**; check it with `/plugin` and the Marketplaces tab.

## 2. Install a plugin
```
/plugin install <plugin>@byterive-kit
```
Claude Code asks for a **scope**:
| scope | stored in | use for |
|---|---|---|
| user | `~/.claude/settings.json` | tools you want in every folder (kickoff) |
| project | the project's `.claude/settings.json` (goes into git) | tools for one project and its collaborators (unity-game-kit in a game repo) |
| local | the project's `.claude/settings.local.json` (not in git) | trying a plugin in one project only you use |

Suggested scopes:
| plugin | scope |
|---|---|
| kickoff | user |
| guidebook | user, or project where you build guides |
| unity-game-kit | project, in each Unity game |
| idea2spec | user, or project where you test ideas |
| cachepulse | user |

Fewer user-wide plugins means fewer skill descriptions loaded in every session.

Install all five from a terminal:
```
claude plugin install kickoff@byterive-kit
claude plugin install guidebook@byterive-kit
claude plugin install unity-game-kit@byterive-kit
claude plugin install idea2spec@byterive-kit
claude plugin install cachepulse@byterive-kit
```
Add `--scope project` inside a project folder to install for that project only.

## 3. Use it
Skills are named `plugin:skill` (for example `kickoff:wrap-up-thread`). Commands appear as `/plugin:command`, for example `/kickoff:resume`.

## 4. Update
```
/plugin marketplace update byterive-kit
```
Then start a new session (terminal: `/reload-plugins`). A plugin updates when its `version` in `plugin.json` is raised.

## 5. Uninstall or disable
```
/plugin uninstall <plugin>@byterive-kit
/plugin disable <plugin>@byterive-kit      (keeps it installed, turns it off)
```
Remove the marketplace: `/plugin marketplace remove byterive-kit`. Removing and re-adding a marketplace removes its plugin installs, so install them again afterwards.

## Troubleshooting
| problem | fix |
|---|---|
| marketplace add fails | check the repository name, and that git can reach github.com; to test a local clone, add the path of the `kit` folder (the one holding `.claude-plugin/marketplace.json`) and run `claude plugin validate` on it |
| plugin update fails with a host-key error | git is using SSH; run `git config --global url."https://github.com/".insteadOf "git@github.com:"` |
| edits do not show | `/plugin marketplace update byterive-kit`, then a new session |
| a skill shows twice | it is installed from two places (for example a plugin and an old `.claude/skills` copy); remove one |

## Token cost
Always-on cost per session where a plugin is enabled (from `claude plugin details`): the plugin's skill and command descriptions. Skill bodies load only when used. Turn plugins off per project with `/kickoff:plugins`.
