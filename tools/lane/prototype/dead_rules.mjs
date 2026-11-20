#!/usr/bin/env node
// DEAD RULES: what the prototype holds that the game never uses (the depth check of 13:16, 20 Nov 2026).
// A machine check, read only. It lists:
//   1. every function a rule piece exports (src/game/pieces/*.js, PIECE.fns) that game code never calls;
//   2. every field a piece function returns that no caller reads, where it can tell;
//   3. every emit('name') with no on('name') listener;
//   4. every saved field of a system (its fresh() state under G.x) that is written and never read by the game
//      (read only by the test hook counts as never read);
//   5. every function in src/game whose only effect is a line in G.log (never shown to the player) or a line in
//      the Ledger, where it can tell: nothing said, no scene, no act, no money, no state changed, nothing emitted;
//   6. every function a system file exports that nothing in the game calls (a test hook at most).
// Usage: node tools/lane/prototype/dead_rules.mjs [--out FILE.md] [--json]
// It prints the count on its last line as "DEAD RULES: N". The aim is zero. Exit code 0 (it is a count, not a gate)
// unless --max N is given and the count is over it.
import fs from 'fs';
import path from 'path';
import url from 'url';
import { createRequire } from 'module';
const HERE = path.dirname(url.fileURLToPath(import.meta.url));
const PROJ = path.join(HERE, 'project');
const require = createRequire(path.join(PROJ, 'package.json'));
const acorn = require('acorn');
const SRC = path.join(PROJ, 'src');
const args = process.argv.slice(2);
const argOf = (n) => (args.includes(n) ? args[args.indexOf(n) + 1] : null);

// ---------- read and parse ----------
const files = [];
(function walkDir(d) {
  for (const f of fs.readdirSync(d).sort()) {
    const p = path.join(d, f);
    if (fs.statSync(p).isDirectory()) {
      if (f !== 'sim' && f !== 'render') walkDir(p);
    } else if (f.endsWith('.js')) files.push(p);
  }
})(SRC);
const rel = (p) => path.relative(SRC, p).replace(/\\/g, '/');
const isPiece = (p) => rel(p).startsWith('game/pieces/');
const parsed = {};
for (const p of files) {
  const text = fs.readFileSync(p, 'utf8');
  const ast = acorn.parse(text, { ecmaVersion: 'latest', sourceType: 'module', locations: true });
  link(ast, null);
  parsed[p] = { text, ast };
}
function kids(n) {
  const out = [];
  for (const k of Object.keys(n)) {
    if (k === 'parent' || k === 'loc') continue;
    const v = n[k];
    if (Array.isArray(v)) for (const c of v) c && typeof c.type === 'string' && out.push(c);
    else if (v && typeof v.type === 'string') out.push(v);
  }
  return out;
}
function link(n, parent) {
  n.parent = parent;
  for (const c of kids(n)) link(c, n);
}
function walk(n, fn) {
  fn(n);
  for (const c of kids(n)) walk(c, fn);
}
const isFn = (n) => n && (n.type === 'FunctionDeclaration' || n.type === 'FunctionExpression' || n.type === 'ArrowFunctionExpression');
const fnOf = (n) => {
  let p = n.parent;
  while (p && !isFn(p)) p = p.parent;
  return p;
};
const propName = (m) => (m.type === 'MemberExpression' && !m.computed && m.property.type === 'Identifier' ? m.property.name : m.type === 'MemberExpression' && m.computed && m.property.type === 'Literal' ? String(m.property.value) : null);
const inHook = (n) => {
  for (let p = n; p; p = p.parent) if (p.type === 'Property' && !p.computed && (p.key.name === 'hook' || p.key.value === 'hook')) return true;
  return false;
};
const line = (p, n) => rel(p) + ':' + n.loc.start.line;

