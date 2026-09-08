---
title: Plan skeleton, making the case for a design system
kit: design-system-value-kit
artifact: PLAN
date: 2026-09-01
status: skeleton; phases, workstreams, gates, and decision slots defined; dates and owners to be filled by the organization running it
classification: unclassified
---

# Plan skeleton: making the case for a design system

*What an organization would do, in what order, with whom, to go from "we have a design system and leadership does not see its value" to "leadership reads a monthly instrument and funds the system as a product." Generic. Every slot that depends on the organization is marked **[decision]** or **[fill]**. The plan assumes the kit's artifacts exist and are used as written; it does not repeat their content.*

---

## 1. Outcome and success criteria

**Outcome.** Within two quarters, the design system reports like a product: a published set of metric definitions, a baseline with at least two periods of data, one instrumented proof event, a monthly one-page report on a fixed date in the tool leadership already opens, a per-team view, and a leading-indicator feed. The first budget conversation after that point is held on the instrument, not on a fresh deck.

**Success criteria at the two-quarter mark.**

- Definitions published for at least three metrics, each with an owner, a version, and a counter-metric.
- Coverage (M1) baselined with a declared method, per platform, with two periods of data.
- Cost ledger (M9) agreed with a finance partner and shown first on the one-pager.
- One proof card published from an instrumented event, with sources and a pessimistic–optimistic range.
- One-pager delivered on the same date for three consecutive months, in the organization's BI or reporting tool.
- The executive sponsor has attended at least two of the last three release reviews, and that attendance is recorded.
- Consumer survey run once with response rate above 30%.

**Explicit non-goals.** Proving an ROI percentage; building a standalone analytics product; measuring every metric in the pack; replacing the design system's own roadmap.

---

## 2. Roles

| Role | Who (typical) | Responsibility in this plan |
|---|---|---|
| Plan owner | design system lead | runs the plan, owns the one-pager, names owners for every metric |
| Executive sponsor | the leader whose budget the system sits in **[decision]** | receives the one-pager, attends release reviews, makes the decisions the one-pager asks for |
| Finance partner | an FP&A or business partner **[decision]** | agrees the loaded rate and owns the cost ledger |
| Instrumentation engineer | a front-end engineer with CI access | layers 3 and 4 of the playbook; the overlay |
| Analyst | whoever owns the BI tool | builds the views and the embedded executive and team pages |
| Consuming-team champions | one per major product **[fill]** | validate definitions, pick one task for the study, own their row on the team view |
| Reviewer (independent) | someone outside the system team | adversarial read of the first one-pager, the first proof card, and the first study before they go to the sponsor (F2) |
| System team | the design system's own designers and engineers | run the rituals, resolve feed events, maintain the definitions |
| Event delivery lead | whoever runs the natural event being instrumented | agrees the capture method and confirms hours |
| Sponsor's office | the sponsor's chief of staff or equivalent | fixes the reporting date and the tool the one-pager lives in |

RACI per workstream is in § 4.

---

## 3. Phases and gates

| Phase | Window | Exit gate (all must be true) |
|---|---|---|
| **0. Frame** | weeks 1–2 | Surface and team lists exist; the sponsor and finance partner are named; the first three metrics are chosen **[decision]**; the reporting date is fixed |
| **1. Baseline** | weeks 3–7 | Cost ledger agreed; coverage method chosen and baselined per platform; definitions v1 published; the next natural event identified and its ledger row opened |
| **2. Instrument** | weeks 5–12 | Overlay shipped on web; code scans running nightly; survey sent once; engagement counts started; views built in the BI tool |
| **3. First report** | weeks 13–15 | One-pager v1 delivered on the fixed date with two 28-day periods after the baseline (week 7 + 56 days = week 15); independent review done; sponsor attended a release review |
| **4. Steady state** | weeks 16–26 | Team view and feed live; proof card published; task study run; second and third one-pagers delivered; Deck B or C assembled from the store when needed |
| **5. Review and adapt** | week 26 | Retire vanity metrics, add at most one; re-baseline if a definition changed; decide whether to extend to mobile and to per-route coverage **[decision]** |

A phase closes on its gate, not on a date; the weeks are a planning estimate.

---

## 4. Workstreams

### WS-A. Definitions and cost (artifacts 01, 02; playbook layers 0–1)

