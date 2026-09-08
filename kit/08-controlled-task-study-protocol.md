---
title: Controlled task study protocol
kit: design-system-value-kit
artifact: 08
date: 2026-09-01
classification: unclassified
---

# Controlled task study protocol

A small internal study that produces your organization's own "faster with the system" number, in the shape of the two published studies that hold up (Sparkbox's Carbon study, n = 8; Figma's designer study). It is cheap, it is honest at small n if the n is stated, and it replaces every borrowed benchmark on your slides.

Run it once in the plan's second quarter (workstream D in the plan skeleton), then yearly.

## Design

- **Participants:** six to eight designers or engineers (up to ten if you can recruit them) (run the two disciplines as separate studies), mixed seniority, from consuming teams, not the system team. Record years of experience and prior system familiarity.
- **Tasks:** three representative tasks of the kind the system claims to help with (a form with validation, a settings screen, a card list with states). Each task has a written brief and a reference design or spec. Keep each under two hours.
- **Conditions:** each participant does the task twice, once from scratch (no system assets, a bare starter) and once with the system. Counterbalance the order across participants so half do "with" first. Use a different but equivalent task variant for the second run to reduce learning effects, or accept and report the learning effect if you cannot.
- **Timing:** self-timed with a stopwatch or time-tracking tool, start to "I would submit this," including time spent reading system docs.
- **Quality review:** two to three reviewers, blind to condition, score each output against the reference on visual fidelity and on an accessibility checklist (keyboard navigation, labels, contrast, focus order). Randomize review order.

## Sample size and what each n buys

State the participant count against an honest floor, never the folk claim that "five users is enough." Three reference points, from the corrected reading of the usability-sample research:

- **5 participants: directional.** Enough to surface the obvious, repeated problems and to point a result in a direction. Not enough to trust a rate or a mean.
- **10 participants: a reliable mean.** The floor for reporting a median or mean time per condition as more than directional. This is the band a study reporting median minutes should aim for.
- **20 participants: a roughly 95% detection floor.** What it takes to claim with high confidence that the study would have caught a real effect if one existed. Below it, call the study directional and claim no detection power it does not have.

This protocol asks for six to eight, up to ten. That sits in the directional-to-reliable band: run it as a directional study whose median is a small-sample estimate, put the n on every figure, and do not present it as a powered detection of the effect. If the decision the study feeds needs the higher confidence, recruit toward twenty and say so; if it only needs a direction, six to eight is honest as long as the number travels with the result.

Two choices here change what the n buys, and both belong in the report. The study is **within-subjects** (each participant runs both conditions), which reads a per-person difference more efficiently than comparing two separate groups, so it earns more from a small n than a between-groups design would. But its headline is a **median time**, a quantitative estimate: a confident claim that the difference is real beyond this sample is a power question (baseline, minimum detectable effect, confidence), not a usability-floor question, so do not borrow the 5 / 10 / 20 floor to stand in for it. Report the small-sample median honestly; do not dress it as a population effect. What counts as a good result, the percentage that would make the system "worth it," is a target the adopting team sets, not a number this protocol supplies.

## Consent and data handling (complete before you recruit)

Participants here are internal colleagues, timed and scored, which makes participant welfare a real obligation and not a formality. Complete this checklist before the first session. It is a list for a human to confirm, not a claim that consent is already handled.

- [ ] Informed consent captured: each participant is told the purpose, how the data is used, and how long it is kept, and agrees before starting.
- [ ] Recording and screen-capture permission taken separately, if any session is recorded.
- [ ] Right to withdraw at any point, without penalty, stated up front.
- [ ] Individual results are protected: one person's times and scores are never shown to their manager or used in a performance review. Report only in aggregate.
- [ ] Incentive, if any, is stated and handled the same way for everyone.
- [ ] Personal data is minimized. Where raw timings, notes, or recordings are stored, name the location, the retention period, and who deletes them when the study closes.
- [ ] Any recording or transcript ingested into a tool is treated as data on the way in: stripped of anything that could act on a system, and stamped with where it came from.

An internal study that leaks individual performance into management view will not earn honest participation twice. The protection line above is what keeps the times real.

## What to record

- Per participant, per task, per condition: minutes, reviewer scores, notes on where time went.
- Per participant: experience, prior familiarity, which order they ran.
- Anything that went wrong (missing component, docs gap): these are product findings, not noise.

## Analysis

- Report the **median** minutes per condition and the range. Mean as a secondary figure.
- Report the percentage difference as a range across tasks, not a single number.
- Report quality scores per condition; if the system condition is faster but scores lower, say so.
- State n, the task set, the order effect, and that participants were internal.

## Output

A one-page report:

1. Headline: "In a study of n = <N> <designers/engineers> on <3> tasks, the median time with the system was <X>% lower (range <a> to <b>), with <equal / higher / lower> quality scores."
2. A small table: task × condition × median minutes × quality score.
3. What the study cannot claim: organization-wide savings, effects on complex or novel work, effects for people with no system familiarity.
4. The product findings (missing components, docs gaps) as a list handed to the system roadmap.
5. Method appendix.

Store the study in `task_study` (artifact 02): medians in minutes per condition, the percentage range across tasks, and the quality scores per condition. That is all M4(a) reports; it is never multiplied by organizational volume.

## Pitfalls

- Choosing tasks the system is unusually good at. Let a consuming-team lead pick one of the three tasks.
- Letting the system team participate.
- Reporting the mean of a skewed distribution as the headline.
- Multiplying the study result by the whole organization's hours and calling it savings.
- Claiming detection confidence the sample size does not support: a six-to-eight-person study is directional, so present it that way rather than as proof the effect is real beyond the room.
- Running the study on colleagues without the consent and individual-result protection above in place first.