// ---------- 1 and 2: pieces ----------
// What each piece function returns (top-level keys of the object literals it can return), where it can tell.
const pieces = {}; // name -> { file, fns: { fn: { keys:Set|null, node } } }
for (const p of files.filter(isPiece)) {
  const { ast } = parsed[p];
  const decl = {};
  for (const s of ast.body) {
    if (s.type === 'FunctionDeclaration') decl[s.id.name] = s;
    if (s.type === 'VariableDeclaration') for (const d of s.declarations) if (d.id.type === 'Identifier' && d.init) decl[d.id.name] = d.init;
  }
  const name = path.basename(p, '.js');
  const fns = {};
  walk(ast, (n) => {
    if (n.type === 'Property' && !n.computed && (n.key.name === 'fns' || n.key.value === 'fns') && n.value.type === 'ObjectExpression')
      for (const q of n.value.properties) {
        if (q.type !== 'Property') continue;
        const fname = q.key.name || q.key.value;
        const body = q.value.type === 'Identifier' ? decl[q.value.name] : q.value;
        fns[fname] = { keys: returnKeys(body, decl), node: q };
      }
  });
  pieces[name] = { file: p, fns };
}
function returnKeys(f, decl) {
  if (!isFn(f)) return null;
  const keys = new Set();
  let opaque = false;
  const locals = {};
  walk(f.body, (n) => {
    if (n.type === 'VariableDeclarator' && n.id.type === 'Identifier' && n.init && fnOf(n) === f) locals[n.id.name] = n.init;
  });
  const seen = new Set();
  const take = (e) => {
    if (!e) return;
    if (e.type === 'ObjectExpression') {
      for (const q of e.properties) {
        if (q.type === 'Property' && !q.computed) keys.add(q.key.name || String(q.key.value));
        else opaque = true; // a spread: it cannot tell
      }
    } else if (e.type === 'ConditionalExpression') (take(e.consequent), take(e.alternate));
    else if (e.type === 'LogicalExpression') (take(e.left), take(e.right));
    else if (e.type === 'CallExpression' && e.callee.type === 'MemberExpression' && e.callee.object.name === 'Object' && e.callee.property.name === 'assign') e.arguments.forEach(take);
    else if (e.type === 'Identifier' && locals[e.name] && !seen.has(e.name)) (seen.add(e.name), take(locals[e.name]));
    else if (e.type === 'Identifier' || e.type === 'Literal' || e.type === 'TemplateLiteral' || e.type === 'UnaryExpression' || e.type === 'BinaryExpression' || e.type === 'ArrayExpression' || e.type === 'MemberExpression');
    else opaque = true;
  };
  if (f.body.type !== 'BlockStatement') take(f.body);
  else
    walk(f.body, (n) => {
      if (n.type === 'ReturnStatement' && fnOf(n) === f) take(n.argument);
    });
  return opaque && !keys.size ? null : keys;
}
// Call sites in game code.
const calls = {}; // 'piece.fn' -> [{ file, node, reads:Set, whole:bool, thrown:bool }]
const storedUnder = {}; // 'piece.fn' -> Set of property names the result was stored under
for (const p of files.filter((f) => !isPiece(f))) {
  const { ast } = parsed[p];
  const alias = {}; // identifier -> piece name (PIECE as X)
  const fnsAlias = {}; // identifier -> piece name (const L = X.fns)
  const direct = {}; // identifier -> 'piece.fn' (const { a } = X.fns)
  for (const s of ast.body)
    if (s.type === 'ImportDeclaration' && /pieces\/(\w+)\.js$/.test(s.source.value)) {
      const pn = s.source.value.match(/pieces\/(\w+)\.js$/)[1];
      for (const sp of s.specifiers) if (sp.imported && sp.imported.name === 'PIECE') alias[sp.local.name] = pn;
    }
  if (!Object.keys(alias).length) continue;
  walk(ast, (n) => {
    if (n.type === 'VariableDeclarator' && n.init && n.init.type === 'MemberExpression' && propName(n.init) === 'fns' && alias[n.init.object.name]) {
      if (n.id.type === 'Identifier') fnsAlias[n.id.name] = alias[n.init.object.name];
      if (n.id.type === 'ObjectPattern') for (const q of n.id.properties) if (q.type === 'Property') direct[q.value.name] = alias[n.init.object.name] + '.' + (q.key.name || q.key.value);
    }
  });
  const which = (c) => {
    // the piece function a callee names, or null
    if (c.type === 'Identifier') return direct[c.name] || null;
    if (c.type !== 'MemberExpression') return null;
    const f = propName(c);
    if (!f) return null;
    if (c.object.type === 'Identifier' && fnsAlias[c.object.name]) return fnsAlias[c.object.name] + '.' + f;
    if (c.object.type === 'MemberExpression' && propName(c.object) === 'fns' && alias[c.object.object.name]) return alias[c.object.object.name] + '.' + f;
    return null;
  };
  walk(ast, (n) => {
    // a mention that is not a call (handed on as a value) counts as a call it cannot follow
    const key = n.type === 'CallExpression' ? which(n.callee) : null;
    if (n.type === 'MemberExpression' && !(n.parent.type === 'CallExpression' && n.parent.callee === n)) {
      const k2 = which(n);
      if (k2 && pieces[k2.split('.')[0]].fns[k2.split('.')[1]]) (calls[k2] = calls[k2] || []).push({ file: p, node: n, reads: new Set(), whole: true });
    }
    if (!key) return;
    const site = { file: p, node: n, reads: new Set(), whole: false, thrown: false };
    (calls[key] = calls[key] || []).push(site);
    let e = n,
      par = n.parent;
    // through brackets that keep the value: (a || b), a ? b : c on the value side, await
    while (par && ((par.type === 'LogicalExpression' && par.right === e) || (par.type === 'ConditionalExpression' && par.test !== e) || par.type === 'AwaitExpression' || par.type === 'ParenthesizedExpression')) (e = par), (par = par.parent);
    if (par.type === 'MemberExpression' && par.object === e) {
      const f = propName(par);
      if (f) site.reads.add(f);
      else site.whole = true;
    } else if (par.type === 'VariableDeclarator' && par.init === e && par.id.type === 'Identifier') readsOfVar(par.id.name, fnOf(par) || ast, par, site);
    else if (par.type === 'VariableDeclarator' && par.id.type === 'ObjectPattern') {
      for (const q of par.id.properties) q.type === 'Property' ? site.reads.add(q.key.name || q.key.value) : (site.whole = true);
    } else if (par.type === 'AssignmentExpression' && par.right === e && par.left.type === 'MemberExpression' && propName(par.left)) {
      (storedUnder[key] = storedUnder[key] || new Set()).add(propName(par.left));
    } else if (par.type === 'AssignmentExpression' && par.right === e && par.left.type === 'Identifier') readsOfVar(par.left.name, fnOf(par) || ast, par, site);
    else if (par.type === 'ExpressionStatement') site.thrown = true;
    else if ((par.type === 'IfStatement' && par.test === e) || (par.type === 'UnaryExpression' && par.operator === '!') || (par.type === 'ConditionalExpression' && par.test === e) || (par.type === 'LogicalExpression' && par.left === e)) site.truth = true; // only whether it came back at all
    else site.whole = true;
  });
}
function readsOfVar(name, scope, declNode, site) {
  walk(scope, (m) => {
    if (m.type !== 'Identifier' || m.name !== name) return;
    const par = m.parent;
    if (par === declNode || (par.type === 'VariableDeclarator' && par.id === m)) return;
    if (par.type === 'AssignmentExpression' && par.left === m) return;
    if (par.type === 'MemberExpression' && par.object === m) {
      const f = propName(par);
      if (f) site.reads.add(f);
      else site.whole = true;
    } else if (par.type === 'MemberExpression' && par.property === m && !par.computed) return;
    else if (par.type === 'Property' && par.key === m && !par.computed && par.value !== m) return;
    else if ((par.type === 'IfStatement' && par.test === m) || (par.type === 'UnaryExpression' && par.operator === '!') || (par.type === 'LogicalExpression' && par.left === m) || (par.type === 'ConditionalExpression' && par.test === m)) return;
    else site.whole = true;
  });
}
// every `.<stored>.<field>` read anywhere, for results kept in state
const chained = {}; // prop -> Set of fields read off it
for (const p of files.filter((f) => !isPiece(f)))
  walk(parsed[p].ast, (n) => {
    if (n.type === 'MemberExpression' && n.object.type === 'MemberExpression') {
      const a = propName(n.object),
        b = propName(n);
      if (a && b) (chained[a] = chained[a] || new Set()).add(b);
    }
  });
