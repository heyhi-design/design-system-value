---
title: Making the case for a design system
subtitle: What leadership looks for, what the evidence supports, and how to make the case retrievable by anyone in the organization
date: 2026-09-01
status: field guide, v0.3
classification: unclassified
audience: design system leads, design and engineering managers, anyone who has to defend or renew a design system budget
---

# Making the case for a design system

*A field guide. The question it answers: how does a design system tell the story of the money it saves, what does leadership actually look for in that story, and how does a team make the evidence available to anyone who needs it, on demand, without the design system team in the room. Everything here is meant to apply to any design system, in any organization, on any stack. Where the evidence is thin, the guide says so.*

---

## 0. The short answer

1. **Leadership is not asking "is the design system good." It is asking "what did I get for the money, compared to what, and what do you want me to decide."** The executive-facing frameworks behind this guide (Forrester's Total Economic Impact construction, the DX Core 4, platform-engineering ROI guidance, CFO-side procurement literature) reduce to the same three-part shape: a baseline, a measured change, and a decision tied to cost or value. No single source states it as a triad; the shape is a synthesis, and § 2 is reconstructed from those sources rather than from executive testimony (see § 9). Stories that lack any one of the three read as advocacy.

2. **One of the most consistently named reasons systems lose funding is perceived value, not actual value.** The 2026 zeroheight report shows satisfaction with leadership buy-in falling from 42% to 32% in one year, with dissatisfaction rising from 23% to 40%. The ranked failure data that exists (Sparkbox 2020) puts staffing and adoption first and a missing executive champion fourth; a practitioner who led a systems team through a layoff explains how those combine: the system supported hundreds of engineers and leadership did not know what it produced. Gartner, per zeroheight's reading of its 2025 Hype Cycle, now places design systems in the trough of disillusionment. This is a communication and instrumentation failure first, and a systems failure rather than a personal one: the artifact was built and the feedback loop to the people who fund it was not.

3. **The numbers that survive an executive's questions are smaller, sourced, and ranged.** Conservative beats impressive. A 5% efficiency estimate with a documented method outlives a 30% claim with none. Finance will accept clear definitions, a baseline window, a comparison method, documented confounders, and an auditable trail. It will reject before-and-after-only reporting, self-reported productivity monetized as hard savings, black-box vendor ROI, and double-counted benefits.

4. **Efficiency is the easiest ledger to open and the weakest one to stand on alone.** Time saved is real and measurable (the two small controlled studies landed at 34% and 47% on discrete tasks), but it is a soft saving. The two evidenced cases of a system attaching itself to a number the business already tracked are share of page views at IBM.com and pixel-level coverage of what users actually see at Preply. Conversion and retention in migrated flows, avoided legal exposure, and avoided duplicate spend across teams are candidate connections this guide recommends (§ 4.3, § 2.6), not documented funding outcomes.

5. **Adoption is a lagging indicator. Engagement, contribution, and sponsor participation lead it by months.** By the time coverage drops, the relationship that produced the drop went bad a quarter ago. A story built only on adoption percentages cannot warn anyone of anything.

6. **The story has to be a product story, not a project story.** The defunding line that circulates most (second-hand, untraced to a primary page; see § 1) is some version of "the system is done, why do we need all these people." A design system that reports like a project (built, shipped, finished) invites that conclusion. One that reports like a product (consumers, releases, roadmap, health, cost to run) does not.

7. **Retrievability is an architecture decision, not a reporting habit.** If the evidence lives in a deck, it dies with the deck. What the cited teams actually did: put the metrics into the analytics tool the organization already opens (Tableau at athenahealth, New Relic at Mews), refresh them automatically (nightly at Pinterest, every ten seconds at Mews), and break every number down by consuming team (Pinterest, Mews, Optimizely). What this guide adds as a proposal, with no cited team doing it yet: a public metric-definitions contract and a Metrics page on the design system's own documentation site (§ 6.1, § 6.3). The design system team should be the author of the numbers and never the bottleneck for reading them.

8. **Where to start:** § 7 is a ninety-day minimum version, § 8 is how to adapt it to your ownership model, size, tooling, and maturity, and the appendix holds three fill-in templates (the value ledger, the metric-definitions contract, the one-page report).

---

## 1. Why systems lose the room

The evidence on failure is more consistent than the evidence on success.

**Buy-in is collapsing while the work gets harder.** The zeroheight Design Systems Report 2026 (147 practitioners) reports buy-in satisfaction at 32%, down from 42% in 2025, with outright dissatisfaction at 40%, up from 23%. Sixty-one percent of teams say they are understaffed. The top challenge for the fifth consecutive year is "driving adoption and raising awareness." Respondents' own words: "leadership has no background in design so they don't understand what buy-in means"; there are "huge adoption gaps with no metrics to track them," which the report calls a vicious cycle. Only 37% of teams have any automation set up, and the measurement most teams do have is coarse: adoption (41%), component usage in design tools (41%), component usage in code (38%), accessibility compliance (36%), speed of development (31%).

**Most teams never measure at all.** The Sparkbox 2022 survey found only 16% of respondents tracked usage and satisfaction metrics, consistent with the prior year. In the 2020 survey, among systems rated unsuccessful, the cited causes were staffing (53%), adoption (52%), maintenance (38%), lack of an executive champion (36%), and funding (30%). Of systems rated successful, 81% had a maintenance process; of unsuccessful ones (in-house respondents), 46%.

**A practitioner who was cut describes the mechanism.** Josh Cusick, who led a systems team through a layoff: it "wasn't due to a lack of actual impact, but a lack of perceived value." The team supported hundreds of engineers; leadership was not aware of what it produced; a largely absent director led to a restructuring event. His conclusion is blunt: design systems "have promised ROI for years without delivering hard metrics," which is why they are first on the block. The line reported second-hand from another organization that cut a ten-person team, "the design system is done, why do we need all these people," is the project-versus-product failure in one sentence. (That quote surfaced only in search summaries and could not be traced to a primary page; treat it as illustrative, not citable.)

**The analyst framing has turned.** Per zeroheight's reading of Gartner's 2025 Hype Cycle, design systems are sliding from the peak of inflated expectations into the trough of disillusionment, "where early enthusiasm meets the hard realities of maintenance, adoption, and organizational buy-in." The same zeroheight report relays Gartner's view that "a codified design system will be essential to enable GenAI." Both are true, and the second is the opening for the next funding conversation.

**It is a never-ending job.** Ben Callahan's A List Apart essay makes the structural point: a design system has no direct revenue line, so it must be sold as an investment with residual benefit across the organization, and it must be re-sold continuously because the people, priorities, and budgets change underneath it.

**The failure sequence is organizational before it is technical.** Across the survey data and practitioner accounts, the order is consistent: maintenance velocity drops first (the backlog grows faster than it is processed), contribution dries up second, adoption degrades last. Any measurement instrument that watches only adoption is watching the last stage. The rest of this guide is about the instrument that would let leadership see the first two.

---

## 2. What leadership actually looks for

Reconstructed, not observed. No primary source was found in which a CFO, CPO, or CTO explains in their own words why they funded or cut a design system (§ 9). What follows is synthesized from executive-facing frameworks (Forrester TEI construction, the DX Core 4, platform-engineering ROI guidance, CFO-side procurement literature) and from the practitioner accounts that succeeded.

### 2.1 Baseline, change, decision

The minimum the finance-side sources describe is three things: a clear baseline, a measured change, and a decision tied to cost or value. A number without a baseline is a boast, and a change without a decision is a status update. The design system report should end with what leadership is being asked to do (fund, hold, expand, protect headcount, mandate adoption in a product line) and what the numbers say about that choice.

### 2.2 The executive's own problem, in the executive's own units

The Supernova executive-buy-in interviews land on one heuristic (Lauren LoPrete, Cash App): find the thing the executive is tired of hearing about, or passionate about, and show the system addressing it. The audience matrix that recurs:

| Audience | What they optimize | What to lead with | What to translate away from |
|---|---|---|---|
| CFO / finance | cost, risk, predictability | cost of the team stated first; avoided duplicate spend; payback period; ranged savings with method | "consistency," "craft," component counts |
| CTO / engineering | velocity, quality, retention | lead time on UI work; defect and accessibility regression rates; onboarding time; migration cost avoided | design vocabulary of any kind |
| CPO / product | time-to-market, outcomes | features shipped per quarter on system primitives; conversion or task completion in migrated flows | "adoption percentage" without an outcome attached |
| CMO / brand | trust, recognition, reach | consistency reframed as trust; rebrand or campaign turnaround time; accessibility as legal exposure | internal efficiency |
| Board / CEO | strategy, competitive position, risk | one number with a trend, one story, one risk avoided | everything else |

Callahan's version of the split is useful: a system owned by IT is sold on productivity; a system owned by marketing is sold on customer and end-user value. The same evidence gets two different front pages.

### 2.3 Conservative numbers that survive interrogation

Every credible practitioner source warns against the big number. PJ Onori (Instacart), via Supernova: you will not get 30% efficiency gains in year one, but perhaps 5%. The Smashing Magazine formula authors recommend rounding and stating a ±25% margin. The finance-side literature is explicit that the smaller number that survives questioning is worth more than the larger number that cannot. A useful house rule for any report: never insert a percentage without a source.

### 2.4 Hard savings, soft savings, and cost avoidance, kept separate

Finance distinguishes three things and discounts them differently:

- **Hard savings** show up on the P&L: a license retired, a vendor contract ended, a hire not made and the requisition closed. Design systems rarely produce these directly, and when they do (a consolidated tooling contract, a QA vendor scope reduced) they should be reported as such, separately.
- **Soft savings** are capacity: hours returned to designers and engineers. Real, but not bankable unless the capacity is visibly redeployed (a named team shipped a named thing with the returned time) or a hire was avoided.
- **Cost avoidance** is spend that would have occurred: the fifty teams that would each have built their own button; the accessibility lawsuit; the three-month rebrand that took three days.

The mistake that costs credibility is monetizing soft savings as if they were hard, or counting the same hours in two categories. Report all three, label them, and never sum them into one headline without saying so.

### 2.5 A connection to something the business already tracks

The stories that moved budgets borrowed an existing corporate metric rather than inventing one:

- **IBM.com** chose share of page views on Carbon as the KPI, because IBM.com's 20 million pages are not equally trafficked and page views connect directly to the traffic and engagement numbers leadership already watched. Result reported: 6.2% of page views on Carbon at the start of 2021 to 44.8% by November, described to leadership as seven-fold growth in ten months.
- **Preply** built visual coverage as a pixel-weighted metric of what users actually see, because "token usage or static analysis" do "not speak the same language as product teams," whose language is conversion, engagement, and retention.
- **Callahan** ties consistency to trust and then to the trust metrics marketing already reports: time on site, visit frequency, subscription rates, bounce rate, NPS.

### 2.6 Risk, not only return

Accessibility exposure is the cleanest risk story (Callahan cites the jump in U.S. web accessibility suits from 814 in 2017 to roughly 2,300 in 2018). Key-person risk is the second: a system that is a side project of whoever built it is an uninsured asset. Brand risk (inconsistent official surfaces undermine confidence and risk reading as fake, the argument NHS Digital makes for the GOV.UK system) is the third. Executives fund risk reduction more readily than efficiency, and risk does not require an ROI formula.

### 2.7 Trend, cadence, and a roadmap

Leadership wants to see the number move, which means the number must exist before the movement. The executive-scorecard literature converges on a row format: metric, current value, target, variance, a four-to-eight-period trend, one named owner, and an answer to "what do we do if this breaches." A design system that shows up once a year at budget time with a fresh deck is asking leadership to trust a snapshot. One that reports monthly from the same instrument is asking them to read a trend.

### 2.8 Traction before the ask

The Belka account of Serenis (three to five components per sprint shipped on unofficial time before formalizing the request) and the Smashing Magazine authors' advice to start federated, building the system "on the side" to lower perceived risk, point the same way: show the system helping a few teams before asking for headcount. Leadership funds momentum. The caveat is Nathan Curtis's: a federated model whose members are not relieved of other duties stalls, so the traction phase needs an end date and a headcount ask attached. The first-pitch story is about a small proven effect and the cost of not extending it; the renewal story is about a trend and a roadmap; the defense-against-cuts story is about what stops when the team stops.

---

## 3. The evidence base, with provenance grades

Practitioners cite the same dozen numbers back and forth, several of which do not trace to a source. Before any of these appear in your own deck or report, use the grade.

**Grades.** A: controlled or primary study with stated method and sample. B: first-person practitioner account with a described method. C: vendor- or analyst-commissioned, method partially disclosed, or explicit estimation. D: secondary or unsourced, circulates widely. X: unverifiable or contradicted; do not cite.

**Provenance state (the traceability axis, orthogonal to the grade).** The grade rates the strength of the study. A second axis rates whether the number can be traced to an inspectable primary, and each row carries one state, appended to its grade in the table: *verified-primary* (traces to an inspectable primary and the figure matches), *partially-verified* (an attribution exists but the primary was not inspectable when this was compiled, or the figure is second-hand), *unverifiable* (a source is offered but cannot be found or does not contain the claim), *unsourced* (no source is offered at all). The two axes are independent: a figure can be *verified-primary* on traceability yet carry a low grade for a small or undisclosed sample, and a widely repeated figure can read as authoritative yet be only *partially-verified* because its primary was never inspected (the McKinsey and InVision rows below are that second case). An *unverifiable* or *unsourced* number is flagged, never repeated as fact: the X and D rows are marked accordingly and stay on the do-not-cite list.

**One more flag, for the design-ROI figures.** A finding drawn from a correlation carries a *correlational* mark; a figure whose own wording asserts cause carries *causal-as-stated*; a modeled or projected figure carries *synthetic (modeled)* wherever it appears. A correlational finding repeated in causal language is mis-stated no matter how well it traces, which is why the two broad-practice design-ROI figures here (the McKinsey Design Index and the InVision maturity study) are marked *correlational* and, by construction, never stand as a headline number. They appear only in their row, with this note. Treat this as the standing caveat on every design-ROI figure, present in the table or not: the reader should be able to see that the numbers were read for correlation-versus-cause, not only for source quality.

| Claim | Source | Grade · state | Notes |
|---|---|---|---|
| Developers built a contact form 47% faster with IBM Carbon than from scratch (median 4.2 h vs 2.0 h) | Sparkbox study | A · verified-primary | n = 8 developers, self-timed; authors call it small and their team atypical (accessibility experts). Consistency gains clearer than accessibility gains. |
| Designers completed a task 34% faster with a directly applicable, up-to-date design system | Figma internal study ("Measuring the value of design systems") | B · verified-primary | Controlled task, but participant count is not disclosed. Ideal conditions stated explicitly; the article says real-world falls "somewhere in between." The "3.5 designers on a 7-person team" line is arithmetic on this number, not a separate finding. |
| Literature-average productivity gains: design 38%, development 31%; five-year ROI ≈135% in the worked example | Smashing Magazine formula (Klüver, Slack, Ray, Loomer, Sparkbox averaged) | B · partially-verified · synthetic (modeled) | The formula excludes onboarding, QA, research, scale, consistency, and accessibility benefits; authors recommend stating ±25%. Several of the averaged inputs are themselves grade C/D. |
| Dev Mode: 20–30% developer output increase; 98 min/week saved per developer; $10M efficiency over three years; $4M "reuse value" from design system usability | Forrester TEI for Figma Dev Mode | C · partially-verified · synthetic (modeled) | Composite organization built from four decision-maker interviews; one company's 200-developer survey supplied the minutes figure. Method for the money is not disclosed on the public page. Useful as a *shape*, not as a benchmark. |
| GOV.UK Design System delivers about £22m of benefit per year (the 2020 GDS podcast post gave £17m) | Tim Paul, who led design on the GOV.UK Design System at GDS; GDS blog 2020 | C · partially-verified | Public-sector benefit estimate from the product's own lead; method not published on either page. Also: services built on the system are roughly twice as fast in Lighthouse. |
| IBM Carbon roadmap KR: development efficiency averaging 2,000 hours saved per offering; 80% of IBM Software offerings on Carbon by end of 2022 | Carbon GitHub roadmap wiki | n/a (target) | A target, not a measured result, so it carries no evidence grade or provenance state. Illustrates how a mature system states business-impact KRs. |
| IBM.com pages on Carbon: 6.2% → 44.8% of page views in ten months (legacy system 54% → 21%) | Knapsack, "Lessons learned from working on Carbon for IBM.com" | B · verified-primary | Author warns that instrumentation cannot always distinguish partial from full compliance; "scrutinize every number." |
| Badoo: two visibly distinct eras in three years of UI-code git history (large frequent changes before, small infrequent after); coverage ~50% → ~80% in under a year | Cristiano Rastelli (Badoo Cosmos) | B · partially-verified | Method: Node script over git history, plotted with D3. Author is explicitly cautious about proving adoption quantitatively. Primary page was unreachable when this guide was compiled; details via secondary summaries. |
| Mews production adoption: 53% on the most complex product, 60% on the guest-facing app; a third, acquired product growing about 5% a month | Mews engineering blog | B · verified-primary | DOM-element ratio, Babel-marked components, sampled every 10 s in production, reported in New Relic by product, team, and route. Explicitly a stakeholder-friendly coverage number rather than a debt number. |
| Pinterest: Figma-side adoption = Gestalt layers ÷ total layers on handoff pages, nightly via REST API, by team and file | Figma blog on Pinterest Gestalt | B · verified-primary | Used to justify cross-platform component investment; design adoption revealed component limitations (PageHeader) that code adoption alone hid. |
| athenahealth processes ~100,000 component insertions a month; detachment patterns reviewed monthly in Tableau | Figma "Design Systems 104" | B · verified-primary | Example of putting design-system data into the BI tool the org already uses. |
| Headspace 20–30% time savings on simple tasks, up to 50% on complex; Vanguard 50% faster design updates; Swiggy feature rollout time halved | Figma blog | C · partially-verified | Company self-reports relayed by a vendor; no method. |
| Netguru Silk design system: MVP 6 → 3 months; rebrand core UI in 2 days, full rollout ~3 working days | Netguru | C · partially-verified | Agency case; useful as an event-based measurement example. |
| Button component: 14–15 h without a system vs 2.5 h with; larger feature 73–85.5 h vs 25.5–36 h | Xebia | C · partially-verified · synthetic (modeled) | Estimation, not measurement, but a clean template for a per-task ledger. |
| "And you thought buttons were easy": 200 h × $100/h = $20k per team; × 50 teams = $1M of buttons | Nathan Curtis, EightShapes | C · partially-verified · synthetic (modeled) | Illustrative arithmetic, not a measurement, and the single most portable "cost of not" framing in the field. |
| Icon pipeline automation $100k+/yr; brand-refresh component migration tool $30k of design hours; token-to-code automation 50% faster, 75% fewer QA bugs | Josh Cusick | B · verified-primary | First-person, dollarized per initiative. The model for tying dollars to named work items. |
| REA Group's design system saved roughly 300k hours (The Design System Guide quotes 320k) | REA Group blog, "The value of REA's design system" (primary), relayed by Supernova and The Design System Guide | B (provisional) · partially-verified | Primary exists and reports the figure as tracked, but the REA page was unreachable when this guide was compiled, so the number and method are unconfirmed here and the two secondaries disagree. Verify before citing. |
| Knapsack calculator benchmarks: 30% QA time reduction, 20% efficiency, 15% faster to market; "$3M" Fortune 500 case | Knapsack | D · unsourced | Vendor, no sources on page. |
| Design systems reduce design debt 60–75% and tech debt 55–70%; inconsistent UI raises user errors 34%; McKinsey "28% higher support costs"; Baymard "41% interaction cost" | Various SEO blogs | X · unverifiable · do not cite | None traced to a primary study. Do not cite. |
| Atlassian: 67% less duplicate code, sprint time two weeks → 3.5 days | beyondlabs.io and similar | X · unverifiable · do not cite | Not on any Atlassian property; not found in Atlassian's own design blog. Do not cite. |
| Polaris apps launch 40% faster, 12% vs 28% first-month churn, 60% fewer UI tickets | tenten.co | X · unverifiable · do not cite | Marketing page, unsourced. Do not cite. |
| McKinsey Design Index: top-quartile firms had revenue growth 32 percentage points higher and total shareholder return 56 percentage points higher than peers over five years | McKinsey, "The Business Value of Design" (2018) | C · partially-verified · correlational | Analyst study of design practice broadly across 300 listed companies, not design systems. Compiled here from a search summary rather than the primary, so partially-verified; and correlational, a design-maturity correlation rather than a causal finding. Legitimate context for a board, illegitimate as a design-system ROI figure. |
| InVision New Design Frontier: Level 5 companies are about 4× as likely as Level 1 to report a revenue impact from design, 5× for cost savings, 6× for time-to-market; only 5% of companies at Level 5 | InVision (2019) | C · partially-verified · correlational | Self-reported survey of 2,200+ organizations, design maturity broadly. Same caveat as McKinsey: correlational, and about design practice, not design systems. |

Two observations from building this table. First, only two controlled studies exist and both are small: 34% (Figma, n undisclosed) and 47% (Sparkbox, n = 8) faster on a discrete UI task with a relevant, maintained system. Treat 30–50% as a plausible band to test in your own organization, not as a benchmark to quote. Second, the numbers that circulate most (the Atlassian sprint claim, the debt-reduction percentages) are the ones with no home, and the more a practitioner repeats them the more an executive who checks will discount everything else they said.

---

## 4. The measurement architecture: three ledgers, plus the leading indicators

Treat the case as a set of ledgers that stay open, rather than a calculation performed once. A fill-in version of the ledger is in Appendix A.

### 4.1 Ledger 1: what the system costs (state it first)

Leadership trusts a team that names its own cost before anyone asks.

- **People.** Headcount × loaded cost. One published rule of thumb (Figr's estimation guide) is salary × 2 for fully loaded; the "Design Systems Aren't Cheap" example is five engineers, four designers, two design technologists producing about 30 components in a year at roughly $1.1M in salaries before benefits. Design System University's framing is the sharpest: a five-person team at $100k average costs $41,667 a month, so a component that takes a month must return at least that, and a button that saves two hours per consumer needs about 434 consumers to break even.
- **Tooling and platform.** Documentation platform, design tooling seats, analytics, CI.
- **Maintenance.** The Smashing Magazine worked example budgets ongoing maintenance at 10% of team time after ramp-up (against 30% during it), an authors' assumption rather than a measurement; Supernova's business-case guide rounds this to "at least a month per year." Framework or tool migrations (a variables migration, a framework major) are lumpy costs that belong in the projection.
- **Cost of the consuming teams' time** for adoption and contribution, if the organization counts it.

This is also the denominator for every ratio below. Support ratio (systems designers to consumers; LoPrete's team runs at roughly 1:60) belongs here as the understaffing argument stated in one number.

### 4.2 Ledger 2: hours (the efficiency case), by method credibility

In descending order of how well the number holds up:

1. **A controlled internal task study.** The Sparkbox and Figma designs are cheap to replicate: pick three representative tasks, six to eight designers or developers, with and without the system, self-timed, with the outputs blind-reviewed for quality. Small n is fine if stated. This produces the organization's own number, which beats any borrowed benchmark.
2. **Event-based measurement (natural experiments).** A rebrand, a dark theme, a spacing overhaul, an accessibility remediation, a framework migration. Hours before the system (from the last time it happened, from tickets, from estimates) versus hours this time. This is the strongest single story a system ever gets, because the event is one leadership already noticed and paid for. Instrument the next one in advance.
3. **Avoided duplication, counted.** Curtis's arithmetic with the organization's real numbers: how many teams would have built it, at what cost each. An interface inventory (the "37 button styles" screenshot wall) is the visual proof that the duplication was real, not hypothetical.
4. **Self-reported time saved, repeated.** Ask consumers quarterly how many hours a week the system saves them; report the aggregate as a trend, never as a dollar figure of hard savings. LoPrete goes further and calls any quantitative approach to velocity "a waste of time," preferring consumer-team case studies; this guide disagrees in part, keeping quantitative velocity only when it comes from a controlled study or an instrumented event (methods 1 and 2), and otherwise agrees. Finance accepts the survey as a directional soft saving if labeled.

Convert hours to money with a fully loaded rate, state the rate, and present a pessimistic and optimistic case rather than a point estimate.

### 4.3 Ledger 3: outcomes and quality (the case that is not about hours)

- **Coverage of what users see.** Three implementations, in ascending fidelity: import or dependency scans (cheap, blind to whether the import renders); DOM-element ratio in production (Mews); pixel-weighted visual coverage in production (Preply, open-sourced). Segment by team, product, and route. Pair with a counter-metric (detachments, overrides, arbitrary values) or the percentage will be gamed by wrapping.
- **Defects and regressions.** UI-inconsistency bugs, accessibility regressions caught in QA, visual-diff failures, per release, on-system versus off-system surfaces.
- **Product outcomes in migrated flows.** Conversion, task completion, support tickets tagged UI-confusion, before and after a flow moves onto the system, with a comparison flow that did not move (difference-in-differences, not before/after alone).
- **Time-to-market.** Lead time for UI-heavy features on system primitives versus bespoke, same team, same quarter.
- **Accessibility posture.** Conformance level of system-served surfaces, tracked; the risk ledger's evidence.
- **Consumer satisfaction.** A short quarterly survey of designers and engineers: "meets my needs," "helps me work faster," would-recommend. The design system's own NPS.

### 4.4 Leading indicators (what moves before adoption does)

Adoption lags because code changes slowly. The signals that move first:

- **Engagement** (Headway's model): office-hours participation normalized by team size, contribution participation (requests, bugs, docs), support participation, rolled into a composite on a three-month rolling average. Their case: engagement fell to 79% while adoption was unchanged, and the drop was the early warning.
- **Sponsor engagement in rituals** (Curtis; Rolla): does the executive sponsor attend release planning and reviews. Curtis's sample OKRs make this a tracked number.
- **Contribution velocity and review SLA adherence.** Whether a documented contribution process is actually resourced and running on time.
- **Release predictability.** Releases shipped on the published schedule.
- **Documentation traffic and search-miss rate.** Where consumers look and do not find.

This is the layer that lets the monthly report say "the system is fine today and will not be in two quarters unless X," which is the only kind of warning leadership can act on.

### 4.5 Counter-metrics and the attribution problem

Every metric on the executive page needs a paired oppositional metric (the DX Core 4 principle: throughput paired with experience, speed with quality). Coverage with detachments. Insertions with satisfaction. Velocity with defect rate. Contribution volume with review SLA.

On attribution: never claim causality from an organization-wide trend. Use natural experiments, adopted-versus-not comparisons at team level, ranges, and explicit confounder lists. The Badoo git-history analysis is the model of an honest before/after: it shows two eras and lets the reader draw the conclusion, with the author on record saying he is wary of proving adoption by numbers alone.

---

## 5. The story shape

### 5.1 The one page

Modeled on how Forrester constructs a TEI narrative (steal the structure, not the numbers): a defined baseline organization, benefits quantified by category, benefits *not* quantified listed explicitly, costs, risk adjustment, and a payback horizon. A fill-in version is in Appendix C.

1. **Headline number with a trend.** One number, baseline → now → target, four to eight periods of history, one owner. Usually coverage of what users see, or hours returned, depending on audience.
2. **The scorecard row.** Three to five metrics in the standard row format (name, value, target, variance, sparkline, owner). Ledger 1's cost line is one of them.
3. **One proof story.** An event-based measurement in three sentences: what happened, what it cost last time, what it cost this time. Screenshots if the audience is visual.
4. **What we are not counting.** The unquantified benefits, named. This is what makes the quantified ones believable.
5. **Risk avoided.** One item: accessibility exposure, key-person dependency, brand inconsistency, migration debt.
6. **The ask, as a decision.** Fund, hold, expand, mandate, protect. With what changes if the answer is no.

### 5.2 Three occasions, three stories

| Occasion | Lead with | Evidence weight | Close with |
|---|---|---|---|
| First funding | the interface inventory and the duplication arithmetic; a small proven effect on two or three teams | cost of not; one internal task study | a bounded ask with a date and a defined stopping point |
| Renewal / annual | trend on the headline metric; the year's event-based proofs; cost per consumer falling | Ledgers 1–3 with the leading indicators | the roadmap as a product roadmap; next year's measurable targets |
| Defense against cuts | what stops when the team stops: release cadence, contribution SLA, the queue of consuming teams | engagement and sponsor metrics; support ratio; named work items with dollars | the cost of re-forming the team later versus holding it now |

### 5.3 Language that travels

From Callahan and the executive interviews: consistency becomes **trust**; efficiency becomes **capacity** (and say what the capacity shipped); "done" becomes **a product with consumers and a roadmap**; accessibility becomes **risk**; "the design system team" becomes **the platform that N products run on**. Say, with PJ Onori, "design systems for software *is* software" when the audience is engineering; it repositions the team from overhead to infrastructure.

### 5.4 Anti-patterns that cost credibility

- Quantitative velocity claims that do not come from a controlled study or an instrumented event.
- A dashboard with forty metrics (the Design System Guide's line: if it is not actionable it is a vanity metric).
- A 30% year-one promise.
- Reporting only at budget time.
- Causal language on a correlational trend.
- Any percentage without a source, including the ones in § 3 marked X.
- Requiring design-system sign-off as a gate; it reads as bureaucracy and slows the numbers the team is trying to improve.

---

## 6. Making the evidence pullable by anyone

This is the part most teams skip, and it is the part that determines whether the case exists when the design system lead is on vacation, has left, or is not invited to the meeting.

### 6.1 Principle: metrics are a product surface of the system

Ship the numbers on the same cadence and in the same place as the components. If the design system's documentation site has a Components section and a Tokens section, it has a Metrics section, with live values, definitions, and a changelog. Optimizely's systems engineer on the Omlet dashboard: "very helpful when communicating this information to stakeholders" compared to text. The medium matters because the reader is not the author.

### 6.2 The data layers and what each can actually give you

| Layer | Source | What it yields | Access reality |
|---|---|---|---|
| Design-side | Figma Library Analytics | components, styles, variables (styles/variables since Oct 2024); instances, insertions, detachments; by team and file; up to 12 months history; daily refresh | Organization and Enterprise plans only. CSV export appears only when more than five teams use the library. REST Library Analytics API is Enterprise-only. Pinterest and others predate this and built their own nightly REST scrapers (FigStats). Other design tools: check for an equivalent usage export before assuming none exists. |
| Code-side, static | Omlet (React/React Native CLI), custom import scans, Storybook | which components are imported where, by repo and team; trend over time; prop usage | Omlet covers React and React Native; anything else is a script over your package graph. Blind to whether the import renders. |
| Production, runtime | Preply visual-coverage script (open-sourced); Mews Babel-marker + 10 s sampler to New Relic; IBM.com page-view share via web analytics | what users actually see, weighted; by product, team, route | A build-time marker plus a lightweight runtime sampler is a few days of engineering. Reuses the analytics or APM tool already in place. |
| Consumers | quarterly survey of designers and engineers | satisfaction, self-reported hours saved, needs met | A form. The hard part is running it every quarter. |
| Engagement | office-hours attendance, contribution tickets, support channel | the leading indicators in § 4.4 | Counting things that already happen; normalize by team size. |
| Cost | HR or finance headcount data, tooling invoices, time tracking | Ledger 1 | Usually a spreadsheet the finance partner already maintains. Ask them to own it. |

### 6.3 The definitions contract

For each metric, one page that anyone can read: definition, formula, source system, exclusions, refresh cadence, owner, known ways to game it, the paired counter-metric, and the date the definition took effect. Versioned. This is the artifact that turns an argument about the numbers into a reference to the document. A fill-in template is in Appendix B.

### 6.4 Where the numbers live

- **One table per metric in the warehouse or analytics tool leadership already opens** (Tableau at athenahealth, New Relic at Mews, Looker, whatever the operating review runs on). Not a design-team-only tool. One source of truth, one owner per KPI.
- **An executive view** with the five-number scorecard and the trend, and **a team view** where every number breaks down by consuming team, product, and route. The per-team breakdown is what turns adoption from a design-system plea into a product-team conversation (Optimizely used it as an adoption scoreboard; Pinterest and Mews report by team).
- **The Metrics page on the docs site**, embedding or linking the same views, with the definitions contract beside them.
- **An auto-generated monthly health report** rendered from the same tables: the one page from § 5.1, produced by a script, reviewed by a human, sent on a fixed date.
- **A quarterly narrative and an annual impact report** that reuse the monthly instrument and add the event-based proofs and the roadmap.

### 6.5 Sequencing

Instrument before the migration event, not after (Figma's guidance: do not wait until launch). Baseline first, then build. A system that cannot show the "before" has no story for the "after."

---

## 7. A minimum viable version

For a team with no instrumentation today.

| Window | Do | Produces |
|---|---|---|
| Week 1–2 | Ledger 1 spreadsheet with a finance partner; interface inventory of one product | the cost line; the duplication picture |
| Month 1 | pick one coverage method and baseline it (start with import scans if nothing else; move to runtime); first consumer survey; write the definitions contract for three metrics | baseline numbers; the contract |
| Month 2 | instrument the next natural event (theme, rebrand, remediation) before it starts; stand up the dashboard in the existing BI tool with a team breakdown | first proof story; the executive view |
| Month 3 | first one-page report on the fixed cadence; sponsor invited to the release review and attendance recorded | the trend begins; the leading indicators begin |
| Quarterly | rerun the survey; publish the Metrics page; add one metric per quarter, retire vanity ones | the durable instrument |

---

## 8. Adapting this to your organization

The architecture above is the same everywhere. Four things change what you lead with and how much of it you build.

### 8.1 By who owns the system

| Ownership | Headline metric to lead with | First proof story | Sponsor to instrument |
|---|---|---|---|
| Engineering / platform | coverage in production, by team; lead time on UI work | a migration or framework upgrade done once instead of N times | the engineering director's attendance at release review |
| Design / DesignOps | design-side adoption on handoff pages; consumer satisfaction | a rebrand or theme shipped in days | the head of design's participation in roadmap planning |
| Product | features shipped on system primitives; outcomes in migrated flows | one flow's conversion or task completion after migration, with a control flow | the CPO's quarterly review slot |
| Marketing / brand | consistency reframed as trust metrics; campaign turnaround | a campaign or landing-page family produced without bespoke UI | the CMO's brand review |
| Shared / federated | engagement and contribution velocity (the health of the federation itself) | avoided duplication counted across the contributing teams | every contributing team's manager, by name |

### 8.2 By size

- **One or two people, one product.** Skip the dashboard. Keep Ledger 1 honest, run one event-based measurement a year, run the consumer survey, and put the three numbers in the same monthly update the product team already sends. The definitions contract can be a single page.
- **Three to ten people, a few products.** The full ninety-day plan in § 7. One coverage method in production, the team breakdown, the monthly one-pager, the Metrics page.
- **Ten or more people, many products or platforms.** Everything above, plus per-platform coverage, the composite engagement score, an annual impact report, and a named owner for each KPI who is not the design system lead. At this size the support ratio and the cost per consumer are the numbers that decide the headcount conversation.

### 8.3 By tooling reality

- **No analytics plan tier in the design tool.** Baseline on the code side first (import scans, then a runtime marker). Design-side adoption can wait; production coverage is the number leadership will believe anyway.
- **No BI tool in the organization.** Use whatever the operating review already reads, even if it is a spreadsheet. The rule is not "use a BI tool"; it is "never make leadership open a design-team tool to see the numbers."
- **Multiple frameworks or platforms.** Report coverage per platform and never average them; the average hides the platform that is drifting.
- **A documentation platform with built-in analytics.** Use it for documentation traffic and search misses, and still put the coverage and cost numbers in the organization's tool.

### 8.4 By maturity

- **Pre-funding.** Interface inventory, the duplication arithmetic, one small controlled task study, a bounded ask with a stopping date.
- **Funded, unmeasured.** Ledger 1 first, then baseline coverage, then the contract. Do not report anything until there are two periods of data.
- **Measured, unread.** The numbers exist and nobody outside the team looks at them. Move them into the organization's tool, add the per-team breakdown, and put the one-pager on a fixed date. This is the most common state and the cheapest to fix.
- **Read, unprotected.** Leadership reads the report and the budget still gets cut. The missing pieces are usually the leading indicators (so the report warns rather than describes) and the risk ledger (so the story is not only about efficiency). Also check whether the sponsor is a person or a title; if the named sponsor left, the system has no sponsor.

---

## 9. What this guide does not settle

- The GOV.UK £22m/year benefit estimate's method is not on the public page; a GDS or NAO document may hold it.
- REA Group's hours-saved figure has a primary source (the REA Group blog) that was unreachable when this guide was compiled; the secondaries disagree (300k vs 320k) and the method is unconfirmed.
- Rastelli's Badoo article, Curtis's OKR article, Deliveroo's health-metrics article, and Rolla's Latin American edtech metrics article were unreachable when this guide was compiled (403s and connection refusals on Medium and eightshapes.com); their content here comes from search summaries and should be re-read before quoting.
- No primary source was found for an executive (CFO, CPO, CTO) describing in their own words why they funded or cut a design system. The executive view in § 2 is reconstructed from practitioners who succeeded and from adjacent finance and platform-engineering literature. A short interview set would strengthen it materially.
- Sparkbox has not published a survey since 2022 in anything found; zeroheight's report is now the field's annual instrument.

---

## Appendix A. The value ledger (fill-in)

Copy this table. Fill only the rows you can source; leave the rest blank rather than estimating without saying so. Every dollar figure carries the loaded rate used and a pessimistic/optimistic pair.

| Ledger | Line | Value | Method / source | Period | Owner | Grade of your own evidence |
|---|---|---|---|---|---|---|
| 1 Cost | Team headcount × loaded cost | | HR data; loaded rate = | annual | finance partner | |
| 1 Cost | Tooling and platform | | invoices | annual | | |
| 1 Cost | Maintenance and migrations (projected) | | | next 12 mo | | |
| 1 Cost | Support ratio (system staff : consumers) | | | current | | |
| 2 Hours | Controlled task study result | | n = ; tasks = ; with/without | one-off, repeat yearly | | |
| 2 Hours | Event-based measurement (name the event) | | hours last time vs this time; source of "last time" | per event | | |
| 2 Hours | Avoided duplication | | teams that would have built it × cost each | per component family | | |
| 2 Hours | Self-reported hours saved per consumer per week | | survey, n = , response rate = | quarterly | | (soft; never monetized as hard) |
| 3 Outcomes | Coverage of what users see | | method (import / DOM / pixel); by team and route | monthly | | |
| 3 Outcomes | Counter-metric (detachments / overrides / arbitrary values) | | | monthly | | |
| 3 Outcomes | UI defects and a11y regressions per release, on vs off system | | | per release | | |
| 3 Outcomes | Outcome in a migrated flow vs a control flow | | conversion / completion / tickets; DiD | per migration | | |
| 3 Outcomes | Consumer satisfaction (meets needs / faster / recommend) | | survey | quarterly | | |
| Leading | Engagement composite (office hours, contributions, support), 3-mo rolling | | normalized by team size | monthly | | |
| Leading | Sponsor attendance at release planning and reviews | | | per ritual | | |
| Leading | Contribution review SLA adherence; release predictability | | | monthly | | |
| Risk | Accessibility conformance of system-served surfaces | | | quarterly | | |
| Risk | Key-person dependency (named backups per critical area) | | | quarterly | | |
| Not counted | Benefits deliberately left unquantified (list) | | | | | |

## Appendix B. Metric definition (one per metric, fill-in)

```
Metric name:
One-line definition (in words a non-specialist reads once):
Formula:
Source system(s) and table(s):
Inclusions / exclusions:
Segmentation available (team, product, route, platform):
Refresh cadence:
Owner (one named person):
Baseline value and date:
Target and date:
Known ways this can be gamed:
Paired counter-metric:
What we do if it breaches:
Definition version and effective date:
Change log:
```

## Appendix C. The one-page report (fill-in)

```
[System name] health report, [period]                              Owner: [name]

HEADLINE
[Metric]: [baseline] → [now] → [target]     Trend (last 6 periods): [sparkline or six values]

SCORECARD (3–5 rows)
Metric | Now | Target | Variance | Trend | Owner
[cost per consumer or team cost] | | | | |
[coverage of what users see] | | | | |
[counter-metric] | | | | |
[leading indicator] | | | | |
[outcome or risk metric] | | | | |

ONE PROOF
[What happened this period.] [What it cost the last time it happened.] [What it cost this time, and how we know.]

WHAT WE ARE NOT COUNTING
[Two or three named benefits left unquantified, and why.]

RISK
[One risk the system currently reduces or carries, stated in the organization's terms.]

THE DECISION
[Fund / hold / expand / mandate / protect: the specific ask.]
[What changes if the answer is no.]

Definitions: [link to the metric-definitions page]     Data: [link to the dashboard]
```

---

## Sources

Fetched directly when this guide was compiled unless marked (s) for search-summary-only.

- zeroheight, Design Systems Report 2026: https://report.zeroheight.com/
- zeroheight, Design Systems Report 2025 (PDF) (s): https://othr.zeroheight.com/hubfs/zeroheight%20-%20Design%20System%20Report%202025%20-%20release%20version.pdf
- Sparkbox, The Value of Design Systems Study (Carbon): https://sparkbox.com/foundry/design_system_roi_impact_of_design_systems_business_value_carbon_design_system
- Sparkbox, 2022 Design Systems Survey: https://designsystemssurvey.sparkbox.com/2022/
- Sparkbox, 2020 Design Systems Survey: https://designsystemsurvey.sparkbox.com/2020/
- Smashing Magazine, One Formula To Rule Them All: The ROI Of A Design System: https://www.smashingmagazine.com/2022/09/formula-roi-design-system/
- Figma, Measuring the value of design systems: https://www.figma.com/blog/measuring-the-value-of-design-systems/
- Figma, Design Systems 104: Making Metrics Matter: https://www.figma.com/blog/design-systems-104-making-metrics-matter/
- Figma, How Pinterest's design systems team measures adoption: https://www.figma.com/blog/how-pinterests-design-systems-team-measures-adoption/
- Figma, Forrester analyzes the ROI of Dev Mode: https://www.figma.com/blog/forrester-analyzes-the-roi-of-dev-mode/
- Figma Help, Library analytics: https://help.figma.com/hc/en-us/articles/360039238353
- Supernova, Getting executive buy-in and proving ROI of design systems: https://www.supernova.io/blog/getting-executive-buy-in-proving-roi-design-systems
- Supernova, How to build a business case for your design system: https://www.supernova.io/blog/how-to-build-a-business-case-for-your-design-system
- Supernova, 9 design system metrics that matter: https://www.supernova.io/blog/9-design-system-metrics-that-matter
- Into Design Systems / Preply, Measure design system impact with visual coverage: https://www.intodesignsystems.com/blog/measure-design-systems-impact
- Mews, Building a design system adoption metric from production data: https://developers.mews.com/design-system-adoption-metric-building/
- Headway, Design system adoption vs engagement: https://www.headway.io/blog/design-system-adoption-vs-engagement
- The Design System Guide, metrics collection: https://thedesignsystem.guide/design-system-metrics
- The Design System Guide, calculating design system costs: https://thedesignsystem.guide/blog/a-guide-for-calculating-design-system-costs
- Design System University, The ROI of a Design System Team: https://designsystem.university/articles/the-roi-of-a-design-system-team
- Cory LaViska, Design Systems Aren't Cheap: https://www.abeautifulsite.net/posts/design-systems-arent-cheap/
- Nathan Curtis, Measuring Design System Success (s): https://medium.com/eightshapes-llc/measuring-design-system-success-d0513a93dd96
- Nathan Curtis, And You Thought Buttons Were Easy? (s): https://medium.com/eightshapes-llc/and-you-thought-buttons-were-easy-26eb5b5c1871
- Nathan Curtis, The Fallacy of Federated Design Systems (s): https://medium.com/@nathanacurtis/the-fallacy-of-federated-design-systems-23b9a9a05542
- Cristiano Rastelli, Measuring the Impact of a Design System (s): https://medium.com/@didoo/measuring-the-impact-of-a-design-system-7f925af090f7
- Josh Cusick, The future of design systems: https://joshcusick.substack.com/p/the-future-of-design-systems
- Ben Callahan, The Never-Ending Job of Selling Design Systems (A List Apart): https://alistapart.com/article/selling-design-systems/
- Belka, How to convince management that a design system is a good investment: https://belkadigital.com/blog/how-to-convince-management-that-a-design-system-is-a-good-investment
- Knapsack, Lessons learned from working on Carbon for IBM.com: https://www.knapsack.cloud/blog/lessons-learned-from-working-on-carbon-for-ibm-com
- Knapsack, Design System ROI Calculator: https://www.knapsack.cloud/calculator
- IBM Carbon, Roadmap wiki: https://github.com/carbon-design-system/carbon/wiki/Roadmap
- Tim Paul, Creating the GOV.UK Design System: https://www.timpaul.co.uk/posts/creating-the-govuk-design-system/
- GDS blog, Podcast: GOV.UK Design System (the £17m estimate): https://gds.blog.gov.uk/2020/02/28/podcast-gov-uk-design-system/
- REA Group, The value of REA's design system (primary for the hours-saved figure; unreachable when compiled): https://www.rea-group.com/about-us/news-and-insights/blog/the-value-of-reas-design-system/
- NHS Digital blog, Why should we build services using a design system: https://digitalhealth.blog.gov.uk/2022/06/08/why-should-we-build-services-using-a-design-system/
- Zeplin, How Optimizely uses Omlet: https://blog.zeplin.io/optimizely-harmony-session-2023
- Netguru, ROI of having a design system: https://www.netguru.com/blog/roi-design-systems
- Xebia, How to save 35 hours using a design system: https://xebia.com/blog/how-to-save-35-hours-using-a-design-system/
- Figr, How to measure and prove the impact of your design system: https://figr.design/blog/how-to-measure-and-prove-the-impact-of-your-design-system
- Figr, How to estimate the cost of creating a design system (loaded-cost rule of thumb) (s): https://figr.design/blog/how-to-estimate-creating-a-design-system-methodologies
- Aquent Studios, Is your design team proving its value: https://aquentstudios.com/blog/is-your-design-team-proving-its-value/
- DX, Introducing the DX Core 4: https://newsletter.getdx.com/p/introducing-the-dx-core-4
- Platform Engineering, How to measure developer productivity and platform ROI: https://platformengineering.org/blog/how-to-measure-developer-productivity-and-platform-roi-a-complete-framework-for-platform-engineers
- Ascend Framework, Designing a leadership scorecard (scorecard row format) (s): https://www.ascendframework.org/resources/scorecard-design-guide
- McKinsey, The Business Value of Design (s): https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-business-value-of-design
- InVision, The New Design Frontier (s): https://www.dexigner.com/news/31748
- Forrester TEI methodology overview (s): https://www.linkedin.com/pulse/overview-forresters-total-economic-impacttei-lisa-david
- Arkestro, Cost avoidance vs hard savings, how CFOs measure value (s): https://arkestro.com/blog/cost-avoidance-vs-hard-savings-how-cfos-actually-measure-procurement-value/

---

*The evidence table carries provenance grades so that readers can decide for themselves what to repeat. Nothing here is a benchmark; everything here is a method. The kit in `kit/` is the set of artifacts that act on this guide.*
