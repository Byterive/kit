---
title: How to use idea2spec
summary: "The idea validation plugin (version 0.1.1): what a run does, the commands, the files it writes, and what it does not do."
keywords: [idea2spec, idea validation, spec, interview, research, kill gate]
status: draft
updated: 2026-11-14
---

# idea2spec (version 0.1.1, early)

Helps you find out whether an idea is worth building before you build it. It asks a few questions, researches the nearest alternatives and how they earn, argues against your idea, scores it, and gives a verdict: GO, CLARIFY or KILL. It writes a spec only on GO. Folder and repo: `<plugins folder>\idea2spec\`, https://github.com/Byterive/idea2spec (MIT).

## Install and needs
Claude Code. Install: `/plugin marketplace add Byterive/kit`, then `/plugin install idea2spec@byterive-kit`. The research and red-team agents search and fetch pages from the public web.

## Commands
Start with `/idea2spec:run` and describe your idea.
| command | does |
|---|---|
| `/idea2spec:run` | the full workflow, one gate at a time |
| `/idea2spec:interview` | only the questions |
| `/idea2spec:research` | only the web research and the evidence ledger (each fact is labelled READ, RECALLED or UNVERIFIED) |
| `/idea2spec:score` | red team, scorecard and verdict; `--after-test` re-scores with real test results (PROCEED, ITERATE or KILL) |
| `/idea2spec:improve` | after a KILL or CLARIFY: testable ways to improve the idea, each tied to evidence, plus a "stay killed" option |
| `/idea2spec:spec` | writes the spec (needs a GO or your recorded override) |
| `/idea2spec:review` | checks the spec against a checklist |
| `/idea2spec:export` | opt-in: a stories folder or an issues list, as local files |

## What you get
Files in `idea2spec/<NNN-slug>/`, in the folder where you ran it: `interview.md`, `00-evidence.md`, `01-decision.md` (scorecard, case against, verdict, cheapest test, kill criteria) and, on GO, `spec.md`. It shows you the folder path and waits for your yes before the first file is written. A KILL is a good outcome: it saved the build time.

## Rules it keeps
- The first question is about privacy: search with generalized terms only (the default), with your exact wording, or not at all.
- Only READ facts can lift a score.
- GO means the cheapest test is worth running, not that the idea will succeed.
- It runs no code (the plugin is Markdown only: skills and agent definitions, no scripts, no hooks), publishes nothing and asks for no passwords or keys.

## Known limits
Quotes are page-fetch extracts, not word for word. The 10-of-14 GO threshold is a starting guess. In claude.ai chat and Cowork it runs in lite mode, where one conversation does every step and a GO shows as "GO (unaudited)".

## More
The plugin's own `README.md` and `PRIVACY.md`.