// a stored result that is also read through a local (const f = x.ellis; f.stage): any `.field` read off a variable set from `.stored`
const viaLocal = {};
for (const p of files.filter((f) => !isPiece(f)))
  walk(parsed[p].ast, (n) => {
    if (n.type === 'VariableDeclarator' && n.id.type === 'Identifier' && n.init && n.init.type === 'MemberExpression' && propName(n.init)) {
      const site = { reads: new Set(), whole: false };
      readsOfVar(n.id.name, fnOf(n) || parsed[p].ast, n, site);
      const a = propName(n.init);
      viaLocal[a] = viaLocal[a] || { reads: new Set(), whole: false };
      site.reads.forEach((r) => viaLocal[a].reads.add(r));
      if (site.whole) viaLocal[a].whole = true;
    }
  });

// a rule used inside another rule of its piece is alive when that other rule is (showFor inside climb)
const usedInside = {}; // 'piece.fn' -> Set of 'piece.fn' whose bodies name it
for (const [pn, P] of Object.entries(pieces)) {
  const { ast } = parsed[P.file];
  const tops = {};
  for (const st of ast.body) {
    if (st.type === 'FunctionDeclaration') tops[st.id.name] = st;
    if (st.type === 'VariableDeclaration') for (const d of st.declarations) if (d.id.type === 'Identifier' && d.init) tops[d.id.name] = d.init;
  }
  for (const [outer, node] of Object.entries(tops))
    walk(node, (n) => {
      if (n.type === 'Identifier' && n.name !== outer && P.fns[n.name] && tops[n.name] && !(n.parent.type === 'MemberExpression' && n.parent.property === n && !n.parent.computed) && !(n.parent.type === 'Property' && n.parent.key === n)) (usedInside[pn + '.' + n.name] = usedInside[pn + '.' + n.name] || new Set()).add(pn + '.' + outer);
    });
}
const aliveInside = (key, seen = new Set()) => [...(usedInside[key] || [])].some((o) => !seen.has(o) && ((calls[o] || []).length || aliveInside(o, seen.add(o))));
const out = { deadFns: [], ignored: [], unheard: [], writeOnly: [], logOnly: [], deadExports: [] };
for (const [pn, P] of Object.entries(pieces))
  for (const [fn, F] of Object.entries(P.fns)) {
    const key = pn + '.' + fn,
      sites = calls[key] || [];
    if (!sites.length && aliveInside(key)) continue;
    if (!sites.length) {
      out.deadFns.push({ id: key, where: line(P.file, F.node), why: 'never called from game code' });
      continue;
    }
    if (sites.every((s) => s.thrown)) {
      out.ignored.push({ id: key + ' (all of it)', where: sites.map((s) => line(s.file, s.node)).join(', '), why: 'called and its result thrown away' });
      continue;
    }
    if (!F.keys || !F.keys.size) continue;
    if (sites.some((s) => s.whole)) continue; // handed on whole somewhere: it cannot tell
    const read = new Set();
    sites.forEach((s) => s.reads.forEach((r) => read.add(r)));
    let storedWhole = false;
    for (const st of storedUnder[key] || []) {
      (chained[st] || new Set()).forEach((r) => read.add(r));
      if (viaLocal[st]) (viaLocal[st].reads.forEach((r) => read.add(r)), (storedWhole = storedWhole || viaLocal[st].whole));
    }
    if (storedWhole) continue;
    const un = [...F.keys].filter((k) => !read.has(k));
    for (const k of un) out.ignored.push({ id: key + ' -> ' + k, where: sites.map((s) => line(s.file, s.node)).join(', '), why: 'returned, and no caller reads it' });
  }

