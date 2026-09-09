// census-walk.js — read-only. Walks each value-surface screen in document order and returns the
// ordered list of text nodes and component instances that ../collectors/census_from_walk.py joins
// with the binding contract to produce screen-census.json for THIS file. Run inside the design
// tool's script runner (use_figma, figma-use skill loaded first) on the target file, save the
// returned JSON as walk.json (outside the repository, or in kit/figma/ where it is ignored), then:
//   python3 ../collectors/census_from_walk.py walk.json --out ../collectors/screen-census.json
// Screens are found by frame name on the current page: the name is the key or the key followed by
// a space (so "Screen 1" never matches "Screen 10"). Instances are identified by their main
// component's name, so a renamed instance still censuses correctly.

const SCREENS = { screen_1: 'Screen 1', screen_2: 'Screen 2', screen_6: 'Screen 6', screen_7: 'Screen 7' };
const isScreen = (name, key) => name === key || name.startsWith(key + ' ');
const page = figma.currentPage;
const out = { components: {}, screens: {} };
for (const c of page.findAllWithCriteria({ types: ['COMPONENT'] })) {
  if (c.name === 'Stat tile' || c.name === 'Delta chip') out.components[c.name] = { id: c.id, text_node_ids: c.findAll((x) => x.type === 'TEXT').map((x) => x.id) };
}
async function walk(n, items) {
  if (n.type === 'INSTANCE') {
    const main = await n.getMainComponentAsync();
    items.push({ kind: 'instance', id: n.id, component: main ? main.name : n.name, texts: n.findAll((x) => x.type === 'TEXT').map((x) => x.characters) });
    return;
  }
  if (n.type === 'TEXT') { items.push({ kind: 'text', id: n.id, text: n.characters }); return; }
  if ('children' in n) for (const c of n.children) await walk(c, items);
}
for (const key of Object.keys(SCREENS)) {
  const frame = page.children.find((n) => n.type === 'FRAME' && isScreen(n.name, SCREENS[key]));
  if (!frame) { out.screens[key] = null; continue; }
  const items = [];
  await walk(frame, items);
  out.screens[key] = { frame: frame.id, name: frame.name, items };
}
return out;
