---
title: Event ledger and proof card
kit: design-system-value-kit
artifact: 07
date: 2026-09-01
classification: unclassified
---

# Event ledger and proof card

The strongest story a design system ever gets is a natural experiment: something the organization was going to do anyway (a rebrand, a theme, an accessibility remediation, a framework migration, a spacing overhaul) that cost far less than the last time. This artifact is the protocol for capturing it honestly and the template for the card that reports it.

## Part 1. The protocol

### Before the event starts

1. **Open the ledger row** (`event_ledger` in artifact 02) with the event type, title, owner, and planned dates.
2. **Establish "last time."** Find the most comparable previous event and its cost in hours: timesheets, ticket estimates, sprint records, invoices, or a structured estimate from the people who did it. Record the *source* of the number, not only the number. If there is no comparable event, record an estimate from two independent people and set `baseline_kind` to `estimated`; the card carries the badge.
3. **Decide what will be counted this time.** Which teams, which activities, which tools. Set up the capture: a tag in the issue tracker, a timesheet code, or a short daily log. Name the person who will collect it.
4. **Take the before picture.** Screenshots of three to five representative screens, dated, one `event_image` row each.
5. **List confounders.** Anything else that changed at the same time (a new hire, a tool change, a smaller scope). Write them down now, not after.

### During

6. Collect hours as agreed. Do not adjust the plan mid-way without recording the change.

### After

7. **Close the row.** Hours this time with source; a pessimistic and an optimistic saving (pessimistic subtracts the confounders' plausible effect; optimistic does not); the loaded rate used and its basis; the saving class (soft, avoidance, or hard).
8. **Take the after picture** of the same screens.
9. **Collect one quote** from someone outside the system team who did the work.
10. **Publish** the card to the event ledger screen and to the next one-pager. Mark the row published.

### What not to do

- Do not multiply one event's saving across the organization.
- Do not report only the optimistic figure.
- Do not omit the confounders; a reader who finds one you left out discounts the rest.
- Do not count the same hours in the task study, the survey, and the event.

### The integrity checks (what makes the number trustworthy)

An event card is the most persuasive thing the system produces, which is exactly why it is the easiest to overclaim. Run these six checks over every card before it is published; they are the difference between a number a skeptic accepts and one they wave away.

1. **Name the kind of evidence.** A single event is a natural experiment with a sample size of one: a before-and-after on one case, not a randomized or powered test. It is an existence proof (this rebrand cost far less than the last one) and a story, not an organization-wide average. Say so on the card, and never turn one event into a rate. The number is honest at a sample of one only if the sample of one is stated.
2. **Fix the metric before the event (no back-solving).** Decide what counts as saved, the comparison basis, and the saving class before the work starts (step 3 above), and report that metric even if it disappoints. Switching from hours to screens-per-hour after seeing the result because it reads better, or promoting whichever framing flatters the number, is the back-solved-metric trap.
3. **Set the window up front (no window-shopping).** Fix the start, the finish, and what is counted before the event, and record any mid-course change (step 6). Moving the finish line to where the saving peaks, or quietly dropping an expensive week as "not really part of it," is the natural-experiment form of stopping a test the moment it looks good.
4. **Do not let one card carry the whole case.** One event is one method. Triangulate: a card feeds M4(b) only, never M1 or M3, and it sits beside the task study, the survey, and the duplication ledger rather than standing in for them. Report the guardrails too: did defects (M5) or satisfaction (M8) move while hours fell? A cheaper rebrand that shipped more bugs is not a clean win.
5. **Source every number (provenance).** Record where "last time" and "this time" came from, not only the figures (step 2), and carry the baseline badge: a recorded baseline and an estimated one must never look alike on the card. An estimated saving reported as if measured is the fastest way to lose the reader.
6. **Randomization does not apply, so lean on the confounders.** Nothing here is randomly assigned, so there is no arm balance to check; the honest substitute is the confounder list (step 5). Because the system was not the only thing that changed, that list is what keeps the card from claiming the whole saving belongs to the system alone. A reader who finds a confounder you left out discounts everything else on the card.

What these checks do not decide: whether the saving is large enough to matter, and whether to act on it. The card reports the honest number and its caveats; that materiality call stays with the reader.

## Part 2. The proof card (fill-in)

Render this as a fixed-size card (it should fit a slide and a dashboard tile) with the before and after images side by side above the text.

```
┌──────────────────────────────────────────────────────────────────┐
│  [BEFORE image]                    [AFTER image]                 │
│  <screen name, date>               <screen name, date>           │
├──────────────────────────────────────────────────────────────────┤
│  EVENT     <type>: <title>                      <start – finish> │
│                                                                  │
│  LAST TIME  <N> hours    source: <timesheets / estimates / …>    │
│  THIS TIME  <M> hours    source: <tag / timesheet code / log>    │
│                                                                  │
│  SAVED      <pessimistic> to <optimistic> hours                  │
│             ≈ <$low> to <$high> at <rate> loaded  (<saving class>)│
│                                                                  │
│  WHAT ELSE CHANGED  <confounders, one line>                      │
│                                                                  │
│  "<one sentence from someone who did the work>"                  │
│   <name, role, team>                                             │
│                                                                  │
│  Definition M4(b) v<version> · Owner <name> · Published <date>   │
└──────────────────────────────────────────────────────────────────┘
```

The card carries its own honesty on its face. When the baseline is estimated rather than recorded, badge it as such beside LAST TIME so an estimate never reads as a measurement. Keep the confounders line populated; a blank one reads as a claim that nothing else changed, which is rarely true. And treat the saving class (soft, avoidance, or hard) as the claim itself, not a footnote: it tells the reader exactly how far the number is allowed to travel.

## Part 3. Event types and what "last time" usually is

| Event type | Where "last time" tends to live | What to count this time |
|---|---|---|
| Rebrand or visual refresh | agency invoices, the last rebrand's project plan, PRs touching color/type across repos | hours across design, engineering, and QA from kickoff to full rollout; screens touched per hour |
| Dark theme or new theme | the first theme's tickets; or an estimate if none existed | hours; number of hard-coded values replaced (from lint) |
| Accessibility remediation | audit reports and their fix tickets | hours; issues closed per hour; regression count after |
| Framework or library major | previous upgrade's PRs and incident log | hours; incidents; teams that did not need to touch UI code |
| Spacing, density, or layout overhaul | design QA rounds from the last one | hours; visual-diff failures |
| New product or surface on the system | a comparable surface built before the system | time from kickoff to first release; defects in first month |

## Part 4. The card's place in the system

- One card per event, kept forever in the event ledger screen (artifact 03, screen 6).
- The two most recent cards appear in Deck B; the two strongest (largest pessimistic saving with a recorded, not estimated, baseline) in Deck C.
- Cards feed M4(b) only. They never feed M1 or M3.
