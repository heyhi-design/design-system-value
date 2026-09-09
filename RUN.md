<!-- classification: unclassified; generic release, no internal references permitted (see scripts/check-no-internal-refs.sh) -->
# Running the kit against a real design system

`SETUP.md` gets you a working checkout. This takes you the rest of the way:
from a checkout to a populated value story against a real design system. Every
step is generic and organization-configurable; nothing here assumes a
particular company, tool account, or design system.

The order matters, because later steps read what earlier steps produce. Run the
credential-free dry-run first, on any machine, before anyone hands over an
access token — it tells you the shape of the answer and what will stay a gap.

Commands follow the three-line form in `SETUP.md` (interpreter, working
directory, invocation). The working directory for the collector commands is
`kit/collectors/`.

## What you need in hand

- **A value store.** A PostgreSQL database you control, dedicated to this work.
  Do not point it at an unrelated production database.
- **The design tool's adoption access**, if you want the design-side
  adoption-over-time series: a plan tier that exposes the library analytics API
  and a token scoped to read it. Without it, the structural census (below) still
  gives you the design-side inventory, point-in-time.
- **The documentation platform's access**, if the design system is documented
  there: an account with the design system loaded and a personal access token.
- **A copy of the value-story template** in the design tool you can edit (see
  `kit/figma/README.md` — duplicate an existing copy, or rebuild it from the
  scripts there).

Tokens live only in your environment or a secret manager. No token, key, or
credential is ever written into a file in this repository. Each adapter reads
its token only from a named environment variable, only on a live run, and
refuses with a clear message otherwise.

## 0. Dry-run: see the shape of the answer

```
python3 dryrun.py --check
```

Every metric and every value-ledger row is classified as a named source or a
`source-gap`. Read the tail as the honest scope statement: the two named sources
(the design tool's analytics and the documentation platform) fill the
design-side adoption story; the cost, hours, quality, engagement, and risk
ledgers are gaps that need code-side, runtime, survey, or finance
instrumentation. This needs no token, no network, and no plan tier.

## 1. Stand up the value store

Apply the table definitions in `kit/02-data-model.md` to your dedicated
database, and create the views it defines (`v_exec_headline`, `v_team_view`).
Load the dimensions the facts reference first (`dim_team`, `dim_surface`,
`dim_metric_definition` — one row per published metric contract from
`kit/01-metric-definitions-pack.md`). Every number a screen shows is a `SELECT`
from a fact table or a view; nothing is computed in the presentation layer.

## 2. Collect the design-side adoption (design tool)

Re-confirm the analytics API surface against the current vendor documentation
before you rely on a shape. Then, in `kit/collectors/figma_adoption_adapter.py`:
fill the `CONFIG` block (the library file keys), set the token in the named
environment variable, flip `STATUS` to `active`, and implement the single
network seam the adapter leaves to you. Run it and load the rows:

```
python3 figma_adoption_adapter.py --live
```

The rows are keyed to the data-model tables by their `_table` field. Resolve
names to dimension ids, fill the required keys, and load with your own loader.
See `kit/collectors/runbook.md` and `kit/collectors/figma-adoption-adapter.md`.

## 3. Collect the documentation side (documentation platform)

Same shape, in `kit/collectors/supernova_adapter.py`: re-confirm the read
surface against the current vendor docs, fill the `CONFIG` block (workspace,
design-system, and version ids), set the token, flip `STATUS`, implement the one
read seam, then:

```
python3 supernova_adapter.py --live
```

Load the inventory rows. The documentation-coverage signal is a candidate
column the current data model does not yet have a table for; record it as the
schema gap it is, not a forced fit. See `kit/collectors/supernova-adapter.md`.

## 4. Structural census (the inventory the adapters do not supply)

The component, variable, and style inventory and the code crosswalk are a
separate, read-only step against the published design library. They do not
depend on a plan tier, and they feed the component dimension and the design-side
coverage counts. Run this after the library exists; reconcile its rows with the
documentation-platform inventory on load (keep one row per component; record
which source is the system of record). See `kit/collectors/metric-source-map.md`
(row S1) and the collectors `README.md`.

## 5. Populate the value-story screens

Get an editable copy of the template and census it (`kit/figma/README.md`, then
`kit/collectors/census_from_walk.py`). Assemble one payload of the design
system's numbers, in the shape of `kit/collectors/screen-data-bindings.json`,
from the value-store views — a metric the store does not carry is simply left
out. Resolve and apply:

```
python3 populate_screens.py <payload>.json --apply-plan --out apply-plan.json
```

then run `kit/collectors/figma_apply.js` through the design tool's script
runner. A slot with no value renders the placeholder (`—`) and never an invented
number. See `kit/collectors/populate-runbook.md`.

## 6. State the gaps honestly

Write down, for this run, which rows filled from which source and which stayed
placeholders. Naming the gaps is the field guide's own rule for the value
ledger: an instrument that admits what it does not yet measure is more credible
than a dashboard of confident guesses. `kit/06-executive-deck-skeleton.md`
turns the filled screens and the gap list into the leadership narrative.

## What you end with

A value store whose views return the design system's real design-side numbers, a
populated set of value-story screens that show them with every gap marked, and a
written scope statement. `kit/PLAN-skeleton.md` sequences all of this into
phases, gates, and the decisions only a person can take.
