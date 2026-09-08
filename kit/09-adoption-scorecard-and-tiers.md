---
title: Adoption scorecard and tiers
kit: design-system-value-kit
artifact: 09
date: 2026-09-01
classification: unclassified
---

# Adoption scorecard and tiers

Two low-tech surfaces that predate every dashboard and still work: a scorecard of products against named adoption levels (Nathan Curtis's 2017 pattern, described here from secondary sources), and a tier ladder with names that teams can climb (the Delivery Hero pattern, also described from secondary sources: a webinar recap and a portfolio page). Use them when the system is early or federated, and as the front page of any periodic update even when the dashboard exists.

Levels are stored in `dim_adoption_level` and each team's current and committed level in `fact_team_level_monthly` (artifact 02), so the team view and the scorecard read the same rows.

## Part 1. Levels (define once)

Levels must be observable, cumulative, and few. A starting set:

| Level | Name | Observable criteria |
|---|---|---|
| 0 | Not started | No system dependency installed; no system library enabled in the design tool |
| 1 | Foundations | Tokens consumed for color, type, and spacing; system library enabled; a named contact on the team |
| 2 | Components | Core components (buttons, inputs, navigation, cards) from the system; no parallel local versions of those |
| 3 | Consistent | Coverage (M1) at or above a threshold on flagship surfaces **[decision: default 70%]**; override rate (M2) at or below a threshold **[decision: default 5%]**; files bugs and requests |
| 4 | Contributing | Contributes components or documentation back; participates in release review; a named contributor with protected time |
| 5 | Exemplar | Above thresholds on all surfaces; other teams point to it; helps onboard new teams |

Optional flavor names (Delivery Hero used Bronze, Silver, Gold, Platinum) help adoption socially; keep the criteria identical whatever the names are.

### Are the levels measurable? (check before you publish the ladder)

A level is only trustworthy if its criteria are observable and each traces to a signal something actually captures. Run the levels against that test before a team is placed on one.

| Level | The signal behind it | Captured how | Honest state |
|---|---|---|---|
| 0 Not started | No system dependency or library present | Dependency manifest; design-tool library list | Instrumented; a scan sees it |
| 1 Foundations | Tokens consumed; library enabled; a named contact | Token-import scan; a roster line | Foundations is scannable; the named contact is self-reported |
| 2 Components | Core components in use; no parallel local versions | Component scan | Capturable by scan, but "no parallel local versions" only holds if the scan looks for the duplicates, not just for system usage |
| 3 Consistent | Coverage (M1) above a threshold; override rate (M2) below one; files bugs and requests | M1, M2, the tracker | Only as instrumented as M1 and M2 are for that team; where coverage is not instrumented, the level cannot be claimed on evidence |
| 4 Contributing | Contributes back; in release review; a named contributor with protected time | Contribution log; review attendance | Contribution and attendance are logged; "protected time" is self-reported |
| 5 Exemplar | Above thresholds on all surfaces; other teams point to it; onboards others | M1 and M2 across surfaces; testimony | The thresholds are instrumented; "other teams point to it" is a judgment, not a metric |

Two consequences worth stating plainly:

- **A level backed by self-report is not a level backed by a metric.** The ladder already draws this line: levels 1 and 2 may be self-reported with a spot check; levels 3 and above are backed by M1, M2, and M6. Keep it. Promoting a team to level 3 on self-report defeats the ladder.
- **A level whose signal is not instrumented for a team cannot be evidenced for that team.** The scorecard below shows this honestly, where "coverage not instrumented" blocks a claim. Where the metric is missing, mark the level committed-pending-instrumentation, not reached.

The ladder itself can be gamed: a team can meet a level's letter (enable the library, file one token bug) without real adoption. The counter is the coverage and override signals the higher levels already require (M1, M2), read alongside adoption-versus-engagement, so a team cannot sit at a high tier while its coverage stays low. Which threshold counts, and whether a missed commitment costs a level, stay a **[decision]** for the system team.

### Are the level names consistent and legible? (a label pass)

The names do social work, so they are worth auditing as labels. This pass flags what is inconsistent or weak; it does not choose the words. Which names a ladder uses, and how many rungs it has, stay the system team's call.

- **The names mix grammatical forms.** Across the six rungs there are nouns ("Foundations," "Components," "Exemplar"), an adjective ("Consistent"), a present participle ("Contributing"), and a participial phrase ("Not started"). A reader cannot tell from a name's form whether it describes a state, an action, or a thing. Choosing one form (all nouns, or all "-ing" actions) is a label decision left to the team; the inconsistency is the finding.
- **Two names compete for the same click.** "Components" (level 2) and "Consistent" (level 3) both read as "we use the system properly," so a team can place itself at the wrong one from the name alone. The criteria separate them (coverage and override thresholds); the names do not. "Consistent" names the outcome rather than the step, which is where the ambiguity comes from.
- **"Exemplar" carries weaker scent than the rest.** "Foundations," "Components," and "Contributing" each predict their criteria; "Exemplar" is an evaluation ("others point to it") a reader cannot derive from the word. It is not wrong, only the least self-explaining rung.
- **The names are external-precedent, not local vocabulary.** This ladder is adapted from published patterns, not from how the adopting org's own teams describe themselves. Before publishing, check the names against the words teams actually use; a team that would never call itself an "Exemplar" will not climb toward the word. Where no such check has happened, treat the names as provisional.
- **The optional metal names do not cover the ladder.** Bronze, Silver, Gold, and Platinum are four names for a six-rung ladder, so they cannot label all six levels one-to-one. If a team uses them, decide which rungs they cover, and which have no metal, rather than leaving readers to guess.

None of the above renames a level or changes the count. It hands the system team a list to reconcile before the ladder goes on a wall. The criteria are the contract; keep them identical whatever the names become.

## Part 2. The scorecard (fill-in)

Products as rows grouped by priority; levels as columns; movement shown left to right. The example below uses the same illustrative fixture as the wireframes in artifact 03, so the two can be compared.

```
Priority   Product / team          L0  L1  L2  L3  L4  L5   Trend   Owner          Note
────────   ─────────────────────   ──  ──  ──  ──  ──  ──   ─────   ────────────   ────────────────────────────
Flagship   Checkout (web)                          ●   ○          ↑       A. Rivera      L4 committed Dec; contributing footer variants
Flagship   Mobile app (iOS)                    ●   ○              ↑       J. Okafor      L2 reached Jun; L3 blocked on override rate
Flagship   Mobile app (Android)            ●   ○                  →       J. Okafor      coverage not instrumented; L2 committed Q4
Secondary  Admin console                   ●                      ↓  ⚑    S. Lindqvist   coverage breach Aug 2; overrides rising
Secondary  Marketing site                              ●          ↑       M. Chen        L4 reached Aug 28 (contributed footer)
Internal   Support tools           ●                              (none)  unowned ⚑      no contact yet; no engagement data

● current level   ○ committed next level (date in note)   ↑ ↓ → movement since last report   ⚑ open breach in the feed
```

Rules:

- Every row has an owner. An unowned row is itself a finding.
- The committed next level carries a date; a date missed twice is reported as such.
- The scorecard is the first page of the monthly or quarterly update. Nothing precedes it except the headline number.
- Levels 3 and above are backed by the metrics (M1, M2, M6), not by self-report; levels 1 and 2 may be self-reported with a spot check.
- Movement arrows compare to the previous report; a trend of "(none)" means the team is not yet in the program.

## Part 3. The tier dashboard for a team

What a team sees about itself: its current tier, the criteria for the next tier with a checkbox per criterion, the metrics behind the checked ones, and what the system team will do to help. Delivery Hero's dashboard showed each squad's progress toward the next tier; posters of the tiers in the office did the social work.

```
Team: Mobile app (iOS)                                 Current tier: 2 · Components
Next tier: 3 · Consistent                              Committed by: 2026-12-15

  [ ] Coverage on flagship surfaces ≥ 70%      current 64%   (M1, ios, pixel, 28-day)  ▲ 6 since last report
  [ ] Override rate ≤ 5%                       current 7.8%  (M2)   → 9 hard-coded colors in Settings; 4 in Trips
  [x] Bugs and requests filed this quarter     current 6
  [x] Named contact with protected time        J. Okafor (confirmed 2026-07)

  What we will do: pair on the Settings overrides (2 h); ship the missing Segmented Control variant that drives 3 of the one-offs.
  Last movement: L1 → L2 on 2026-06-14
```

## Part 4. Celebration and visibility

- Publish level changes as `info` events in the feed and in the release notes.
- Name the team and the person when a level is reached.
- Keep the poster, physical or pinned in the chat tool, current.
