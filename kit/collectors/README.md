---
title: Collectors
kit: design-system-value-kit
artifact: collectors/README
date: 2026-09-08
classification: unclassified
---

# Collectors

The operable layer of the kit. Point the packet at a real design system and pull
the numbers that fill the value ledger, the metric-definitions pack, and the
reporting screens, from two named sources: a design tool's library analytics
(Figma) and a design-system documentation platform (Supernova).

Artifact 04 is the method (how to get each number out of the systems you have).
This folder is the mechanism (the adapters that do it), plus an honest map of
what those two sources can and cannot supply.

## Files

| File | What it is |
|---|---|
| `metric-source-map.md` | For every metric M1..M9 and every value-ledger row, the source, the call, the transform into an artifact 02 table, or a `source-gap` mark. Start here. |
| `figma-adoption-adapter.md` | Spec for the Figma Library Analytics adapter (design-side adoption over time). Gated on Enterprise access. |
| `supernova-adapter.md` | Spec for the documentation-platform adapter (structure and documentation coverage). Gated on account access. |
| `runbook.md` | How to run the dry-run, and how to point the packet at a design system and produce a filled ledger. |
| `source_map.py` | The machine-readable mirror of the map. The single source of truth the scripts read. |
| `figma_adoption_adapter.py` | The Figma adapter reference script. Runs a dry-run today, a live pull once activated. |
| `supernova_adapter.py` | The documentation-platform adapter reference script. Same shape. |
| `dryrun.py` | The credential-free driver. Emits the fill-map and source-gap list; `--check` asserts coverage. |

## Start here

```
python3 dryrun.py            # what fills from where, and what stays a source-gap
python3 dryrun.py --check    # assert every metric and ledger row is classified
```

The dry-run needs no token, no network, and no plan tier. It is the right thing
to run before any access exists.

## Activation path: fill the config, flip the status

Each adapter ships gated and becomes live in three steps, with no structural
rewrite:

1. **Fill the config.** Set the ids in the adapter's `CONFIG` block (Figma library
   file keys, or the Supernova workspace and design-system ids).
2. **Set the token.** Export the source's token into the named environment
   variable (`FIGMA_LIBRARY_ANALYTICS_TOKEN` or `SUPERNOVA_API_TOKEN`). The token
   lives in the operator's environment, never in a file here.
3. **Flip the status.** Change `STATUS` from `"gated"` to `"active"` at the top of
   the adapter.
4. **Implement the network seam.** Fill in the adapter's single `_request` (Figma)
   or `_read` (Supernova) method with your own HTTP client, then run it with
   `--live`. The adapters deliberately leave that one call to the operator and
   refuse cleanly until it exists.

The operator runs every live collector with their own token. No credential is
written into any file in this kit. See `runbook.md` for the full flow.

## The deferred structural half

The Figma structural inputs (component, variable, and style inventory and the
code crosswalk, S1 on the map) are not collected by these two adapters. They come
from the design read surface plus a read-only library census, and they depend on
the design library existing first. Run that census step after the library is
built; it feeds `dim_component` and the design-side coverage counts. The dry-run
does not depend on it, and this folder does not invoke it.

## Genericity

Everything here is generic and organization-configurable: no design system, org,
tool account, or vendor identifier is hardwired. The kit's genericity check
(`scripts/check-no-internal-refs.sh`) is binding on this folder.
