---
title: The design-tool template
kit: design-system-value-kit
artifact: figma/README
date: 2026-09-08
classification: unclassified
---

# The design-tool template

The four value-surface screens (exec one-pager, team view, event ledger, leading feed) exist as a theme-able template in a design tool: two variable collections (Primitives, and Semantic with Light and Dark modes), two components (Stat tile, Delta chip), and the four screens with every fill, stroke, padding, and radius bound to a Semantic variable. The template is not a file in this repository. This folder gives it three independent ways to survive and travel, cheapest first: **duplicate** an existing copy, **restore** a copy that has been populated back to its template state, or **rebuild** it from scratch in a blank file from the scripts here.

Everything here is generic: scripts address variables and components by name, never by id, and no file key or design-system name is baked in. The scripts run inside the design tool's script runner (the Figma Plugin API through the `use_figma` tool, with its `figma-use` skill loaded first), one file at a time, on whatever file key you pass to the tool.

## Files

| File | What it does |
|---|---|
| `emit-variables-script.py` | Generates `build-variables.js` from `../tokens/neutral.tokens.json`. Run after any token change; `--check` fails when the script is stale |
| `build-variables.js` | Creates or updates the Primitives and Semantic collections (Light + Dark, aliases, scopes, code syntax). Idempotent. Generated, do not edit |
| `build-components.js` | Creates the Stat tile and Delta chip, bound by name. Refuses to run if they already exist on the page |
| `build-screens.js` | Builds the four screens from the components over the variables, with the template's example strings. `BUILD` selects which screens |
| `census-walk.js` | Read-only. Walks the screens and returns the ordered text and instance list that `../collectors/census_from_walk.py` turns into `screen-census.json` for that file |
| `check-build-scripts.py` | Static check, no design tool needed: the emitter is current, every script parses, every bound variable name exists in the token set. Part of `scripts/smoke.sh` |
| `emit_variables.py` | Import shim so the checker can reuse the emitter's token reader; not run directly |

## Duplicate (the cheapest path)

If a copy of the template exists that you can open, duplicate it in the design tool (File menu, Duplicate) into your own team or drafts. Then, in the copy:

1. Run `census-walk.js` through the script runner and save the returned JSON as `walk.json` in this folder (it is ignored by git and by the manifest, as are `apply-plan.json` and `restore.json` in `../collectors/`).
2. `python3 ../collectors/census_from_walk.py walk.json --out ../collectors/screen-census.json` (from this folder). The census records the node ids of your copy and, for every slot, the string it currently shows, so the copy can be restored later. Instances are matched by their main component's name, so a renamed instance still censuses.
3. Follow `../collectors/populate-runbook.md` to fill the screens with your design system's numbers.

Node ids are file-specific; slot ids are stable. A census taken on a fresh copy is also its restore point.

## Restore (return a populated copy to template state)

`populate_screens.py --restore-template --apply-plan --out restore.json` emits an apply-plan that sets every slot back to the string recorded as `text` in the census. Run it through `../collectors/figma_apply.js` exactly like a populate. It writes text only, so theming and bindings are untouched. If a slot has no recorded text the resolver says so and skips it; it never invents a value.

## Rebuild (from scratch, in a blank file)

Order matters. Each step is one script-runner call on the same file; load the `figma-use` skill first; the target needs a plan tier that allows two variable modes.

1. **Variables.** Paste `build-variables.js`. Expect 49 primitives and 16 semantic roles, modes Light and Dark.
2. **Components.** Paste `build-components.js`. Expect a 77×23 Delta chip and a 230×123 Stat tile.
3. **Screens.** Paste `build-screens.js` (all four at once, or set `BUILD` to a subset). The two builders read variables only from the collections named Primitives and Semantic, so a file that already carries a `color/text` in some other collection is not a problem; a file with a second collection of either name is. Expect four frames whose names start `Screen 1`, `Screen 2`, `Screen 6`, and `Screen 7` (each followed by the screen's title), 880 / 820 / 780 / 720 wide.
4. **Prove it.** Count solid paints with an unbound color across the page (the zero-raw-literals check) and screenshot one screen with the Semantic collection set to Dark on the frame, then Light. Every fill and stroke must change with the mode.
5. **Census, then populate.** Steps 1 and 2 of Duplicate, then the populate runbook.

What the recipe reproduces: the committed four screens and their two components, as recorded from the reference template on 2026-09-08. It does not reproduce the other seven screens in the eleven-screen inventory (`../03-screen-specs.md`), which were never built. Fonts: Inter Regular and Bold.

## Verification record

Proven 2026-09-08 in a fresh blank file: variables 49 + 16 (Light, Dark); components 77×23 and 230×123; screens 880×957, 820×368, 780×335, 720×426 (two match the reference exactly; the other two differ by text-wrap height only); 203 solid paints, 0 unbound; both modes render; a census taken with `census-walk.js` joined cleanly with the contract (129 slots); a second sample payload (`sample-data-atlas.json`) populated every slot with its nine source-gaps shown as placeholders and none of the template's numbers, names, or events left (the 25 static slots, such as column headers and method notes, read the same for every design system by design).

## After a token change

1. Edit `../tokens/neutral.tokens.json`, re-run `../tokens/check-contrast.py`.
2. `python3 emit-variables-script.py` to regenerate `build-variables.js`.
3. Re-run `build-variables.js` on every live copy of the template: it updates values in place and never duplicates a variable.
4. `python3 check-build-scripts.py`, then `bash ../../scripts/smoke.sh`.