- A1 Surface list, team list, library tagging. Owner: plan owner. Week 1.
- A2 Choose the first three metrics with the sponsor and two champions. Recommended default: M1 coverage, M2 override rate, M9 cost. **[decision]** Week 2.
- A3 Publish definitions v1 (screen 8). Week 3.
- A4 Cost ledger with finance: loaded rate basis, maintenance reserve %, support ratio. **[decision: rate; reserve %]** Week 3.
- A5 Stand up the store: dimensions and the first fact tables in the warehouse or as BI views. Owner: analyst. Weeks 3–4.
- A6 Cost ledger screen (screen 5) in the BI tool, provisional until D3 is taken. Owner: analyst. Weeks 4–5.
- RACI: R plan owner, A sponsor, C finance partner and champions, I system team.

### WS-B. Baseline and production measurement (playbook layers 3–4; artifact 05)

- B1 Choose coverage method per platform: pixel-weighted if the runtime allows, else DOM ratio, else import scan. Record method on every row. **[decision]** Week 3.
- B2 Build-time marker on system components. Week 4.
- B3 Runtime sampler to the existing analytics or APM tool; segment by product, route, platform, team. Weeks 5–7.
- B4 Nightly code scans and lint rules into the store (playbook layer 3). Weeks 4–6.
- B4b Design-tool library analytics export on a schedule (playbook layer 2), where the plan tier allows. Week 5.
- B5 Overlay v1 on web (bookmarklet or dev toggle), using the same marker. Weeks 6–9.
- B6 Baseline recorded and announced with date and method, after the sampler has run one full week. Week 7.
- B7 Defect labels in the tracker and automated accessibility checks in CI (playbook layer 5), loading `fact_defects_release` and `fact_a11y_pass_release`. Owner: QA lead. Weeks 6–8.
- RACI: R instrumentation engineer, A plan owner, C analyst, I champions.

### WS-C. Consumers and engagement (playbook layers 6–7; artifacts 01 M6–M8)

- C1 Four-question survey drafted, sent to all consumers, results loaded. Weeks 5–8.
- C2 Engagement counting started: office hours (normalized by team size), contributions, support. Spreadsheet is acceptable. Week 5 onward, monthly.
- C3 Sponsor invited to release review; attendance recorded from the first one. Week 5 onward.
- C4 Champions named per product; each validates their team's row before the first team view. Week 8.
- RACI: R plan owner, A plan owner (C1, C2, C4) and sponsor (C3), C champions.

### WS-D. Events and studies (artifacts 07, 08)

- WD1 Identify the next natural event (theme, rebrand, remediation, migration). Open the ledger row; establish last-time hours with source; take before images. **[fill: event]** Week 4.
- WD2 Capture hours during the event; close the row with range, confounders, quote. When the event ends.
- WD3 Controlled task study: recruit six to eight participants from consuming teams, three tasks (one chosen by a champion), blind quality review. Weeks 16–26.
- RACI: R plan owner, A sponsor, C champions and the event's delivery lead.

### WS-E. Surfaces and reporting (artifact 03 screens 1, 2, 7; artifact 06)

- E1 Executive view (screen 1) built in the BI tool from the store; embedded on the design system docs site under Metrics. Weeks 9–12.
- E2 One-pager generated on the fixed date; independent review; delivered to the sponsor. Week 15, then monthly.
- E3 Team view (screen 2) with sort-by-owner and the quadrant. Weeks 16–20.
- E4 Feed (screen 7) generated nightly from breach rules; a person edits and resolves. Weeks 18–22.
- E5 Deck skeleton (artifact 06) wired to the store for the next funding, renewal, or defense conversation. Weeks 20–26.
- RACI: R analyst, A plan owner, C independent reviewer and the sponsor's office, I finance.

### WS-F. Governance of the numbers

- F1 Definition change process: any change creates a new version, a break marker, and a note in the one-pager.
- F2 Independent review of each first-of-kind artifact (first one-pager, first proof card, first study) before it leaves the team.
- F3 Quarterly metric review: retire what nobody acts on; add at most one metric.
- F4 Access: read for everyone by default.
- RACI: R plan owner (F1, F3, F4) and independent reviewer (F2), A sponsor.

---

## 5. Timeline (indicative, twenty-six weeks)

```
Week    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 | 16–26
Phase   0  0  1  1  1  1  1  2  2  2  2  2  3  3  3 | 4 ──────── 5
WS-A    ■■ ■■ ■■ ■■ ■■
WS-B          ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■
WS-C                ■■ ■■ ■■ ■■                      | monthly, quarterly
WS-D             ■■ (event runs on its own schedule)  | study (WD3)
WS-E                            ■■ ■■ ■■ ■■ ■■ ■■ ■■  | team view, feed, deck
WS-F    ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  | continuous
Baseline                   ▲ week 7
Report                                         ▲ week 15, first one-pager (fixed date)
```