// ---------- 3: events nobody listens for ----------
const emitted = {},
  heard = new Set();
for (const p of files) {
  const t = parsed[p].text;
  walk(parsed[p].ast, (n) => {
    if (n.type !== 'CallExpression' || !n.arguments.length) return;
    const c = n.callee;
    const nm = c.type === 'Identifier' ? c.name : c.type === 'MemberExpression' ? propName(c) : null;
    const a = n.arguments[0];
    if (nm === 'emit' && a.type === 'Literal' && typeof a.value === 'string') (emitted[a.value] = emitted[a.value] || []).push(line(p, n));
    if (nm === 'emit' && a.type !== 'Literal' && !(rel(p) === 'game/core.js')) (emitted['(a name worked out at ' + line(p, n) + ')'] = []).push(line(p, n));
    if (nm === 'on' && a.type === 'Literal' && typeof a.value === 'string') heard.add(a.value);
  });
  void t;
}
for (const [name, where] of Object.entries(emitted)) if (!name.startsWith('(') && !heard.has(name)) out.unheard.push({ id: "emit('" + name + "')", where: where.join(', '), why: 'nothing listens for it' });

// ---------- 4: saved fields written and never read ----------
// A system's saved state is what its fresh() returns. A field is read when some member expression `.field` is read
// anywhere in the game outside a system's test hook. Writes: assignment, ++, push/unshift/splice/length=, and the
// prune `a.f = a.f.filter(...)`.
const freshKeys = []; // { sys, key, where }
for (const p of files.filter((f) => rel(f).startsWith('game/') && !isPiece(f)))
  walk(parsed[p].ast, (n) => {
    if (n.type === 'Property' && !n.computed && (n.key.name === 'fresh') && isFn(n.value)) {
      const f = n.value;
      const take = (e) => e && e.type === 'ObjectExpression' && e.properties.forEach((q) => q.type === 'Property' && !q.computed && freshKeys.push({ sys: path.basename(p, '.js'), key: q.key.name || String(q.key.value), where: line(p, q) }));
      if (f.body.type !== 'BlockStatement') take(f.body);
      else walk(f.body, (m) => m.type === 'ReturnStatement' && fnOf(m) === f && take(m.argument));
    }
  });
