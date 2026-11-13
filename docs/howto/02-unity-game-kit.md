---
title: How to use unity-game-kit
summary: "Unity game plugin: install per game, what each skill does (setup, doctor, check, content-check, asset, art-compare, build-android, store-shots), the 2D skills and modules, what it writes into a project, and the session-start hook."
keywords: [unity, game, android, comfyui, art, doctor, build, store screenshots, 2d]
status: draft
updated: 2026-11-14
---

# unity-game-kit (version 0.2.1)

Sets up a Unity game the same way every time and tells you what is still missing. Scope: Windows, Unity 6, Android, local ComfyUI art. Repository: https://github.com/Byterive/unity-game-kit.

## Install
In the game's folder: `/plugin install unity-game-kit@byterive-kit`, scope **project**. It works well with kickoff (profile `unity`). You need Python 3, and for art a local ComfyUI.

## Skills
| skill | say | does |
|---|---|---|
| `/game-setup` | "set up this project" | asks name, platforms, orientation, art style and 2D modules; copies the kit templates; runs the doctor |
| `/game-doctor` | "what is missing?" | checks the real project (Unity modules, packages, kit scripts, scene, tests, Unity CLI, Python, ComfyUI, Android settings) and walks you through the next fix |
| `/check` | "check the game" | compile errors, tests, level check, play-mode screenshot |
| `/content-check` | after changing levels or data | runs the game's own validator (level solver, data checker) |
| `/asset` | "new art", "redo this sprite" | art brief, ComfyUI options, you pick, iterate, the approved asset goes into the Unity project |
| `/art-compare` | "which model is best?" | checkpoint, LoRA and strength grid on one fixed prompt |
| `/build-android` | "put it on my phone", "Play build" | development APK installed over USB, or a signed AAB for Google Play |
| `/store-shots` | "store screenshots" | captures and frames screenshots and the feature graphic |

## 2D game skills
Seven are always on: `2d-code-hygiene`, `2d-game-feel`, `2d-ui-touch-mobile`, `2d-performance-android`, `2d-save-systems`, `2d-art-pipeline`, `2d-level-pacing-prototype`. `2d-pack-index` loads the optional modules a game lists in `modules` in `gamekit.json`: camera, audio, shaders, physics tuning, AI pathing, procedural, and at most one genre (puzzle, platformer, tower defense, roguelike, card). `/game-setup` asks which; `/game-doctor` warns about unknown names or two genres. Google Play figures in the pack are dated 2026-11-04 and must be re-checked before a release. Test the pack: `python scripts/test_modules.py`.

## Hook
SessionStart runs `scripts/doctor.py --brief`: one line when a project with `gamekit.json` needs attention; silent elsewhere.

## What it writes into a game
- `Unity/Assets/<Id>/Editor/`: automation commands, Android build (APK, signed AAB), `Checks/` (tests, play, screenshot).
- `automation/`: config, art bible, asset types, model settings, ComfyUI workflows and scripts, batch and APK install scripts, nightly job.
- `gamekit.json`: your setup answers and skipped checks (the kit's memory for that game).
- `.gitignore` lines and a `CLAUDE.md` section.
Existing files are never overwritten; they are listed as "kept" for a manual merge.

## Scripts (run by hand if needed)
```
python scripts/apply_template.py --root "F:/Games/My Game" --name "My Game" --dry-run
python scripts/doctor.py            (table; --json, --brief, --write-status)
```
Template placeholders: `__NAME__`, `__ID__`, `__LOWER__`, `__ENV__`, `__DATE__`.

## Models
Art generation uses models you download yourself under their own licences. The plugin ships no model files. `reference/comfyui-models.md` is a list of models and nodes for a 12 GB GPU, with links and a licences section; the licence notes are marked draft (checked 2026-10-18), so read each model's own licence before a game ships art made with it. ComfyUI runs on your machine; the kit talks to it only at `http://127.0.0.1:8188`. Background removal uses `rembg` and `onnxruntime`, which you install yourself with pip (`pip install -r automation/requirements.txt`); the kit does not bundle or auto-install them, and `rembg` downloads its model on first use.

## What runs on your machine
On session start a hook runs `scripts/doctor.py --brief` (Python standard library only). In a project with a `gamekit.json` it reads your project files, checks whether ComfyUI answers at `127.0.0.1:8188` and prints one line if setup items need attention. Outside a kit project it stays silent. The doctor prints install hints as text; it never runs them for you.

## Change the kit
Edit `templates/` (what goes into games), `skills/<name>/SKILL.md` (behaviour) or `scripts/doctor.py` (checks), then follow [07](07-add-or-change-a-skill.md). Existing games change only when you run `/game-setup` again (it adds missing files only).
