// build-screens.js — recorded from the reference template. Rebuilds the four value-surface screens
// (exec one-pager, team view, event ledger, leading feed) from the two components
// (build-components.js) over the Semantic variables (build-variables.js). Every fill, stroke,
// padding, and radius is bound to a variable by NAME; no node or variable id is used. Text carries
// the template's own example strings; run populate-runbook.md afterwards to fill a design
// system's numbers. Run inside the design tool's script runner (use_figma, figma-use skill loaded
// first). Set BUILD to a subset to build fewer screens per call.

const BUILD = ['Screen 1', 'Screen 2', 'Screen 6', 'Screen 7'];

const collections = await figma.variables.getLocalVariableCollectionsAsync();
const wanted = new Set(collections.filter((c) => c.name === 'Primitives' || c.name === 'Semantic').map((c) => c.id));
if (wanted.size !== 2) throw new Error('expected collections named Primitives and Semantic (run build-variables.js first)');
const V = {};
for (const v of await figma.variables.getLocalVariablesAsync()) if (wanted.has(v.variableCollectionId)) V[v.name] = v;
const need = (n) => { if (!V[n]) throw new Error('variable missing: ' + n + ' (run build-variables.js first)'); return V[n]; };
const solid = (n) => figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: { r: 0, g: 0, b: 0 } }, 'color', need(n));
const bindNum = (node, field, n) => node.setBoundVariable(field, need(n));
const bindPad = (node, spec) => { const m = typeof spec === 'string' ? { t: spec, r: spec, b: spec, l: spec } : spec; if (m.t) bindNum(node, 'paddingTop', m.t); if (m.r) bindNum(node, 'paddingRight', m.r); if (m.b) bindNum(node, 'paddingBottom', m.b); if (m.l) bindNum(node, 'paddingLeft', m.l); };
const bindRadius = (node, n) => ['topLeftRadius', 'topRightRadius', 'bottomLeftRadius', 'bottomRightRadius'].forEach((f) => bindNum(node, f, n));
const numValue = (n) => { const v = need(n); return v.valuesByMode[Object.keys(v.valuesByMode)[0]]; };
const SZ = { H: 'HUG', F: 'FILL', X: 'FIXED' };
const page = figma.currentPage;
const COMP = {};
for (const c of page.findAllWithCriteria({ types: ['COMPONENT'] })) if (c.name === 'Stat tile' || c.name === 'Delta chip') COMP[c.name] = c;
for (const name of ['Stat tile', 'Delta chip']) if (!COMP[name]) throw new Error('component missing on this page: ' + name + ' (run build-components.js first)');
const isScreen = (name, b) => name === b || name.startsWith(b + ' ');
for (const n of page.children) for (const b of BUILD) if (isScreen(n.name, b)) throw new Error('screen already exists: ' + n.name + ' (' + n.id + ')');

async function text(chars, style, size, fill, ar) {
  await figma.loadFontAsync({ family: 'Inter', style });
  const t = figma.createText();
  t.fontName = { family: 'Inter', style };
  t.fontSize = size;
  t.characters = chars;
  t.fills = [solid(fill)];
  t.textAutoResize = ar === 'H' ? 'HEIGHT' : 'WIDTH_AND_HEIGHT';
  return t;
}