// fields added later onto a system's state: x.<new> = ... where x = X('id') (first write seen in the system's own file)
for (const p of files.filter((f) => rel(f).startsWith('game/') && !isPiece(f))) {
  const sys = path.basename(p, '.js');
  walk(parsed[p].ast, (n) => {
    if (n.type === 'AssignmentExpression' && n.left.type === 'MemberExpression' && propName(n.left)) {
      const o = n.left.object;
      const isX = (o.type === 'CallExpression' && o.callee.name === 'X') || (o.type === 'Identifier' && o.name === 'x');
      if (isX && !freshKeys.some((k) => k.sys === sys && k.key === propName(n.left))) freshKeys.push({ sys, key: propName(n.left), where: line(p, n) });
    }
  });
}
const WRITERS = new Set(['push', 'unshift', 'splice', 'pop', 'shift', 'fill', 'sort']);
function useOf(m) {
  // 'write' | 'read' | 'hook'
  const par = m.parent;
  if (par.type === 'AssignmentExpression' && par.left === m) return 'write';
  if (par.type === 'UpdateExpression') return 'write';
  if (par.type === 'UnaryExpression' && par.operator === 'delete') return 'write';
  if (par.type === 'MemberExpression' && par.object === m) {
    const f = propName(par),
      gp = par.parent;
    if (gp.type === 'CallExpression' && gp.callee === par && WRITERS.has(f) && gp.parent.type === 'ExpressionStatement') return 'write';
    if (f === 'length' && gp.type === 'AssignmentExpression' && gp.left === par) return 'write';
    // the prune: a.f = a.f.filter(...)
    if (gp.type === 'CallExpression' && gp.callee === par && (f === 'filter' || f === 'slice' || f === 'concat' || f === 'map')) {
      const ggp = gp.parent;
      if (ggp.type === 'AssignmentExpression' && ggp.right === gp && ggp.left.type === 'MemberExpression' && propName(ggp.left) === propName(m)) return 'write';
    }
    // a.f[k] = v ; a.f.g = v ; a.f[k]++ : writes into it
    if (gp.type === 'AssignmentExpression' && gp.left === par) return 'write';
    if (gp.type === 'UpdateExpression') return 'write';
  }
  // x.f = x.f || [] ; x.f = (x.f || 0) + 1 : a read only to write itself back
  for (let q = par, depth = 0; q && depth < 4; q = q.parent, depth++)
    if (q.type === 'AssignmentExpression' && q.left.type === 'MemberExpression' && propName(q.left) === propName(m)) return 'write';
  // (x.f = x.f || []).push(...)
  return inHook(m) ? 'hook' : 'read';
}
const uses = {}; // key -> { read, hook, write }
const wanted = new Set(freshKeys.map((k) => k.key));
for (const p of files.filter((f) => !isPiece(f)))
  walk(parsed[p].ast, (n) => {
    if (n.type === 'MemberExpression') {
      const k = propName(n);
      if (k && wanted.has(k)) {
        const u = (uses[k] = uses[k] || { read: 0, hook: 0, write: 0 });
        u[useOf(n)]++;
      }
    }
    // a destructure reads: const { watched } = x
    if (n.type === 'ObjectPattern') for (const q of n.properties) if (q.type === 'Property' && wanted.has(q.key.name)) (uses[q.key.name] = uses[q.key.name] || { read: 0, hook: 0, write: 0 }).read++;
  });
