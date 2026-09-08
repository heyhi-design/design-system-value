---
title: Populate-from-data runbook
kit: design-system-value-kit
artifact: collectors/populate-runbook
date: 2026-09-08
classification: unclassified
---

# Populate-from-data runbook

How to take the four value-surface screens (the exec one-pager, team view, event
ledger, and leading feed) and fill them with one design system's own numbers, so
the same template serves any design system without redrawing it. The result is a
static mockup: it is populated once per run, refreshed on demand, not bound live
to a data source. Figma text cannot bind to a data feed, so "refresh" means
running this again.

Read this beside `screen-data-bindings.md` (which slot shows what), `metric-source-map.md`
(where each number comes from), and the collectors `runbook.md` (how the design-side
adapters produce rows). The live leadership surface is still a BI tool reading
artifact 02; these screens are the readable, brandable companion to it.

## What is generic and what is per target

- **Generic (reused for every design system):** the binding contract
  (`screen-data-bindings.json`), the resolver (`populate_screens.py`), and the
  apply script (`figma_apply.js`). No design system, file key, or number is baked
  into any of them.
- **Per target (supplied each run):** the data payload (one design system's
  numbers), the target Figma file key, and the per-file census
  (`screen-census.json`, the node ids in that file). The payload and the census
  are the two inputs you change to point the template at a different design system.

## The three steps

### 1. Collect

Assemble one payload of the design system's numbers, in the shape of
`sample-data.json`. The design-side rows (component and token adoption) come from
the live adapters once their access exists; the cost, hours, quality, engagement,
and risk rows are filled from code scans, a production sampler, an issue tracker,
a survey, and finance data, exactly as `metric-source-map.md` lays out. A metric
the design system has not instrumented yet is simply left out of the payload; the
next step renders it as a visible gap rather than inventing a number.

Two sample payloads ship with the kit, both fictional design systems:

- `sample-data.json` is fully instrumented (every slot fills).
- `sample-data-atlas.json` is a second, distinct design system that has not
  instrumented defects, so it shows the source-gap behavior.

### 2. Resolve (credential-free)

From `kit/collectors/`:

```
python3 populate_screens.py --check                          # structural coverage: every slot bound, no contract error
python3 populate_screens.py --data sample-data.json          # resolved {screen: {slot: string}} + source_gaps
python3 populate_screens.py --data sample-data.json --apply-plan --out apply-plan.json
```

`--check` confirms every text slot on the four screens has a binding and every
binding has a slot, and reports the run-time source-gaps for the payload (it does
not fail on gaps; a gap is a real state of a design system, not an error).
`--apply-plan` joins the resolved strings with the census node ids and writes the
op list the apply step consumes. Both run with no token and no network.

A slot whose payload value is absent renders the placeholder (`—` by default) and
is listed in `source_gaps`. The resolver never fills a gap with a guessed number.

### 3. Apply (the design-tool step)

This step writes into the target Figma file. It sets text only. It never changes
a fill, a stroke, or a variable binding, so the file's light and dark theming and
its zero-raw-literals guarantee are preserved.

1. Load the `figma-use` skill (required before any `use_figma` call).
2. Open `figma_apply.js` and paste the `ops` list from `apply-plan.json` into it.
3. Run it with `use_figma`, passing the target design system's own file key. The
   file key is a parameter of the call, never hardcoded in the script.
4. Screenshot the screens in light and dark and confirm every bound slot carries
   the new numbers and no slot still shows the previous data.

For a target file that is not the reference template, first regenerate
`screen-census.json` against that file with the design tool's `get_metadata`, then
resolve and apply as above. Node ids are file-specific; the slot ids are stable.

## UPDATE or BUILD

There are two ways to get the screens into a target file.

- **UPDATE** refreshes screens that already exist in the file (a duplicate of the
  reference template, or screens built once and re-run each period). It needs no
  publishing step. This is the default and the path the three steps above follow.
- **BUILD** assembles the screens from scratch by instancing the published
  component library (the metric tile and delta chip) into the design system's own
  file. Use it the first time a design system adopts the template and has no
  screens yet. BUILD needs the component library published so its components can
  be imported by key; publishing the library is an operator step. Where the
  library is unpublished, duplicate the reference template and use UPDATE instead.

## The honesty rules, restated

- A number the design system has not measured is a visible gap, never a guess.
- The screens carry the design system's own numbers, its own team names, its own
  proof events. Nothing from the template's example data survives a run.
- The screens are a static picture as of the run. Every number on them should
  trace to the payload, and the payload should trace to the sources in
  `metric-source-map.md`.