// ---- spec factories (the recorded structure) ----
const T = (chars, o = {}) => ({ k: 'T', chars, st: o.st || 'Regular', s: o.s || 12, fill: o.fill || 'color/text', ar: o.ar || 'W', sz: o.sz || (o.ar === 'H' ? ['F', 'H'] : ['H', 'H']) });
const F = (n, o = {}, ch = []) => Object.assign({ k: 'F', n, ch }, o);
const header = (title, sub) => F('Header', { lm: 'V', pas: 'A', cas: 'F', gap: 2, sz: ['F', 'H'] }, [T(title, { st: 'Bold', s: 18 }), T(sub, { fill: 'color/text-muted' })]);
const card = (n, o, ch) => F(n, Object.assign({ lm: 'V', pas: 'A', cas: 'F', fill: 'color/surface', stroke: 'color/border', sw: 1, sz: ['F', 'H'] }, o), ch);
const cell = (chars, fill) => T(chars, { ar: 'H', fill: fill || 'color/text' });
const hcell = (chars) => cell(chars, 'color/text-muted');
const row = (cells, first) => F('Row', { lm: 'H', pas: 'F', cas: 'A', gap: 12, pad: [8, 0, 8, 0], padv: { t: 'space/2', b: 'space/2' }, sz: ['F', 'H'], stroke: first ? undefined : 'color/border', sides: first ? undefined : [1, 0, 0, 0] }, cells);
const tile = (label, value, sub) => ({ k: 'I', c: 'Stat tile', texts: [label, value, sub], sz: ['F', 'H'] });
const chip = (value) => ({ k: 'I', c: 'Delta chip', texts: [value], sz: ['H', 'H'] });
const shot = (chars) => F('shot', { lm: 'V', pas: 'F', cas: 'F', h: 90, pad: [12, 12, 12, 12], padv: 'space/3', cr: 'radius/sm', fill: 'color/bg', stroke: 'color/border', sw: 1, sz: ['F', 'X'] }, [T(chars, { s: 11, fill: 'color/text-subtle' })]);
const tag = (chars, color) => F('Tag', { lm: 'H', pas: 'A', cas: 'A', pad: [4, 8, 4, 8], padv: { t: 'space/1', b: 'space/1', l: 'space/2', r: 'space/2' }, cr: 'radius/sm', fill: 'color/surface', stroke: color, sw: 1, sz: ['H', 'H'] }, [T(chars, { st: 'Bold', s: 10, fill: color })]);
const feed = (kind, color, headline, sub, flag, first) => F('Item', { lm: 'H', pas: 'F', cas: 'A', gap: 12, pad: [12, 0, 12, 0], padv: { t: 'space/3', b: 'space/3' }, cai: 'CENTER', sz: ['F', 'H'], stroke: first ? undefined : 'color/border', sides: first ? undefined : [1, 0, 0, 0] },
  [tag(kind, color), F('Body', { lm: 'V', pas: 'A', cas: 'F', gap: 2, sz: ['F', 'H'] }, [T(headline, { s: 13, ar: 'H' }), T(sub, { s: 11, fill: 'color/text-muted', ar: 'H' })])].concat(flag ? [tag(flag, color)] : []));
const root = (name, x, y, w, ch) => F(name, { lm: 'V', pas: 'A', cas: 'F', w, x, y, gap: 16, pad: [32, 32, 32, 32], padv: 'space/8', fill: 'color/bg' }, ch);
const footer = (chars) => T(chars, { s: 11, fill: 'color/text-subtle', ar: 'H' });

