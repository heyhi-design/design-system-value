#!/usr/bin/env python3
"""Credential-free dry-run for the value-kit collectors.

Runs with no token and no network. It answers two questions the kit has to
answer before anyone points it at a real design system:

  coverage (V10)  Does every metric M1..M9 and every value-ledger row map to a
                  named source or a source-gap? Nothing is left unclassified.
  fill-map (V11)  For each row: which source would fill it, into which table,
                  and (for a gap) what instrumentation the gap needs.

Usage:
  python3 dryrun.py            fill-map + source-gap list + coverage check
  python3 dryrun.py --check    coverage check only (exit 0 pass, 1 fail)
  python3 dryrun.py --adapters  also run each adapter's own credential-free dry-run

This is the checker beside the map (source_map.py) and its readable report
(metric-source-map.md), the same shape as the kit's tokens checker.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import source_map  # noqa: E402


def print_fill_map():
    print("== fill-map ==")
    print("")
    print("What the two named sources DO supply (design side):")
    for r in source_map.STRUCTURAL_INPUTS:
        print("  [{id}] {label}".format(id=r["id"], label=r["label"]))
        print("       source: {src}  ->  {target}".format(src=r["source"], target=r["target"]))
    print("")
    print("Metrics M1..M9:")
    for r in source_map.METRICS:
        line = "  {id} {label}: source={src} ({cov})".format(
            id=r["id"], label=r["label"], src=r["source"], cov=r["coverage"])
        print(line)
        print("       -> {target}".format(target=r["target"]))
        if r["source"] == "source-gap" or r["coverage"] == "partial":
            print("       gap: {gap}".format(gap=r["gap_needs"]))
    print("")
    print("Value-ledger rows (field guide Appendix A):")
    for r in source_map.LEDGER_ROWS:
        print("  {id} [{ledger}] {label}: source={src} ({cov})".format(
            id=r["id"], ledger=r["ledger"], label=r["label"],
            src=r["source"], cov=r["coverage"]))
        print("       -> {target}".format(target=r["target"]))
        if r.get("gap_needs"):
            print("       gap: {gap}".format(gap=r["gap_needs"]))
    print("")


def print_source_gaps():
    gaps = source_map.source_gaps()
    print("== source-gap list ({n} rows no figma/supernova read can supply) ==".format(
        n=len(gaps)))
    print("")
    for r in gaps:
        label = r["label"]
        print("  [{id}] {label}".format(id=r["id"], label=label))
        print("       needs: {gap}".format(gap=r["gap_needs"]))
    print("")


def coverage_check():
    """V10: every metric and every ledger row is classified. Returns True/False."""
    ok = True
    problems = []

    metric_ids = [m["id"] for m in source_map.METRICS]
    expected = ["M%d" % i for i in range(1, 10)]
    if metric_ids != expected:
        ok = False
        problems.append("metric ids are {got}, expected {exp}".format(
            got=metric_ids, exp=expected))

    bad = source_map.unclassified()
    if bad:
        ok = False
        problems.append("rows with no source classification: " + ", ".join(bad))

    # Every ledger row must carry a source value (source-gap and n/a both count
    # as classified; blank does not).
    for r in source_map.LEDGER_ROWS:
        if not r.get("source"):
            ok = False
            problems.append("ledger row {id} has no source".format(id=r["id"]))

    n_metrics = len(source_map.METRICS)
    n_ledger = len([r for r in source_map.LEDGER_ROWS if r["id"] != "N1"])
    n_narr = len([r for r in source_map.LEDGER_ROWS if r["id"] == "N1"])
    n_gap = len(source_map.source_gaps())
    n_figma = len(source_map.covered_by("figma-analytics"))
    n_super = len(source_map.covered_by("supernova"))

    print("== coverage check (V10) ==")
    print("  metrics classified:        {n}/9".format(n=n_metrics))
    print("  ledger data rows classified: {n}/18".format(n=n_ledger))
    print("  narrative rows (no source by design): {n}".format(n=n_narr))
    print("  rows covered by figma-analytics: {n}".format(n=n_figma))
    print("  rows covered by supernova:       {n}".format(n=n_super))
    print("  source-gap rows:           {n}".format(n=n_gap))
    if ok:
        print("  RESULT: COVERAGE OK (nothing unclassified)")
    else:
        print("  RESULT: COVERAGE FAILED")
        for p in problems:
            print("   - " + p)
    print("")
    return ok


def run_adapter_dry_runs():
    import figma_adoption_adapter
    import supernova_adapter
    figma_adoption_adapter.dry_run()
    print("")
    supernova_adapter.dry_run()
    print("")


def main(argv):
    if "--check" in argv:
        return 0 if coverage_check() else 1

    print_fill_map()
    print_source_gaps()
    if "--adapters" in argv:
        run_adapter_dry_runs()
    ok = coverage_check()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
