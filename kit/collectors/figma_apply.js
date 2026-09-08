// Reference apply script for the populate-from-data generator (design-tool step).
//
// Run this inside the design tool's script runner (the Figma Plugin API, via the
// use_figma tool with the figma-use skill loaded first). It is the third step of
// the runbook: collect -> resolve -> APPLY. It writes text only. It never touches
// fills, strokes, or variable bindings, so a target file's theming and its
// zero-raw-literals guarantee are preserved by construction.
//
// USAGE
//   1. Resolve a payload into apply ops:
//        python3 populate_screens.py --data <payload>.json --apply-plan --out apply-plan.json
//      apply-plan.json.ops is a list of:
//        { "type": "text",       "node": "<id>",     "value": "<string>", "slot": "<id>" }
//        { "type": "tile"|"chip","instance": "<id>", "role": "label|value|sub", "value": "...", "slot": "..." }
//   2. Paste that ops list into `const ops = [...]` below.
//   3. Call use_figma with the target file key (the design system's own Figma
//      file), this code, and skillNames "figma-use". Do NOT hardcode a file key
//      in this script: it is a parameter of the tool call.
//
// The role->index map mirrors screen-census.json components.*.text_nodes_in_order:
// a Stat tile exposes [label, value, sub]; a Delta chip exposes [value]. So a
// chip's "value" is text index 0, while a tile's "value" is index 1. Keep this
// map in sync with the census if the component internals change.

const ops = [
  // PASTE apply-plan.json "ops" here.
];

const ROLE_ORDER = { tile: ["label", "value", "sub"], chip: ["value"] };

async function setText(node, value) {
  if (!node) throw new Error("missing node");
  if (node.type !== "TEXT") throw new Error("not TEXT: " + node.id + " " + node.type);
  const len = node.characters.length;
  const fonts = len > 0 ? node.getRangeAllFontNames(0, len) : [node.fontName];
  for (const f of fonts) { await figma.loadFontAsync(f); }
  node.characters = value;
}

const mutated = [], errors = [];
for (const op of ops) {
  try {
    if (op.type === "text") {
      const n = await figma.getNodeByIdAsync(op.node);
      await setText(n, op.value);
      mutated.push(op.node);
    } else {
      const order = ROLE_ORDER[op.type];
      if (!order) throw new Error("unknown op type " + op.type);
      const idx = order.indexOf(op.role);
      if (idx < 0) throw new Error("role " + op.role + " not in " + op.type + " order");
      const inst = await figma.getNodeByIdAsync(op.instance);
      if (!inst) throw new Error("missing instance " + op.instance);
      const texts = inst.findAllWithCriteria({ types: ["TEXT"] });
      const t = texts[idx];
      if (!t) throw new Error("no TEXT at index " + idx + " in " + op.instance);
      await setText(t, op.value);
      mutated.push(t.id);
    }
  } catch (e) {
    errors.push((op.slot || "?") + ": " + e.message);
  }
}
return { ops: ops.length, mutated: mutated.length, errors };