const SCREENS = {
  'Screen 1': root('Screen 1 — Exec one-pager', 120, 700, 880, [
    header('Design System health report · August 2026', 'Owner: A. Rivera · Definitions ↗ · Data ↗ · Numbers as of 2026-09-01 06:00'),
    card('Headline', { lm: 'H', pas: 'F', cas: 'A', gap: 24, pad: [24, 24, 24, 24], padv: 'space/6', cai: 'CENTER', cr: 'radius/lg' }, [
      F('Left', { lm: 'V', pas: 'A', cas: 'A', gap: 6, sz: ['H', 'H'] }, [
        T('COVERAGE OF WHAT USERS SEE (M1)', { fill: 'color/text-muted' }),
        F('ValueRow', { lm: 'H', pas: 'A', cas: 'A', gap: 12, cai: 'CENTER', sz: ['H', 'H'] }, [T('68.3%', { st: 'Bold', s: 44 }), chip('▲ +2.1 pts')]),
        T('baseline 48.2% → now 68.3% → target 80% (Dec)', { s: 13, fill: 'color/text-muted' }),
      ]),
      F('Trend', { lm: 'V', pas: 'A', cas: 'F', gap: 4, cai: 'CENTER', sz: ['F', 'H'] }, [
        { k: 'V', d: 'M 0 64 L 60 54.15384615384616 L 120 39.38461538461539 L 180 27.07692307692308 L 240 12.307692307692308 L 300 0', stroke: 'color/accent', sw: 2.5 },
        T('six-period trend (28-day periods): Mar → Aug', { s: 11, fill: 'color/text-subtle' }),
      ]),
    ]),
    F('Scorecard', { lm: 'H', pas: 'F', cas: 'A', gap: 12, sz: ['F', 'H'] }, [
      tile('COST PER TEAM (M9)', '$41k', 'target ≤ $45k · owner FIN'),
      tile('OVERRIDE RATE (M2)', '8.1%', 'target ≤ 5% · owner JO'),
      tile('DEFECTS ON VS OFF (M5)', '0.4 / 1.9', 'per release · target ≤ 0.5 on'),
      tile('ENGAGEMENT (M6)', '88%', '3-mo avg 82.7 · target ≥ 80%'),
    ]),
    card('Proof', { gap: 10, pad: [24, 24, 24, 24], padv: 'space/6', cr: 'radius/lg' }, [
      T('PROOF · Dark theme rollout · 2026-06-03 to 2026-07-11', { fill: 'color/text-muted' }),
      F('ProofRow', { lm: 'H', pas: 'F', cas: 'A', gap: 16, sz: ['F', 'H'] }, [
        shot('BEFORE · Checkout · 2026-06-02'),
        shot('AFTER · Checkout · 2026-07-12'),
        F('numbers', { lm: 'V', pas: 'A', cas: 'F', gap: 4, sz: ['F', 'H'] }, [
          T('LAST TIME 1,140 h — source: 2024 theme timesheets', { fill: 'color/text-muted', ar: 'H' }),
          T('THIS TIME 190 h — source: DS-THEME tag, 4 repos', { fill: 'color/text-muted', ar: 'H' }),
          T('saved 810 to 950 h', { st: 'Bold', s: 20 }),
          T('≈ $69k to $81k at $85/h loaded · cost avoidance (M4b)', { fill: 'color/success', ar: 'H' }),
          T('“We changed 40 tokens and shipped in a sprint.” L. Pineda, Staff Eng', { fill: 'color/text-subtle', ar: 'H' }),
        ]),
      ]),
    ]),
    F('Columns', { lm: 'H', pas: 'F', cas: 'A', gap: 16, sz: ['F', 'H'] }, [
      card('WHAT WE ARE NOT COUNTING', { gap: 6, pad: [20, 20, 20, 20], padv: 'space/5', cr: 'radius/md' }, [
        T('WHAT WE ARE NOT COUNTING', { s: 11, fill: 'color/text-muted' }),
        T('· Onboarding time for 9 new engineers (no baseline yet)', { ar: 'H' }),
        T('· QA hours on system-built surfaces (tracking starts Q4)', { ar: 'H' }),
        T('· Brand-consistency effects on trust metrics', { ar: 'H' }),
      ]),
      card('RISK AND BREACHES', { gap: 6, pad: [20, 20, 20, 20], padv: 'space/5', cr: 'radius/md' }, [
        T('RISK AND BREACHES', { s: 11, fill: 'color/text-muted' }),
        T('Automated a11y pass rate on system surfaces: 96%, up 3 pts (not a conformance claim)', { ar: 'H' }),
        T('Key-person: 2 of 5 critical areas have no named backup', { fill: 'color/warning', ar: 'H' }),
        T('Breach (M1): Admin console coverage 58% to 41% over 28 days, since Aug 2 · owner S. Lindqvist · open in the feed', { fill: 'color/danger', ar: 'H' }),
      ]),
    ]),
    card('The decision', { gap: 6, pad: [20, 20, 20, 20], padv: 'space/5', cr: 'radius/md', stroke: 'color/accent', sw: 2 }, [
      T('THE DECISION', { s: 11, fill: 'color/text-muted' }),
      T('Hold current headcount through Q1; approve the Android coverage instrumentation (10 eng-days).', { st: 'Bold', s: 16, ar: 'H' }),
      T('If no: Android stays unmeasured; the 80% target applies to web only and the December read-out will say so.', { fill: 'color/text-muted', ar: 'H' }),
    ]),
    footer('Definitions: /design-system/metrics · Data: BI › Design System › Executive · Method notes attached · Screen 1 of 11'),
  ]),
  'Screen 2': root('Screen 2 — Team view', 1120, 700, 820, [
    header('Team view · coverage by consuming team', 'Sorted by coverage · 22 teams · breach flagged · Screen 2 of 11'),
    card('Table', { gap: 0, pad: [16, 16, 16, 16], padv: 'space/4', cr: 'radius/md' }, [
      row([hcell('TEAM'), hcell('COVERAGE'), hcell('OVERRIDE'), hcell('DEFECTS'), hcell('ENGAGEMENT'), hcell('OWNER')], true),
      row([cell('Checkout'), cell('90%'), cell('3.1%'), cell('0.2'), cell('88%'), cell('LP')]),
      row([cell('Storefront'), cell('85%'), cell('5.0%'), cell('0.3'), cell('82%'), cell('AR')]),
      row([cell('Mobile web'), cell('73%'), cell('6.4%'), cell('0.6'), cell('80%'), cell('MC')]),
      row([cell('Support'), cell('68%'), cell('7.2%'), cell('0.9'), cell('74%'), cell('DK')]),
      row([cell('Marketing'), cell('62%'), cell('11%'), cell('0.4'), cell('77%'), cell('JO')]),
      row([cell('Admin console'), cell('41% ▼', 'color/danger'), cell('9.1%'), cell('1.2'), cell('71%'), cell('SL')]),
    ]),
  ]),
  'Screen 6': root('Screen 6 — Event ledger', 2020, 700, 780, [
    header('Event ledger · hours before and after', 'Each row is a natural experiment instrumented in advance · Screen 6 of 11'),
    card('Table', { gap: 0, pad: [16, 16, 16, 16], padv: 'space/4', cr: 'radius/md' }, [
      row([hcell('EVENT'), hcell('LAST TIME'), hcell('THIS TIME'), hcell('SAVED'), hcell('METHOD')], true),
      row([cell('Dark theme rollout'), cell('1,140 h'), cell('190 h'), cell('810–950 h', 'color/success'), cell('DS-THEME tag')]),
      row([cell('Spacing overhaul'), cell('320 h'), cell('140 h'), cell('180 h', 'color/success'), cell('estimate + tickets')]),
      row([cell('A11y remediation'), cell('600 h'), cell('210 h'), cell('390 h', 'color/success'), cell('ticket delta')]),
      row([cell('Framework upgrade'), cell('—'), cell('—'), cell('instrument first', 'color/text-muted'), cell('open')]),
    ]),
    footer('Method: hours from timesheets and tagged commits · pessimistic to optimistic range · Screen 6 of 11'),
  ]),
  'Screen 7': root('Screen 7 — Leading feed', 2820, 700, 720, [
    header('Leading feed · what changed, what needs a decision', 'Engagement and events move before adoption does · Screen 7 of 11'),
    card('Feed', { gap: 0, pad: [16, 16, 16, 16], padv: 'space/4', cr: 'radius/md' }, [
      feed('BREACH', 'color/danger', 'Admin console coverage 58% to 41% over 28 days', 'Aug 2 · owner S. Lindqvist · since Aug 2', 'NEEDS DECISION', true),
      feed('CONTRIBUTION', 'color/success', 'Mobile web added 3 components to the system', 'Jul 28 · +2 contributors this month'),
      feed('PROOF', 'color/accent', 'Dark theme rollout closed: saved 810 to 950 h', 'Jul 20 · published to the ledger'),
      feed('DEFINITION', 'color/text-muted', 'M1 coverage v1 to v2: method change, labeled break', 'Jul 12 · two periods before the series resumes'),
      feed('SPONSOR', 'color/accent', 'Eng director attended release review', 'Jul 5 · 2 of the last 3 reviews'),
    ]),
  ]),
};

