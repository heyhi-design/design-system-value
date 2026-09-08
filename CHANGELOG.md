<!-- classification: unclassified; generic release, no internal references permitted (see scripts/check-no-internal-refs.sh) -->
# Changelog

## 0.3.1 (2026-09-08)

Packaging only; no artifact content changed.

- Added `SETUP.md`: requirements, install, the three-line command form, layout, the after-you-change checklist, the mirror rule, rights.
- Added `scripts/smoke.sh`: one command that runs every credential-free check (collectors dry-run and gated adapters, populate contract and both sample payloads, token contrast gate, JSON validity, relative-link resolution, manifest, genericity scan).
- Added `scripts/manifest.sh` and `MANIFEST.txt` (path, size, SHA-256 for every file; the check fails in both directions).
- Added `scripts/check-links.py` (every relative Markdown link and asset path must resolve).
- Added `docs/assets/README.md` stating the contact sheets' terms in one place.
- Collector runbooks now point at the command form in `SETUP.md`.

## 0.3 (2026-09-08)

Every kit document reviewed and upgraded in place against its own design-method discipline, generic throughout (no worked example; judgment slots stay empty behind named gates):

- Field guide: a four-state claims-provenance crosswalk over the A..X grades; the design-ROI caveat made structural, so the McKinsey and InVision figures can never be a headline.
- Metric definitions (01): a Goals-to-Signals-to-Metrics traceability table and a Goodhart counter-metric table pairing every metric with a genuine opposing counter.
- Event ledger and proof card (07): a six-check statistical-integrity section (a single event is an n=1 natural experiment; metric fixed first; window set first; triangulation; provenance; confounders).
- Controlled task study (08): the corrected sample-size floor (5 directional, 10 reliable-mean, 20 for a ~95% detection floor) and a consent and data-handling checklist.
- Adoption scorecard (09): a measurability pass on the tier signals and a label-consistency pass on the tier names.
- Screen specs (03) and overlay (05): an interaction-state inventory (applicable-but-unshown states flagged MISSING, an APG keyboard column, accessibility hooks) and a microcopy string or an explicit empty slot for every state.
- Visual survey: restructured as a dated-evidence competitive teardown with a 14-pattern presence matrix and an empty severity column.
- Data model (02): re-run against PostgreSQL 17; a metric-id/grain mismatch corrected. Instrumentation playbook (04): a date-stamped access-reality re-check.
- Added a neutral, generic, theme-able design-token set (kit/tokens/, DTCG, light and dark modes, every text and interactive-UI pair WCAG-gated). No brand mode: swap the ramps to rebrand.
- Added an operable collectors layer (kit/collectors/): a metric-to-source map (every metric and every value-ledger row mapped to a source or marked a source-gap), a credential-free dry-run, and drop-in, credential-configurable adapter stubs for a design tool's library analytics and a documentation platform. The two adapters ship gated until the operator supplies access.
- Sources: added Faulkner (2003) behind the sample-size floor.

## 0.2 (2026-09-01)

- Kit: data model rewritten after review (metric id and version on every fact row; method and platform as keys; sample-weighted, in-scope coverage views; response-weighted satisfaction; tables for adoption levels, feed identity, consented verbatims, accessibility pass rate, event images, duplication ledger). Executed against PostgreSQL 17 with a seeded probe.
- Kit: M4(a) no longer extrapolates; M4(d) avoided duplication added; breach rules for M3 and M7; thresholds marked as decisions with defaults; owners as fill-ins.
- Kit: one-pager tile set fixed (cost first; coverage is the headline only); plan arithmetic closes (baseline week 7, first report week 15); playbook layers 2 and 5 and the cost-ledger screen assigned to workstreams; roles and RACI completed; risk for "no natural event" added.
- Kit: wireframes and the scorecard regenerated from one reconciled fixture; SOURCES.md added.
- Survey: Polaris deck-template claim removed (it was a listing site's own template); "every in-house winner lived in the BI tool" corrected (Uber and Pinterest built standalone dashboards; the failure is unvisited, not standalone); dates and column counts corrected; Mews section added; overlay superiority marked as inference.

## 0.1 (2026-09-01)

- Field guide, visual survey with contact sheets, and the first version of the kit and plan skeleton.
