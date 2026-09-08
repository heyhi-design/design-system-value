<!-- classification: unclassified; generic release, no internal references permitted (see scripts/check-no-internal-refs.sh) -->
# Design System Value

How a design system proves its worth to the people who fund it, and the artifacts a team uses to do it.

This repository holds three things:

| Folder | What it is | Start here if |
|---|---|---|
| `docs/making-the-case-for-a-design-system.md` | The field guide. What leadership looks for, what the published evidence actually supports (with provenance grades), the three-ledger measurement architecture, the story shape, and how to make the evidence retrievable by anyone. | You need to understand the problem before building anything |
| `docs/how-value-gets-shown-to-leadership.md` | The visual survey. Dashboards, calculators, reports, and decks that render design-system value today, in design systems and in adjacent fields, with a pattern library and an eleven-screen inventory. Contact sheets of the captured screens are in `docs/assets/`. | You are designing or embedding a reporting surface |
| `SETUP.md` + `scripts/` | Requirements, install, the command form, and the one-command smoke check (`bash scripts/smoke.sh`). `MANIFEST.txt` lists every file with its hash. | You are setting this up on a new machine, or you changed something |
| `kit/` | The Design System Value Kit. Metric definitions, a data model verified on PostgreSQL, screen specs with wireframes, an instrumentation playbook, an overlay spec, deck skeletons, protocols for events and studies, an adoption scorecard, a sources list, a 26-week plan skeleton, a neutral theme-able token set (`kit/tokens/`), and an operable collectors layer (`kit/collectors/`). | You have been asked to actually do it |

Everything is generic. No company, tool, or consultancy is assumed. Where a choice depends on your organization, the artifact marks it **[decision]** (a judgment someone must make) or **[fill]** (a fact someone must supply).

## The argument in five lines

1. Leadership asks three things: what did we get, compared to what, and what do you want me to decide.
2. Systems lose funding for perceived value more often than for actual value; the fix is an instrument, not a better deck.
3. Numbers that survive an executive's questions are small, sourced, and ranged. Hard savings, soft savings, and cost avoidance stay on separate lines.
4. Adoption lags. Engagement, contribution, and sponsor participation lead it by months.
5. Report like a product, not a project, and put the numbers where leadership already looks.

## How to use the kit

Read `kit/README.md`. The short version: define the cost ledger and three metrics before measuring anything; baseline; ship the overlay; instrument the next natural event; deliver a one-page report on a fixed date with two periods of data; then add the team view and the feed. `kit/PLAN-skeleton.md` turns that into phases, gates, workstreams, and the ten decisions only a person can take.

## Provenance

The evidence in the field guide carries grades: A (controlled or primary study with stated method and sample), B (first-person practitioner account with a described method), C (vendor, analyst, or self-report), D (unsourced, circulates widely), X (unverifiable or contradicted; do not cite). Every precedent the kit names has a public URL in `kit/SOURCES.md`. The contact sheets in `docs/assets/` are crops of public pages captured for study; they are not for redistribution outside this repository.

## Integrity check

`scripts/smoke.sh` runs every credential-free check in the repository, ending with `scripts/check-no-internal-refs.sh`, which scans for references that should never appear in a generic release. Run it before publishing any change:

```bash
bash scripts/smoke.sh
```

To run only the genericity scan: `scripts/check-no-internal-refs.sh`. After any edit, regenerate the manifest with `bash scripts/manifest.sh --write` (see `SETUP.md`).

## Status

Version 0.3.1, 2026-09-08 (0.3 content; the 0.3.1 packaging adds `SETUP.md`, the smoke check, and the manifest). The kit has been through a structured design-method review as a generic upgrade-in-place and now carries a neutral, theme-able design-token set (`kit/tokens/`, light and dark, WCAG-gated) and an operable collectors layer (`kit/collectors/`, credential-free dry-run plus drop-in adapter stubs); all documents have been through independent adversarial review, and the data model executes against PostgreSQL 17 with a seeded probe. See `CHANGELOG.md`.