// ---- interpreter ----
async function build(spec, parent) {
  let node;
  if (spec.k === 'F') {
    node = figma.createFrame();
    node.name = spec.n || 'Frame';
    if (spec.lm) node.layoutMode = spec.lm === 'V' ? 'VERTICAL' : 'HORIZONTAL';
    if (spec.w || spec.h) node.resize(spec.w || node.width, spec.h || node.height);
    if (spec.lm) {
      node.primaryAxisSizingMode = spec.pas === 'A' ? 'AUTO' : 'FIXED';
      node.counterAxisSizingMode = spec.cas === 'A' ? 'AUTO' : 'FIXED';
      node.itemSpacing = spec.gap || 0;
      const p = spec.pad || [0, 0, 0, 0];
      node.paddingTop = p[0]; node.paddingRight = p[1]; node.paddingBottom = p[2]; node.paddingLeft = p[3];
      node.primaryAxisAlignItems = spec.pai || 'MIN';
      node.counterAxisAlignItems = spec.cai || 'MIN';
    }
    node.fills = spec.fill ? [solid(spec.fill)] : [];
    if (spec.stroke) {
      node.strokes = [solid(spec.stroke)];
      node.strokeAlign = 'INSIDE';
      if (spec.sides) { node.strokeTopWeight = spec.sides[0]; node.strokeRightWeight = spec.sides[1]; node.strokeBottomWeight = spec.sides[2]; node.strokeLeftWeight = spec.sides[3]; }
      else node.strokeWeight = spec.sw || 1;
    }
    if (spec.cr) { node.cornerRadius = numValue(spec.cr); bindRadius(node, spec.cr); }
    if (spec.padv) bindPad(node, spec.padv);
  } else if (spec.k === 'T') {
    node = await text(spec.chars, spec.st, spec.s, spec.fill, spec.ar);
  } else if (spec.k === 'V') {
    node = figma.createVector();
    node.name = 'Vector';
    node.vectorPaths = [{ windingRule: 'NONE', data: spec.d }];
    node.fills = [];
    node.strokes = [solid(spec.stroke)];
    node.strokeWeight = spec.sw;
    node.strokeAlign = 'CENTER';
  } else if (spec.k === 'I') {
    node = COMP[spec.c].createInstance();
    const ts = node.findAll((x) => x.type === 'TEXT');
    for (let i = 0; i < spec.texts.length && i < ts.length; i++) {
      for (const f of ts[i].getRangeAllFontNames(0, ts[i].characters.length)) await figma.loadFontAsync(f);
      ts[i].characters = spec.texts[i];
    }
  }
  if (parent) parent.appendChild(node); else page.appendChild(node);
  if (parent && parent.layoutMode !== 'NONE' && spec.sz) { node.layoutSizingHorizontal = SZ[spec.sz[0]]; node.layoutSizingVertical = SZ[spec.sz[1]]; }
  if (!parent) { node.x = spec.x; node.y = spec.y; }
  if (spec.ch) for (const c of spec.ch) await build(c, node);
  return node;
}

const created = {};
for (const name of BUILD) { const n = await build(SCREENS[name]); created[name] = n.id; }
return { createdNodeIds: Object.values(created), screens: created };
