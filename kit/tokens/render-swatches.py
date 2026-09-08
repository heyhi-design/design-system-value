#!/usr/bin/env python3
"""Render swatches.html from neutral.tokens.json (light + dark, in context).

Reads the token source and emits a self-contained HTML swatch sheet: the
primitive ramps, the semantic roles as labelled chips, and a mini metric tile
in both modes, so the neutral palette can be eyeballed before it drives Figma
variables. Regenerate after any token edit. Stdlib only.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
data = json.loads((HERE / "neutral.tokens.json").read_text())
prim = data["primitive"]
sem = data["semantic"]["color"]


def hx(ref):
    if isinstance(ref, str) and ref.startswith("{"):
        node = {"primitive": prim}
        for p in ref[1:-1].split("."):
            node = node[p]
        return node["$value"]
    return ref


def s(role, mode):
    return hx(sem[role]["$extensions"]["mode"][mode])


RAMPS = ["gray", "accent", "green", "amber", "red"]
ROLES = ["bg", "surface", "surface-raised", "text", "text-muted", "text-subtle",
         "border", "border-strong", "border-interactive", "accent",
         "accent-hover", "on-accent", "focus", "success", "warning", "danger"]


def ramp_html(name):
    steps = prim[name]
    cells = "".join(
        f'<div style="flex:1;height:40px;background:{v["$value"]}"></div>'
        for k, v in steps.items())
    return f'<div class="ramp"><div class="lbl">{name}</div><div class="row">{cells}</div></div>'


def panel(mode):
    bg, surf, surf2 = s("bg", mode), s("surface", mode), s("surface-raised", mode)
    text, muted, subtle = s("text", mode), s("text-muted", mode), s("text-subtle", mode)
    acc, onacc, border = s("accent", mode), s("on-accent", mode), s("border", mode)
    borderi, focus = s("border-interactive", mode), s("focus", mode)
    succ, warn, dang = s("success", mode), s("warning", mode), s("danger", mode)
    chips = "".join(
        f'<div class="chip" style="background:{surf};border:1px solid {border}">'
        f'<span class="sw" style="background:{s(r, mode)}"></span>'
        f'<code style="color:{text}">{r}</code>'
        f'<code style="color:{muted}">{s(r, mode)}</code></div>'
        for r in ROLES)
    tile = f'''
      <div style="background:{surf};border:1px solid {border};border-radius:12px;padding:20px;max-width:320px">
        <div style="color:{muted};font-size:12px;text-transform:uppercase;letter-spacing:.04em">Coverage of what users see</div>
        <div style="display:flex;align-items:baseline;gap:10px;margin-top:6px">
          <div style="color:{text};font-size:40px;font-weight:700">68.3%</div>
          <div style="color:{succ};font-size:13px;font-weight:600">&#9650; +2.1 pts</div>
        </div>
        <div style="color:{muted};font-size:13px;margin-top:4px">baseline 48.2% &rarr; now 68.3% &rarr; target 80%</div>
        <div style="display:flex;gap:8px;margin-top:16px">
          <button style="background:{acc};color:{onacc};border:none;border-radius:8px;padding:8px 14px;font-weight:600">View detail</button>
          <button style="background:transparent;color:{acc};border:1px solid {borderi};border-radius:8px;padding:8px 14px">Filter</button>
        </div>
        <div style="margin-top:12px;color:{dang};font-size:12px">&#9660; Admin console breached (M1)</div>
      </div>'''
    return f'''<section style="background:{bg};padding:24px;border-radius:12px">
      <h2 style="color:{text};margin:0 0 16px;font-size:16px">{mode} mode</h2>
      <div class="chips">{chips}</div>
      <div style="margin-top:20px">{tile}</div>
    </section>'''


html = f'''<!doctype html><meta charset="utf-8">
<title>Neutral tokens: swatch sheet</title>
<style>
  body{{font:14px/1.4 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:24px;background:#e2e8f0;color:#0f172a}}
  h1{{font-size:18px;margin:0 0 4px}} .meta{{color:#475569;margin:0 0 20px;font-size:13px}}
  .ramps{{margin:0 0 24px}} .ramp{{margin:6px 0}} .ramp .lbl{{font-size:12px;color:#475569;margin-bottom:2px}}
  .ramp .row{{display:flex;border-radius:6px;overflow:hidden;border:1px solid #cbd5e1}}
  .panels{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
  @media(max-width:760px){{.panels{{grid-template-columns:1fr}}}}
  .chips{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
  .chip{{display:flex;align-items:center;gap:8px;border-radius:8px;padding:6px 8px;font-size:12px}}
  .chip .sw{{width:20px;height:20px;border-radius:4px;flex:0 0 auto;box-shadow:0 0 0 1px rgba(0,0,0,.1)}}
  .chip code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
</style>
<h1>Neutral tokens &mdash; swatch sheet</h1>
<p class="meta">Generated from neutral.tokens.json by render-swatches.py. Every text-on-surface pair is WCAG-gated in contrast-report.md (32/32 pass). No brand mode; swap the primitive ramps to rebrand.</p>
<div class="ramps">{"".join(ramp_html(r) for r in RAMPS)}</div>
<div class="panels">{panel("light")}{panel("dark")}</div>
'''

(HERE / "swatches.html").write_text(html)
print("wrote", (HERE / "swatches.html").name, f"({len(html)} bytes)")
