// build-components.js — recorded from the reference template. Creates the two components the
// value-surface screens instance: "Delta chip" and "Stat tile". Every fill, stroke, padding, and
// radius is bound to a variable by NAME (run build-variables.js first). Text uses Inter.
// Run inside the design tool's script runner (use_figma, figma-use skill loaded first).
// Idempotent enough for a fresh page: it refuses to run if either component already exists.

const collections = await figma.variables.getLocalVariableCollectionsAsync();
const wanted = new Set(collections.filter((c) => c.name === 'Primitives' || c.name === 'Semantic').map((c) => c.id));
if (wanted.size !== 2) throw new Error('expected collections named Primitives and Semantic (run build-variables.js first)');
const V = {};
for (const v of await figma.variables.getLocalVariablesAsync()) if (wanted.has(v.variableCollectionId)) V[v.name] = v;
const need = (n) => { if (!V[n]) throw new Error('variable missing: ' + n + ' (run build-variables.js first)'); return V[n]; };
const solid = (n) => figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: { r: 0, g: 0, b: 0 } }, 'color', need(n));
const bindNum = (node, field, n) => node.setBoundVariable(field, need(n));
const bindRadius = (node, n) => ['topLeftRadius', 'topRightRadius', 'bottomLeftRadius', 'bottomRightRadius'].forEach((f) => bindNum(node, f, n));
async function text(chars, style, size, fill, autoResize) {
  await figma.loadFontAsync({ family: 'Inter', style });
  const t = figma.createText();
  t.fontName = { family: 'Inter', style };
  t.fontSize = size;
  t.characters = chars;
  t.fills = [solid(fill)];
  t.textAutoResize = autoResize || 'WIDTH_AND_HEIGHT';
  return t;
}

const page = figma.currentPage;
for (const c of page.findAllWithCriteria({ types: ['COMPONENT'] })) {
  if (c.name === 'Delta chip' || c.name === 'Stat tile') throw new Error('component already exists on this page: ' + c.name + ' (' + c.id + ')');
}
let right = 0;
for (const c of page.children) right = Math.max(right, c.x + c.width);
const X = page.children.length ? right + 200 : 100;

// Delta chip: a signed change with an arrow. One TEXT (value) at index 0.
const chip = figma.createComponent();
chip.name = 'Delta chip';
chip.layoutMode = 'HORIZONTAL';
chip.primaryAxisSizingMode = 'AUTO';
chip.counterAxisSizingMode = 'AUTO';
chip.itemSpacing = 4;
chip.counterAxisAlignItems = 'CENTER';
chip.paddingTop = 4; chip.paddingBottom = 4; chip.paddingLeft = 8; chip.paddingRight = 8;
chip.cornerRadius = 4;
chip.fills = [solid('color/surface')];
chip.strokes = [solid('color/border')];
chip.strokeWeight = 1;
chip.strokeAlign = 'INSIDE';
bindNum(chip, 'paddingTop', 'space/1'); bindNum(chip, 'paddingBottom', 'space/1');
bindNum(chip, 'paddingLeft', 'space/2'); bindNum(chip, 'paddingRight', 'space/2');
bindRadius(chip, 'radius/sm');
page.appendChild(chip);
chip.x = X; chip.y = 120;
chip.appendChild(await text('▲ +2.1 pts', 'Bold', 12, 'color/success'));
chip.description = 'Delta chip: a signed change with an arrow. One TEXT node (value), text index 0. Fill color/surface, stroke color/border, value text color/success (swap to color/danger for a fall).';

// Stat tile: label, value, sparkline, sub. Three TEXT nodes in document order: label (0), value (1), sub (2).
const tile = figma.createComponent();
tile.name = 'Stat tile';
tile.layoutMode = 'VERTICAL';
tile.resize(230, 123);
tile.primaryAxisSizingMode = 'AUTO';
tile.counterAxisSizingMode = 'FIXED';
tile.itemSpacing = 6;
tile.paddingTop = 16; tile.paddingBottom = 16; tile.paddingLeft = 16; tile.paddingRight = 16;
tile.cornerRadius = 8;
tile.fills = [solid('color/surface')];
tile.strokes = [solid('color/border')];
tile.strokeWeight = 1;
tile.strokeAlign = 'INSIDE';
['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'].forEach((f) => bindNum(tile, f, 'space/4'));
bindRadius(tile, 'radius/md');
page.appendChild(tile);
tile.x = X; tile.y = 200;
const label = await text('COST PER TEAM (M9)', 'Regular', 11, 'color/text-muted', 'HEIGHT');
tile.appendChild(label); label.layoutSizingHorizontal = 'FILL';
const value = await text('$41k', 'Bold', 22, 'color/text');
tile.appendChild(value);
const spark = figma.createVector();
spark.name = 'Vector';
spark.vectorPaths = [{ windingRule: 'NONE', data: 'M 0 20 L 30 14.666666666666666 L 60 16 L 90 6.666666666666666 L 120 9.333333333333332 L 150 0' }];
spark.fills = [];
spark.strokes = [solid('color/accent')];
spark.strokeWeight = 2;
spark.strokeAlign = 'CENTER';
tile.appendChild(spark);
const sub = await text('target ≤ $45k · owner FIN', 'Regular', 11, 'color/text-subtle', 'HEIGHT');
tile.appendChild(sub); sub.layoutSizingHorizontal = 'FILL';
tile.description = 'Stat tile: label, value, sparkline, sub. Three TEXT nodes in document order: label (index 0), value (index 1), sub (index 2); the sparkline vector between value and sub is not text. Fill color/surface, stroke color/border, sparkline stroke color/accent.';

return { createdNodeIds: [chip.id, tile.id], components: { 'Delta chip': chip.id, 'Stat tile': tile.id } };
