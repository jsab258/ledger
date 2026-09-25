// Draft a FreeSewing pattern and write each part's seam outline as points, for Blender.
//
//     node tools/meshgen/freesewing_draft.mjs <node_modules dir> florent head=570 out.json
//
// WHY, 25 September. Jafar's ruling: clothes from FreeSewing's open patterns
// (MIT), sewn and draped in Blender. The first is the simplest garment, the
// Florent flat cap, which needs one measurement: head circumference, in mm.
// This drafts the pattern with FreeSewing's own code and writes, for every
// part, its seam line (no seam allowance: cloth is simulated edge to edge)
// sampled every 2 mm, its named paths sampled the same way (the edges that are
// sewn to other parts), and its named points (notches, fold ends), all in mm,
// y down as FreeSewing draws.
import { pathToFileURL } from 'node:url'
import path from 'node:path'
import fs from 'node:fs'

const [modules, design, ...rest] = process.argv.slice(2)
const out = rest.pop()
const measurements = Object.fromEntries(rest.map((kv) => kv.split('=')).map(([k, v]) => [k, Number(v)]))
const mod = await import(pathToFileURL(path.join(modules, '@freesewing', design, 'src', 'index.mjs')).href)
const Design = mod[design.charAt(0).toUpperCase() + design.slice(1)]
const pattern = new Design({ measurements, sa: 0 })
pattern.draft()

// Walks the path's own operations (move, line, cubic curve), a point every
// ~2 mm along each curve; walking by distance tripped on the zero-length line
// the brims end with.
function sample(p, step = 2) {
  const pts = []
  const r = (v) => Math.round(v * 100) / 100
  const push = (x, y) => {
    const last = pts[pts.length - 1]
    if (!last || Math.hypot(last[0] - x, last[1] - y) > 1e-6) pts.push([r(x), r(y)])
  }
  let cur = null, first = null
  for (const op of p.ops) {
    if (op.type === 'move') { cur = op.to; first = first || op.to; push(cur.x, cur.y) }
    else if (op.type === 'line') { push(op.to.x, op.to.y); cur = op.to }
    else if (op.type === 'curve') {
      const a = cur, b = op.cp1, c = op.cp2, d = op.to
      const est = Math.hypot(b.x - a.x, b.y - a.y) + Math.hypot(c.x - b.x, c.y - b.y) + Math.hypot(d.x - c.x, d.y - c.y)
      const n = Math.max(2, Math.ceil(est / step))
      for (let i = 1; i <= n; i++) {
        const t = i / n, u = 1 - t
        push(u * u * u * a.x + 3 * u * u * t * b.x + 3 * u * t * t * c.x + t * t * t * d.x,
             u * u * u * a.y + 3 * u * u * t * b.y + 3 * u * t * t * c.y + t * t * t * d.y)
      }
      cur = d
    }
  }
  let len = 0
  for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
  return { length: Math.round(len * 10) / 10, closed: p.ops.some((o) => o.type === 'close'), points: pts }
}

const result = { design, measurements, parts: {} }
for (const set of pattern.parts) {
  for (const [name, part] of Object.entries(set)) {
    if (part.hidden) continue
    const paths = {}
    for (const [pn, p] of Object.entries(part.paths)) {
      if (pn === 'sa' || pn.startsWith('__macro') || (p.attributes && p.attributes.get && String(p.attributes.get('class') || '').includes('help'))) continue
      try { paths[pn] = sample(p) } catch (e) { console.error(`freesewing_draft: ${name}.${pn} not walked: ${e.message}`) }
    }
    const points = Object.fromEntries(Object.entries(part.points).map(([k, v]) => [k, [Math.round(v.x * 100) / 100, Math.round(v.y * 100) / 100]]))
    result.parts[name] = { paths, points }
  }
}
fs.writeFileSync(out, JSON.stringify(result, null, 1))
console.log(`freesewing_draft: ${design} ${JSON.stringify(measurements)} -> ${Object.keys(result.parts).length} parts: ` +
  Object.entries(result.parts).map(([n, p]) => `${n} (${Object.keys(p.paths).join('/')})`).join(', '))
