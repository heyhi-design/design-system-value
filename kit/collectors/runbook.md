---
title: Collectors runbook
kit: design-system-value-kit
artifact: collectors/runbook
date: 2026-09-08
classification: unclassified
---

# Collectors runbook

How to point the kit at a real design system and produce a filled value ledger,
and how to run the credential-free dry-run first so you know what will fill and
what will not before anyone hands over a token.

Read this beside `metric-source-map.md` (what fills from where), artifact 02 (the
tables the numbers land in), and artifact 04 (the method behind each data layer).

## The two modes

1. **Dry-run (no credentials).** Emits the fill-map and the source-gap list from
   the static map. Needs nothing but Python. Run this first, on any machine, to
   see the shape of the answer.
2. **Live collection (per source, gated).** Once a source's access exists, fill
   its config, set its token in the named environment variable, flip its status,
   run it, and load the rows into the value store. The operator holds the token;
   the kit never does.

## Mode 1: dry-run

From `kit/collectors/`:

```
python3 dryrun.py            # fill-map + source-gap list + coverage check
python3 dryrun.py --check    # coverage check only (exit 0 pass, 1 fail)
python3 dryrun.py --adapters # also run each adapter's own credential-free dry-run
```

The dry-run answers two questions with no access to anything:

- **Coverage.** Every metric M1..M9 and every value-ledger row is classified as a
  named source or a source-gap. `--check` exits non-zero if anything is left
  unclassified.
- **Fill-map.** For each row: which source would fill it, into which table, and,
  for a gap, what instrumentation the gap needs.

The tail of a dry-run reports the counts:

```
== coverage check (V10) ==
  metrics classified:        9/9
  ledger data rows classified: 18/18
  narrative rows (no source by design): 1
  rows covered by figma-analytics: 6
  rows covered by supernova:       2
  source-gap rows:           24
  RESULT: COVERAGE OK (nothing unclassified)
```

Read that as the honest scope statement: the two named sources fill the
design-side adoption story; the cost, hours, quality, engagement, and risk
ledgers are source-gaps that need code-side, runtime, survey, or finance
instrumentation. Nothing about the dry-run needs a token, a network, or a plan
tier, so it is the right thing to run in a first conversation with a team.

## Mode 2: live collection

Prerequisites: the value store from artifact 02 stands up in the operator's
warehouse, and the source you are collecting from has its access in place (an
Enterprise plan and a Library Analytics token for Figma; an account and an API
token for Supernova).

Per source, the activation path is the same steps as the collectors README (fill config, set token, flip status, implement the one network seam) and no structural rewrite:

1. **Fill the config.** In the adapter script, set the ids (Figma library file
   keys, or the Supernova workspace and design-system ids). Confirm the endpoint
   base and the env-var name.
2. **Set the token.** Export the token into the named environment variable
   (`FIGMA_LIBRARY_ANALYTICS_TOKEN` or `SUPERNOVA_API_TOKEN`). The token stays in
   the operator's environment and never enters a file in the kit.
3. **Flip the status.** Change `STATUS` from `"gated"` to `"active"` at the top of
   the adapter, then run it live:

```
python3 figma_adoption_adapter.py --live
python3 supernova_adapter.py --live
```

Once the network seam is implemented, each `--live` run returns rows keyed to the artifact 02 tables (the
`_table` field on each row names the target). Load them with the operator's own
loader (a `COPY`, an insert script, or the warehouse's ingestion path). Then the
views in artifact 02 (`v_exec_headline`, `v_team_view`) read them and the value
ledger's design-side rows are filled.

What comes back filled is the design side: the M2 detachment counter-metric, the
M3 design-side instance count, and the token and component inventory. What stays
blank is every row the map marks `source-gap`. Fill those from the layers in
artifact 04 (code scans, a production sampler, the survey, the finance
spreadsheet), or leave them blank and say so, which is the field guide's own
rule for the value ledger.

## The deferred structural half

The Figma structural inputs (S1 on the map: the component, variable, and style
inventory and code crosswalk) are not collected by these two adapters. They come
from the design read surface plus a read-only library census, and they depend on
the design library existing first. Run that census step after the library is
built; it feeds `dim_component` and the design-side coverage counts. This runbook
does not invoke it, and the dry-run does not depend on it.

## Credentials discipline

The operator runs every live collector with their own token, in their own
environment or secret manager. No token, key, or credential is written into any
file in this kit. The adapters read a token only from the named environment
variable, only in `--live`, only when the status is `active`, and refuse
otherwise with a clear message. A dry-run never reads a token at all.
