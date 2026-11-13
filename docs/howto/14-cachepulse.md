---
title: How to use cachepulse
summary: "The prompt-cache meter plugin (version 0.1.53): what it shows, the commands, where the TTL comes from, what it keeps private, and its limits."
keywords: [cachepulse, prompt cache, ttl, cache miss, claude code, meter]
status: draft
updated: 2026-11-14
---

# cachepulse (version 0.1.53, early)

Shows whether Claude Code reused its prompt cache for your last request, how long the cache may last, and, after a miss, the most likely cause with the evidence behind it. Repo: https://github.com/Byterive/cachepulse (MIT).

It uses Claude Code's early-access plugin API, which can change between releases without notice. A Claude Code update can break it until the plugin is updated.

## Install and needs
Claude Code with the early-access plugin API. Install: `/plugin marketplace add Byterive/kit`, then `/plugin install cachepulse@byterive-kit`. It makes no network requests, starts no processes and writes no files of its own.

## What you get
- **A band above the prompt:** the cache read share with a bar, the cache state and the TTL with its source, and the last request's read, wrote and new tokens. The bar's length is the read share; its colour is the time left on the cache.
- **A side panel:** where the TTL comes from, plan usage, recent requests, the latest miss with its cause, and a trend of read share against context size. Subagent requests count in the panel totals; the band follows the main conversation only.
- **An expiry toast:** one minute before a 5m cache may expire (and ten minutes before for a 1h cache). It says "may", never "will".
- **A model-switch warning:** switching model rewrites the cache. When Claude Code says the cache was warm, you get a warning at the switch.

## Commands
| command | does |
|---|---|
| `/cachepulse` | the text summary |
| `/cachepulse why` | the likely cause of the last miss or partial hit, with its evidence |
| `/cachepulse theme` | the colour theme |
| `/cachepulse config` | the full TTL source list with the winner marked, plus the subagent TTL |

## How a request is read
| result | meaning |
|---|---|
| Hit | 80% or more of the input was read from the cache (or some was read and nothing was written) |
| Partial | some read, under 80%, with something written to the cache |
| Miss | nothing was read |

Causes it can name: first request since it loaded, a new session, a `/clear`, a compaction, a model change, caching that appears to be off, a cache lifetime that ran out, new content after the cached part, or no cause found.

## Where the TTL comes from
It shows one TTL and its source, taking the first that has a value: your pick in cachepulse (display only), timing proof of 1h, `FORCE_PROMPT_CACHING_5M`, `CLAUDE_CODE_PROMPT_CACHE_TTL`, the `promptCacheTtl` setting, `ENABLE_PROMPT_CACHING_1H`, a timing hint of 5m, your account default.

## Rules it keeps
- Every figure is labelled observed, configured, inferred, estimate or unknown. Inferred values are guesses.
- It uses token counts and timestamps from Claude Code's events, kept in memory (200 requests at most). It also reads the TTL settings and variables above, the subagent TTL variable and setting, and the session usage Claude Code reports. Claude Code's plugin store keeps a few small values between sessions: theme, TTL pick, on or off choices, last model name, last reported TTL and account kind. Details are in the plugin's `PRIVACY.md`.
- It does not change Claude Code's settings, files or variables.

## Limits
- The cost line is a list-price estimate, not your bill. Prices come from a table in the plugin dated 2026-11-10; check Anthropic's published prices for current figures. Models without a price in the table are left out.
- It works only with what the early-access API provides. It does not claim to work with every Claude Code version or model.
