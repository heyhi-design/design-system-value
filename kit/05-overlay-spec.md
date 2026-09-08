---
title: Overlay spec (the eye)
kit: design-system-value-kit
artifact: 05
date: 2026-09-01
classification: unclassified
---

# Overlay spec: the eye for everyone

A small tool that highlights, on the live product, which parts of the screen come from the design system and which do not. Uber's version (Base Counter) let any product manager turn it on and see the number on their own phone. The survey's inference, which Uber's article does not state, is that this did more for adoption than the dashboard. On that reasoning the overlay is the kit's best return relative to its cost (three to eight engineering days, see the playbook's effort map), and it should ship before the dashboard is polished.

## Purpose

- Make the coverage metric (M1) legible without a chart: a picture of the product with system parts outlined.
- Let anyone, not only the system team, find the one-offs on a screen they own.
- Provide the same marking that the production sampler uses, so the overlay and the metric agree by construction.

## Scope

- Web first (a bookmarklet or browser extension, and a Storybook or dev-mode toggle). Mobile second (a debug-menu toggle that decorates the view tree).
- Read-only. It never changes the product.

## Behavior

1. **Toggle** from a keyboard shortcut, a bookmarklet, a query parameter in non-production, or a debug menu on mobile.
2. **Marking.** Every element produced by a system component is outlined in one color (green in Uber's implementation); every element that *looks like* a system pattern but is not from the system is outlined in a second color (red); everything else is left alone. Detection uses the same build-time marker as the production sampler (`data-ds-component="<name>"` or equivalent) plus an optional allow-list of "known custom" patterns for the second color.
3. **Badge.** A small fixed badge shows the screen's coverage number computed live with the same formula as M1 (weighted area), the count of system elements, and the count of non-system elements. Tapping the badge lists the non-system elements with their approximate location and the closest system component, if a mapping exists.
4. **Weights visible.** The badge's detail view shows the weight class applied to each element, so the number can be questioned.
5. **Capture.** One action copies a screenshot with the overlay plus the numbers, formatted as a proof-card image (artifact 07), and opens an issue in the tracker pre-filled with the screen, the owner team, and the list of one-offs. The path into the ticketing system is what makes the overlay part of the accountability loop rather than a curiosity.
6. **Performance.** Off by default; when on, marking runs once per navigation and on a debounced resize. No network calls unless capture is used.

## What it shows and does not show

- Shows: system versus non-system, per element, on the real product; the live coverage number; the owner team (from `dim_surface`).
- Does not show: whether the system component is used correctly, accessibility conformance, or anything about design intent. Say so in the badge's help text.

## Dependencies

- The build-time marker (layer 4 in artifact 04). Without it, the overlay falls back to matching class names or component display names, which is less reliable and must be labeled as such.
- The surface list (`dim_surface`) if the owner team is to be shown.

## Acceptance

- On three flagship screens, the overlay's coverage number matches the production sampler's number for the same route within 2 points.
- A product manager with no system knowledge can turn it on, find a one-off, and file an issue in under two minutes.
- Turning it on and off leaves no trace in the DOM or the analytics stream.

## Extensions (later)

- A "what would this screen look like on the system" mode that swaps known one-offs for their system equivalents visually (Uber's before/after figure, generated).
- Per-element history: when this one-off first appeared and in which release.
- Storybook addon that shows the same marking on stories, so the design system team sees its own coverage in the catalog.

---

## Interaction inventory (the overlay's states)

The overlay is one tool with a small element set. This inventory enumerates its states against the control-state contract (default / hover / focus-visible / active / disabled / loading / error, plus success and selected) and the data-view floor (empty / loading / error / populated) before it is built, and flags every applicable state the behavior above does not yet show as `MISSING`. A `MISSING` cell is a flag for the human, never a defect verdict; the ruling on each is the gate at the end of this section.

### Element census

| # | Element | Class | Provenance | APG pattern (role call is the human's) |
|---|---|---|---|---|
| O1 | Toggle (shortcut / bookmarklet / query param / debug menu) | action | from-source | Switch (`aria-pressed`), or the platform's own shortcut |
| O2 | Marking layer (system vs non-system outlines) | data view | from-source | none (a decoration over the live DOM) |
| O3 | Badge (live coverage number + counts, tappable) | composite | from-source | Disclosure (`aria-expanded`) |
| O4 | Badge detail (one-off list with weights) | data view | from-source | none (list) |
| O5 | Capture action (screenshot + open an issue) | action | from-source | Button |

### State matrix (contract states)

Legend: `shown` = the behavior above carries it · `MISSING` = applicable by class, not shown (a flag) · `n/a` = not applicable by class.

| Element | default | hover | focus-visible | active | disabled | loading | error | success | selected |
|---|---|---|---|---|---|---|---|---|---|
| O1 toggle | shown | MISSING | MISSING | MISSING | MISSING (if unavailable off-marker) | n/a | n/a | n/a | MISSING (`aria-pressed` on/off) |
| O3 badge | shown | MISSING | MISSING | MISSING | n/a | MISSING (recomputing the live number) | MISSING (if the count fails) | n/a | MISSING (`aria-expanded`) |
| O5 capture | shown | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | n/a |

Data views O2 and O4 carry no hover / active and are enumerated on the data-view floor below; their `focus-visible` cell applies wherever a one-off in the list or on the overlay is focusable and is `MISSING` until the behavior specs that focus.

### Data-view states (empty / loading / error / populated)

| Data view | empty | loading | error | populated |
|---|---|---|---|---|
| O2 marking layer | MISSING (no elements detected) | MISSING (scanning) | MISSING (degraded: no build-time marker, class-name fallback) | shown (the outlines) |
| O4 badge detail | MISSING (no one-offs, i.e. full coverage) | MISSING (building the list) | MISSING | shown (the one-off list) |

The main finding: the behavior specs the populated marking well and omits its **loading**, **empty**, and **degraded** states. The degraded state is not hypothetical: the Dependencies note already says that without the build-time marker the overlay "falls back to matching class names, which is less reliable and must be labeled as such." That label is a state string with no home yet (drafted below).

### Transitions (candidate state machines, agent-drafted)

| Element | From → To | Trigger | Exit path | Flag |
|---|---|---|---|---|
| O1 toggle | off → on | shortcut / bookmarklet / query param / menu | on → off (same trigger) | selected state (`aria-pressed`) unspecced |
| O2 marking | idle → loading | toggle on, navigation, debounced resize | loading → populated / degraded (no marker) / empty | `loading-no-error-exit`: only the marked result is drawn; degraded and empty unspecced |
| O5 capture | default → loading | activate | loading → success (issue opened) / error (capture or tracker call failed) | `loading-no-error-exit`, `error-no-recovery`: the behavior draws only "opens an issue pre-filled" |

### Focus, keyboard, gesture

Target-size floor is WCAG 2.2 SC 2.5.8 (24×24 CSS px); 44×44 is the recommended comfortable target.

| Element | Focusable | Keyboard | Touch | Target ≥ 24×24 |
|---|---|---|---|---|
| O1 toggle | yes (its own control) | the shortcut, plus Enter/Space if a button; the shortcut must not collide with assistive-technology shortcuts | tap the debug control | check |
| O3 badge | yes | Enter/Space toggles the detail (Disclosure); it must be operable by keyboard, not tap-only | tap to expand | check (the badge is a target) |
| O5 capture | yes | Enter/Space activates | tap | check |

Flags: `tap-only-risk` on O3 (the behavior says "tapping the badge" lists the one-offs; a keyboard path must exist); `hover-only` on nothing yet, but the marking must not rely on color alone (see the hooks below).

### Accessibility hooks per state

- **O2 loading:** `aria-busy="true"` on the overlay region; a polite `status` region announces the scan.
- **O2 degraded / error:** a polite `status` region announces the best-guess mode so a non-visual user knows the outlines are unreliable.
- **Color is not the only signal.** The marking distinguishes system from non-system by color (green and red in the reference implementation). Color alone fails WCAG 2.2 SC 1.4.1 (Use of Color); add a non-color cue (a label, an icon, or an outline style) so the two classes are distinguishable without color. This is a finding for the gate, not a contract failure of this spec.
- **O3 badge:** `aria-expanded` on the badge; the live coverage number sits in a polite live region so a screen reader hears it recompute on navigation.
- **O5 capture:** `aria-busy` while preparing; a polite `status` announces success; `role="alert"` on a failure.
- **O1 toggle:** `aria-pressed` reflects on/off; toggling on announces the coverage summary so the state change is perceivable without sight.

### Copy slots (empty; filled by the microcopy set below)

| Element | State | Taxonomy slot | String |
|---|---|---|---|
| O2 marking | loading / error (degraded) | Loading / Error | (below) |
| O4 badge detail | empty / loading | Empty / Loading | (below) |
| O5 capture | loading / error / success | Loading / Error / Success | (below) |
| O1 toggle | on (announcement) | Notification | (below) |

---

## Microcopy set (candidate strings for every copy-bearing state)

**Generic voice frame (candidate, doubly-candidate mode).** No client voice system is confirmed for this generic kit, so every string below is a candidate twice over: agent-drafted, and written against a voice frame no human has signed. The frame is the kit's own conventions: plain and precise; a state string names the next step, not only the condition; no false precision; no marketing adjectives; terse in a badge or a toast.

| Element | State | Slot | Candidate string [candidate: agent-drafted] | Constraints | Doctrine | Lineage |
|---|---|---|---|---|---|---|
| O1 toggle | on | Notification | "Overlay on. {systemCount} system, {oneOffCount} one-offs, {coverage} coverage." | announced · {systemCount}, {oneOffCount}, {coverage} | state named + what is now visible ✓ | new |
| O2 marking | loading | Loading | "Scanning this screen." | overlay · ≤24ch | object named ✓ · no duration ✓ | new |
| O2 marking | error (degraded) | Error | "Showing best-guess matches: this screen has no system markers, so the outlines may be off." | banner | condition: from spec (Dependencies note) ✓ · next step implicit (add markers) | revised-from: "must be labeled as such" |
| O4 badge detail | empty | Empty | "Every element on this screen is from the system." | panel | states the full-coverage condition ✓ | new |
| O4 badge detail | loading | Loading | "Listing the one-offs." | panel · ≤24ch | object named ✓ | new |
| O5 capture | loading | Loading | "Preparing the proof image and the issue." | toast | object named ✓ · no duration ✓ | new |
| O5 capture | success | Success | "Issue opened with the screenshot and the one-off list. Open it in the tracker." | toast | done + next possible ✓ | new |
| O5 capture | error | Error | "The capture didn't finish: {condition}. Try again." ⚠ condition-unsupplied | toast · {condition}: held | next-step: retry ✓ · condition: NOT on the row | new |

Legend: ✓ = doctrine part met · ⚠ = a flag for the human.

### Flags (findings for the human, never verdicts)

- `condition-unsupplied` (O5 capture, error): the behavior does not define the failure trigger for the capture or the tracker call, so `{condition}` is held and no cause is named.
- `next-step-unsupplied` (O5 capture, tracker-open failure): if the failure is the tracker call rather than the screenshot, the recovery (retry, save the image locally, copy a link) is undecided; the retry string above covers the capture failure only. Flagged, not invented.
- `use-of-color` (O2 marking): the green/red distinction is color-only until a non-color cue is added (a11y hooks, above).

### Claim / SLA guardrail

Empty. No string asserts an SLA, a timeframe, or a number as a claim; the badge's coverage figure is a live measurement, not copy. The Acceptance section's "within 2 points" and "under two minutes" are test targets, not strings.

### Candidate glossary (terms and conflicts; no rulings)

| Term | Where | Candidate definition | Conflict seen |
|---|---|---|---|
| one-off | O2, O4, screen 4 | an element that looks like the system but is not from it | (none) |
| coverage | O1, O3 | the live share of the screen that is from the system | same word as the dashboard metric (M1); confirm they compute the same way |
| marker | Dependencies, O2 | the build-time attribute that identifies a system element | (none) |

### Open questions and near-misses

**Open questions (questions, not judgments):**
- What is the failure trigger for the capture and, separately, for the tracker call, so the held `{condition}` is filled and the tracker-open recovery path can be decided?
- Which `MISSING` states are gaps to design and which are deliberate (a toggle may not need a specced disabled state in production)?
- Which non-color cue distinguishes system from one-off (a label, an icon, an outline style)?
- Does the badge's live coverage number compute the same way as the dashboard's M1, so the two never disagree in front of a viewer?

**Near-misses and unchecked territory (traces, no verdicts):**
- Almost flagged: the "off" state of the toggle as an empty state; turning the overlay off returns the product to normal and needs no string, so it is not a copy-bearing state.
- Explicit empty slot, not drafted: the marking layer's `empty` state (no elements detected on the screen) is applicable by the data-view floor and is flagged `MISSING` in the inventory, but it is effectively unreachable on a real product screen, so no string is drafted. The gate rules whether it needs one.
- Considered, set aside: a permission string for the capture-to-tracker step (it may need an auth grant); the behavior does not describe one, so none is drafted.

### The judgment slots (empty by construction)

**⛔ Which interactions matter, NEEDS HUMAN.** Which of the overlay's states get design attention: ____________________

**⛔ Deliberate-absence rulings, NEEDS HUMAN.** Each `MISSING` flag above is either a gap to design or a deliberate absence. Rule on each: ____________________

**⛔ Which copy ships, tone calls, terminology rulings, NEEDS HUMAN.** Per string: accept, rewrite, or ask for alternates; resolve each ⚠ flag; confirm the "coverage" definition matches M1: ____________________

**Named gate.** Sign-off owner (design lead / content lead): ____________________  Date: ______
No state is declared complete or deliberately absent, and no string ships, until this line is signed by a human.
