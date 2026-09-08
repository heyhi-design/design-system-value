---
title: Screen data bindings
kit: design-system-value-kit
artifact: collectors/screen-data-bindings
date: 2026-09-08
classification: unclassified
---

# Screen data bindings

The contract that turns the four value-surface screens into a template any design
system can fill with its own numbers. For every text slot on the exec one-pager,
team view, event ledger, and leading feed, it names the source (a metric, a
value-ledger element, an event, a team, a feed item, a design-system field, or
static chrome) and the display template. It extends the data-binding lines in
`03-screen-specs.md` and the metric map in `metric-source-map.md` down to the
level of individual text nodes.

The machine mirror is `screen-data-bindings.json` (the exhaustive, resolver-read
list of all 129 slots). This document is the readable summary; the resolver
(`populate_screens.py`) and the apply step read the JSON.

## Two files, one join

The binding is deliberately split so the contract stays generic:

- **`screen-data-bindings.json`** carries the slot, its source, and its template.
  It has no node ids, so it is the same for every design system.
- **`screen-census.json`** carries, per target file, the text-node id behind each
  slot. It is regenerated for each file with the design tool's `get_metadata`.

The two join on the slot id. A slot's meaning is stable; only its address in a
given file changes.

## Template syntax

A template is a string with `{path|format}` tokens. `path` is a dotted path into
the payload; numeric segments index lists (`teams.0.coverage`). A trailing `?`
(`{teams.0.cov_suffix?}`) marks the token optional: an absent or empty value
renders empty and flags no gap. Without `?`, an absent, null, or empty value
renders the placeholder (`—` by default) and flags the slot as a run-time
source-gap. A template with no tokens is a static slot and renders unchanged.

Formats: `pct1` (one-decimal percent), `pct0` (integer percent), `pts_signed`
(signed points, `+5.2 pts`), and `str` (pass-through, the default). The resolver
formats where a format is declared and passes operator-supplied display strings
through unchanged; it never reformats a string the payload already shaped.

## What each screen shows

Every number below traces to a metric id from `01-metric-definitions-pack.md`, so
each slot on a screen links back to a defined metric, a value-ledger row, or an
event. Static chrome (section titles, column headers, the metric-name labels, the
"Screen N of 11" footers) is marked `static` and does not change between design
systems.

### Screen 1, exec one-pager

| Group | Slots | Source |
|---|---|---|
| Title and meta | system name, period, owner, timestamp | `design_system` |
| Headline | coverage value, delta chip, baseline/now/target line, trend caption | M1 |
| Scorecard tiles | cost per team; override rate; defects on vs off; engagement | M9, M2, M5, M6 (value and sub each; the metric-name label is static) |
| Proof card | event, window, before/after, last/this time with source, saved range, dollarized line, quote | the most recent event (artifact 07) |
| What we are not counting | three named unquantified benefits | narrative (N1) |
| Risk and breaches | a11y pass-rate line; key-person line; breach line | M5, R2, M1 |
| The decision | the ask; the if-no consequence | the team's decision |
| Footer | definitions and data locations | `design_system` |

### Screen 2, team view

One row per team: team name, coverage (M1) with an optional breach marker,
override rate (M2), defects (M5), engagement (M6), owner. The subtitle carries the
team count. Column headers are static.

### Screen 6, event ledger

One row per event: event name, last time, this time, saved range, method. An open
event carries the same slots with its placeholder content (`—`, `instrument
first`, `open`) supplied in the payload. Column headers and the method footnote
are static.

### Screen 7, leading feed

One row per feed item: the type chip, the headline, the since-and-owner subline,
and (on the breach row) a decision chip. All bound to the feed list.

## Source-gaps: the honesty rule

No slot is permanently unbound. Every slot maps to a source. A source-gap is a
property of a given payload, not of the contract: when a design system has not
instrumented a metric (defects and accessibility are the common case, exactly as
`metric-source-map.md` predicts), the slots that draw on it render the placeholder
and are listed in the resolver's `source_gaps`. The generator never fills a gap
with a guessed number. The second sample payload (`sample-data-atlas.json`) has no
defects instrumentation and shows this behavior on nine slots.

## Regenerating for a new target file

The slot ids are stable, so `screen-data-bindings.json` is reused unchanged. Only
`screen-census.json` is regenerated: run the design tool's `get_metadata` on the
target file, read the text-node id behind each slot, and rewrite the census. The
scorecard tiles and the delta chip are component instances; their text descendants
resolve in document order (a tile exposes label, value, sub; a chip exposes a
single value), which the census records under `components`.
