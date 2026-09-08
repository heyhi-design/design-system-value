---
title: Design System Value Kit
subtitle: The artifacts a team uses to measure, show, and defend a design system's value, generic and ready to adapt
date: 2026-09-01
status: v0.3; every artifact is usable as-is and marked where judgment is required
classification: unclassified
derived_from:
  - docs/making-the-case-for-a-design-system.md (the field guide)
  - docs/how-value-gets-shown-to-leadership.md (the visual survey)
---

# Design System Value Kit

This kit answers one question: **given the research, what would a team actually do on Monday?** It turns the field guide's argument (baseline, change, decision; three ledgers plus leading indicators; the definitions contract; the one-page report) and the survey's pattern library (headline, tiles, team table, migration chart, proof card, event feed, visible method) into artifacts a team can copy, fill in, and ship.

Nothing here is specific to any company, tool, or consultancy. Where a choice depends on the organization (which BI tool, which coverage method, which executive owns the budget), the artifact says so and leaves the slot open.

## What is in the kit

| # | Artifact | What it is for | Use it when |
|---|---|---|---|
| 01 | [Metric definitions pack](01-metric-definitions-pack.md) | Filled-in definition contracts for the nine core metrics, each with formula, source, exclusions, gaming path, and counter-metric | Before any number is shown to anyone |
| 02 | [Data model](02-data-model.md) | The tables a value store needs, as a portable schema sketch, so the dashboard, the one-pager, and the deck all read the same rows | Standing up the store in the organization's warehouse or BI tool |
| 03 | [Screen specs and wireframes](03-screen-specs.md) | Eleven screens, each with audience, layout, components, data bindings, states, and its precedent; low-fidelity wireframes for the four that matter most | Designing or embedding the reporting surface |
| 04 | [Instrumentation playbook](04-instrumentation-playbook.md) | Per data layer (design tool, code, production, consumers, engagement, cost): what to collect, how, with which tool class, and what it cannot tell you | Building the pipeline |
| 05 | [Overlay spec](05-overlay-spec.md) | A small spec for the on-screen highlighter that marks system versus non-system UI; on the survey's inference from Uber's Base Counter, the best return for its cost | First month, in parallel with the baseline |
| 06 | [Executive deck skeleton](06-executive-deck-skeleton.md) | Slide-by-slide outlines for the three occasions (first funding, renewal, defense), following the executive-summary grammar that executives already recognize | Any leadership presentation |
| 07 | [Event ledger and proof card](07-event-ledger-and-proof-card.md) | The protocol for measuring a natural experiment (rebrand, theme, remediation, migration) and the template for the card that reports it | Before the next big UI change starts |
| 08 | [Controlled task study protocol](08-controlled-task-study-protocol.md) | How to run the small internal with/without study that produces your own efficiency number | Once in the plan's second quarter, then yearly |
| 09 | [Adoption scorecard and tiers](09-adoption-scorecard-and-tiers.md) | The oldest leadership surface: products as rows, levels as columns, plus a tier ladder with names | Federated or early systems, and as the front page of any periodic update |
| SOURCES | [Sources](SOURCES.md) | A public URL for every precedent and study the kit names, with provenance grades | Whenever a precedent is quoted |
| PLAN | [Plan skeleton](PLAN-skeleton.md) | The execution plan that puts all of the above into motion: phases, workstreams, roles, gates, risks, and the decisions only a human can take | When someone asks "how would we run this" |
| tokens | [Design tokens](tokens/) | A neutral, theme-able design-token set (DTCG): gray and accent ramps, semantic roles, light and dark modes, every text and interactive-UI pair WCAG-gated. Swap the ramps to rebrand. | Theming the reporting surface, or handing tokens to a design tool or code |
| collectors | [Collectors](collectors/) | The operable metrics-collection layer: a metric-to-source map, a credential-free dry-run, and drop-in, credential-configurable adapter stubs for a design tool's library analytics and a documentation platform. | Pulling the fill-the-slots numbers from a real design system |

## The order that works

1. **Cost ledger and definitions first** (01, 02). State what the system costs and define three metrics before measuring anything. A number without a published definition cannot be defended in the meeting where it matters.
2. **Baseline, then the overlay** (04, 05). Pick one coverage method and record the "before." Ship the overlay so anyone can see what the number means on their own screen.
3. **Instrument the next event** (07). The rebrand, theme, or remediation that is already scheduled is the best proof story you will get this year. Set up the measurement before it starts.
4. **First one-pager on a fixed date** (03 screen 1, 06). Two 28-day periods after the baseline (about week 15), the definitions attached, the ask stated as a decision.
5. **Team view and event feed** (03 screens 2 and 7). Per-team breakdown turns the report into a product-team conversation; the feed turns it into a warning system.
6. **Quarterly: survey, metric review, deck if needed; yearly: the task study** (08, 06). Retire vanity metrics, add one metric per quarter at most.

## Rules the kit assumes

- Never insert a percentage without a source. Borrowed benchmarks carry their provenance grade; your own numbers carry their definition and date.
- Hard savings, soft savings, and cost avoidance stay in separate lines and are never summed into one headline without saying so.
- Every metric on an executive surface has a paired counter-metric.
- The numbers live in the tool leadership already opens. A standalone dashboard is the fallback.
- Report like a product (consumers, releases, roadmap, cost to run, health trend), never like a project.
- The field guide's ledgers are used by name: Ledger 1 is cost, Ledger 2 is hours, Ledger 3 is outcomes and quality.

## What the metric pack leaves out, and why

Two of the field guide's Ledger 3 lines are not in the nine metrics: outcomes in migrated flows (conversion or task completion with a control flow, difference-in-differences) and time-to-market for UI-heavy features. Both need product analytics and delivery data the kit cannot assume every organization has. Add them as M10 and M11 using the same contract shape when the data exists.

## What the kit deliberately leaves to people

Metric selection for a specific organization, target-setting, the sponsor to instrument, the loaded rate finance will accept, the executive framing per audience, and the ask itself. Each artifact marks these as **[decision]** slots.
