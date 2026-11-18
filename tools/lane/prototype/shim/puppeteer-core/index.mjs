// The lane's stand-in for puppeteer-core (18 Nov 2026). The prototype's tests were written for
// puppeteer-core and a system Chrome at /usr/bin/google-chrome; the cloud has Playwright's own
// Chromium instead. This module gives the tests the calls they use, carried out by Playwright,
// so neither the game nor its tests change. Only these calls exist:
//   puppeteer.launch({ args, headless, executablePath }) -> browser (executablePath is ignored)
//   browser.newPage(), browser.close()
//   page.setViewport, goto, evaluate(fn, ...args), evaluateOnNewDocument(fn, ...args),
//   waitForFunction(text | fn, options), click(selector), mouse.click(x, y), on('console' |
//   'pageerror', handler), screenshot(options), close()
// Playwright passes one argument into the page, Puppeteer several: functions are sent as text
// with their arguments as JSON, so every argument must be plain data (as all of the tests' are).
import { createRequire } from 'module';

function findPlaywright() {
  const tries = [process.env.LEDGER_PLAYWRIGHT, 'playwright', 'playwright-core'].filter(Boolean);
  const req = createRequire(import.meta.url);
  for (const t of tries) {
    try { return req(t); } catch (e) { /* next */ }
  }
  // the cloud's global install
  const g = createRequire('/usr/lib/node_modules/');
  for (const t of ['playwright', 'playwright-core']) {
    try { return g(t); } catch (e) { /* next */ }
  }
  const npmRoot = process.env.NPM_GLOBAL_ROOT;
  if (npmRoot) { try { return createRequire(npmRoot + '/')('playwright'); } catch (e) { /* none */ } }
  throw new Error('playwright not found (set LEDGER_PLAYWRIGHT to its folder)');
}

const asCall = (fn, args) => {
  const src = typeof fn === 'function' ? fn.toString() : String(fn);
  if (typeof fn !== 'function') return src;
  return `(${src})(...${JSON.stringify(args)})`;
};

function wrapPage(pg) {
  return {
    _pw: pg,
    setViewport: (v) => pg.setViewportSize({ width: v.width, height: v.height }),
    goto: (url, o) => pg.goto(url, o),
    evaluate: (fn, ...args) => pg.evaluate(asCall(fn, args)),
    evaluateOnNewDocument: (fn, ...args) => pg.addInitScript({ content: asCall(fn, args) }),
    waitForFunction: (fn, o = {}) => pg.waitForFunction(typeof fn === 'function' ? asCall(fn, []) : fn, undefined, { timeout: o.timeout, polling: o.polling }),
    click: (sel) => pg.click(sel),
    mouse: { click: (x, y, o) => pg.mouse.click(x, y, o) },
    keyboard: pg.keyboard,
    on: (name, handler) => {
      if (name === 'console') pg.on('console', handler); // same text() and type() ('warning', 'error')
      else if (name === 'pageerror') pg.on('pageerror', handler);
      else pg.on(name, handler);
    },
    screenshot: (o) => pg.screenshot(o),
    close: () => pg.close(),
  };
}

async function launch(o = {}) {
  const { chromium } = findPlaywright();
  const args = (o.args || []).filter((a) => !a.startsWith('--window-size'));
  const b = await chromium.launch({ headless: o.headless !== false, args });
  const ctx = await b.newContext();
  return {
    newPage: async () => wrapPage(await ctx.newPage()),
    close: () => b.close(),
  };
}

export default { launch };
export { launch };