A "period" is 28 days. Two periods after the baseline are needed for the first delta, which is why the first report is week 15 and not week 12.

Fill real dates against the organization's release calendar and the date of the next budget conversation, which is the hard deadline the plan works back from **[fill]**.

---

## 6. Decisions that only a person can take

Listed here so they are taken deliberately and early, not discovered mid-plan.

| # | Decision | Owner | By |
|---|---|---|---|
| D1 | Which three metrics ship first | sponsor with plan owner | week 2 |
| D2 | Which executive is the sponsor, and which budget line the system sits in | the sponsor's leadership peers | week 1 |
| D3 | The loaded rate and the maintenance reserve percentage | finance partner | week 3 |
| D4 | Coverage method per platform, and whether mobile is in scope for quarter 1 | plan owner with instrumentation engineer | week 3 |
| D5 | The weights for pixel-weighted coverage, if used | plan owner with two champions | week 4 |
| D6 | Coverage and override thresholds for adoption levels 3+ | plan owner with champions | week 8 |
| D7 | The fixed reporting date and the tool the one-pager lives in | sponsor's office | week 2 |
| D8 | Which natural event to instrument first | plan owner with the event's delivery lead | week 4 |
| D9 | Targets (set only after two periods of data) | sponsor with plan owner | week 13 |
| D10 | Whether the audience framing is internal-efficiency or customer-value (drives Deck A/B wording) | sponsor | week 10 |
| D11 | Which surfaces are flagship (`dim_surface.weight_class`), which sets the headline's denominator | plan owner with champions | week 2 |
| D12 | Confirm or change the default breach thresholds in artifact 01 (5 points, 7-day doubling, 60% for two months, 14-day escalation) | plan owner with sponsor | week 3 |

---

## 7. Risks and their early signals

| Risk | Early signal | Mitigation |
|---|---|---|
| Measuring before defining | arguments about what the percentage means | Gate 1 requires definitions v1 before any number is shown |
| Method switch mid-series | a sudden jump in coverage | method is a key on every fact row; a switch starts a new series |
| Vanity dashboard | more than five tiles on the executive page | F3 quarterly review; the one-pager template has fixed slots |
| Sponsor absent | attendance recorded as 0 of 2 | C3 makes attendance a tracked number from week 5 |
| Self-reported hours presented as savings | a dollar figure with no method | M4 methods are labeled and never summed; independent review F2 |
| Instrumentation stalls on mobile | no Android or iOS rows by week 8 | scope decision D4 keeps quarter 1 to web; mobile is a quarter 2 decision, stated on the one-pager |
| Team resistance to per-team breakdown | requests to anonymize the team view | champions validate their own rows first (C4); the quadrant frames actions, not blame |
| Finance rejects the rate | one-pager cost line disputed | D3 taken with finance, basis recorded on the row |
| Event baseline reconstructed from memory | "last time" has no source | WD1 requires the source field before the event starts |
| No natural event occurs in the window | WD1 has no candidate by week 6 | Instrument the smallest scheduled UI change instead, or bring WD3 (the task study) forward; the one-pager says which |
| The plan owner is the only person who can read the numbers | no one else opens the BI page | F4 read-for-all; E1 embeds on the docs site; the deck exporter reads the store |

---

## 8. What is deliberately out of scope

- Any ROI percentage as a headline.
- Borrowed benchmarks on any surface (they may appear in an appendix with their provenance grade).
- Replacing the design system's product roadmap; this plan adds an instrument beside it.
- Vendor selection. The plan names tool *classes*; the organization chooses products.

---

## 9. Handoffs and cadence

- **Weekly (plan owner + instrumentation engineer + analyst):** gate progress, blockers, the feed.
- **Monthly (fixed date):** one-pager to the sponsor; team view refreshed; champions review their rows the week before.
- **Quarterly:** survey; metric review (F3); deck assembled if a funding, renewal, or defense conversation is scheduled; study once per year.
- **On event close:** proof card published within two weeks.

---

## 10. First ten actions (week 1)

1. Name the sponsor and the finance partner.
2. Fix the monthly reporting date.
3. Write the surface list and the team list with managers.
4. Tag the libraries (system, legacy, custom).
5. Draft definitions v1 for M1, M2, M9 from artifact 01 (drafts; adopted at D1 in week 2).
6. Book the hour with finance for the loaded rate and reserve.
7. Identify the next natural event and its delivery lead.
8. Shortlist the coverage method per platform (decided at D4 in week 3).
9. Draft the store's dimension tables (created once D1 is taken).
10. Schedule the independent reviewer for week 12.