const seenKey = new Set();
for (const k of freshKeys) {
  const id = k.sys + '.' + k.key;
  if (seenKey.has(id)) continue;
  seenKey.add(id);
  const u = uses[k.key] || { read: 0, hook: 0, write: 0 };
  if (k.key === 'v') continue;
  if (!u.read) out.writeOnly.push({ id: 'G.x.' + id, where: k.where, why: u.hook ? 'written, and read only by the test hook' : u.write ? 'written and never read' : 'made and never used' });
}

// ---------- 5: a log line or a Ledger line standing in for something felt ----------
const FELT = new Set(['tell', 'sub', 'scene', 'say', 'choose', 'act', 'pay', 'earn', 'emit', 'goToPoint', 'startChase', 'toast', 'show', 'spend', 'take']);
for (const p of files.filter((f) => rel(f).startsWith('game/') && !isPiece(f) && !/\/(tune|kinds|cast)\//.test(rel(f)))) {
  const { ast } = parsed[p];
  const fns = [];
  walk(ast, (n) => isFn(n) && fns.push(n));
  for (const f of fns) {
    if (inHook(f)) continue;
    let log = 0,
      ledger = 0,
      felt = 0,
      changes = 0,
      callsOther = 0,
      returns = 0;
    walk(f.body, (n) => {
      if (n.type === 'CallExpression') {
        const nm = n.callee.type === 'Identifier' ? n.callee.name : n.callee.type === 'MemberExpression' ? propName(n.callee) : null;
        if (nm === 'logLine') log++;
        else if (nm === 'write' || nm === 'note') ledger++;
        else if (FELT.has(nm)) felt++;
        else if (n.callee.type === 'Identifier' && /^[a-z]/.test(nm || '') && !['hyp', 'quid', 'hourNow', 'dayNow', 'X', 'P_', 'here', 'tomXZ', 'tomNear', 'freshLine', 'String', 'Number'].includes(nm)) callsOther++;
        else if (n.callee.type === 'MemberExpression' && WRITERS.has(nm)) changes++;
      }
      if (n.type === 'AssignmentExpression' && n.left.type === 'MemberExpression') changes++;
      if (n.type === 'UpdateExpression' && n.argument.type === 'MemberExpression') changes++;
      if (n.type === 'ReturnStatement' && n.argument && fnOf(n) === f) returns++;
    });
    if (f.body.type !== 'BlockStatement') returns++;
    if (!(log + ledger) || felt || changes || callsOther) continue;
    // an arrow that is nothing but the line itself, handed to on(): the event ends in the log or the Ledger alone
    const name = f.id ? f.id.name : f.parent.type === 'VariableDeclarator' ? f.parent.id.name : f.parent.type === 'Property' ? f.parent.key.name || f.parent.key.value : f.parent.type === 'CallExpression' && f.parent.arguments[0] && f.parent.arguments[0].type === 'Literal' ? "on('" + f.parent.arguments[0].value + "')" : '(a function)';
    if (returns && !log) continue; // it returns something as well: its caller may do the felt part
    out.logOnly.push({ id: name, where: line(p, f), why: log && !ledger ? 'its only effect is a line in G.log, which the player never sees' : 'its only effect is a line in the Ledger' + (log ? ' and one in G.log' : '') });
  }
  // a log line whose words say something happened in the world ("went to", "came", "an officer"), in a function with
  // no act and nothing moved: listed apart, since the player meets nothing
  walk(ast, (n) => {
    if (n.type !== 'CallExpression' || n.callee.name !== 'logLine') return;
    const f = fnOf(n);
    if (!f || inHook(n)) return;
    let moved = 0;
    walk(f.body, (m) => {
      if (m.type === 'CallExpression') {
        const nm = m.callee.type === 'Identifier' ? m.callee.name : propName(m.callee);
        if (['goToPoint', 'act', 'tell', 'sub', 'scene', 'say', 'choose', 'startChase', 'sendTo', 'walkTo', 'place', 'spawn'].includes(nm)) moved++;
      }
    });
    const words = parsed[p].text.slice(n.start, n.end);
    if (!moved && /went to|came |An officer|arrive|walk/i.test(words) && !out.logOnly.some((o) => o.where === line(p, f))) out.logOnly.push({ id: 'logLine', where: line(p, n), why: 'the log says somebody went somewhere, and nobody is moved or shown: ' + words.slice(0, 90).replace(/\s+/g, ' ') });
  });
}

// ---------- 6: a system's exported function nobody uses ----------
for (const p of files.filter((f) => rel(f).startsWith('game/') && !isPiece(f) && !/\/(tune|kinds|cast|sim)\//.test(rel(f)) && !/(_all|index|systems)\.js$/.test(rel(f)))) {
  const names = [];
  for (const st of parsed[p].ast.body)
    if (st.type === 'ExportNamedDeclaration' && st.declaration) {
      if (st.declaration.type === 'FunctionDeclaration') names.push([st.declaration.id.name, st]);
      if (st.declaration.type === 'VariableDeclaration') for (const d of st.declaration.declarations) if (d.id.type === 'Identifier' && d.init && isFn(d.init)) names.push([d.id.name, st]);
    }
  for (const [name, node] of names) {
    let used = 0;
    for (const q of files) {
      walk(parsed[q].ast, (n) => {
        if (n.type !== 'Identifier' || n.name !== name) return;
        const par = n.parent;
        if (par.type === 'FunctionDeclaration' && par.id === n) return;
        if (par.type === 'VariableDeclarator' && par.id === n) return;
        if (par.type === 'ImportSpecifier' || par.type === 'ExportSpecifier') return;
        if (par.type === 'MemberExpression' && par.property === n && !par.computed) return;
        if (q === p && inHook(n)) return; // offered to tests only
        if (q !== p && par.type === 'Property' && par.key === n && par.value !== n) return;
        used++;
      });
    }
    if (!used) out.deadExports.push({ id: path.basename(p, '.js') + '.' + name, where: line(p, node), why: 'exported, and called by nothing in the game (a test hook at most)' });
  }
}

// ---------- report ----------
const total = Object.values(out).reduce((a, l) => a + l.length, 0);
const heads = {
  deadFns: '1. Rule functions the game never calls',
  ignored: '2. Returned fields no caller reads (where it can tell)',
  unheard: '3. Events nobody listens for',
  writeOnly: '4. Saved fields written and never read by the game',
  logOnly: '5. A log or Ledger line standing in for something felt (where it can tell)',
  deadExports: "6. A system's function nobody in the game calls",
};
if (args.includes('--json')) console.log(JSON.stringify({ total, counts: Object.fromEntries(Object.entries(out).map(([k, v]) => [k, v.length])), out }, null, 1));
else {
  let md = '# Dead rules: what the build holds and the game never uses\n\n';
  md += 'Written by tools/lane/prototype/dead_rules.mjs (a machine reading of the source, nothing run). ' + new Date().toISOString().slice(0, 16) + ' UTC. The aim is zero.\n\n';
  md += 'Total: ' + total + ' (' + Object.entries(out).map(([k, v]) => heads[k].split('. ')[0] + ': ' + v.length).join(', ') + ').\n';
  for (const [k, list] of Object.entries(out)) {
    md += '\n## ' + heads[k] + ' (' + list.length + ')\n\n';
    for (const o of list) md += '- ' + o.id + ': ' + o.why + ' (' + o.where + ')\n';
    if (!list.length) md += 'None.\n';
  }
  const o = argOf('--out');
  if (o) fs.writeFileSync(o, md);
  else console.log(md);
}
console.log('DEAD RULES: ' + total + ' (' + Object.values(out).map((l) => l.length).join(' + ') + ')');
const max = argOf('--max');
process.exit(max !== null && total > Number(max) ? 1 : 0);
