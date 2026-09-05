/* Runnable browser QA. No fixture tiles, scientific feeds or baseline writes.
 * Start the app on localhost:8050; see docs/replay/README.md for environment.
 */
const { chromium, firefox } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const base = process.env.HATI_URL || 'http://127.0.0.1:8050';
const out = path.resolve('docs/replay/qa');
fs.mkdirSync(out, { recursive: true });
const report = { timestamp: new Date().toISOString(), browsers: [], scientificFixtures: 'Only an intentionally corrupted temporary copy for integrity failure; no synthetic tiles.' };
const expected = { S1: [9,17], S2: [6,20], S3: [4,22], S4: [8,18], S5: [7,19], S6: [9,17], S7: [6,20], S8: [0,26] };
const sources = {S1:'A16', S2:'A15', S3:'A14', S4:'A26', S5:'A19', S6:'A17', S7:'A24', S8:'A20'};

async function scenario(page, sid) {
  await page.locator('#scenario-menu-btn').click();
  await page.getByRole('menuitem').filter({ hasText: new RegExp('^' + sid) }).click();
  await page.locator(`.replay-panel[data-scenario="${sid}"]`).waitFor();
  await page.waitForFunction(([count]) => document.querySelectorAll('.replay-map-badge[data-role="CANDIDATE_ALTERNATIVE"]').length === count, expected[sid]);
  await selected(page, sources[sid]);
  await page.waitForFunction(() => document.activeElement?.id === 'replay-selected-title');
}
async function selected(page, aid) {
  await page.waitForFunction(id => document.querySelector('#replay-selected-title')?.textContent.startsWith(id + ' ·'), aid);
}
async function candidate(page, aid, keyboard = false) {
  const button = page.locator(`.replay-candidate[data-asset="${aid}"]`);
  if (keyboard) { await button.focus(); await page.keyboard.press('Enter'); }
  else await button.click();
  await selected(page, aid);
}
async function textIncludes(page, selector, value) {
  assert.ok((await page.locator(selector).innerText()).includes(value), `${selector} contains ${value}`);
}
async function bindings(page, sid) {
  const [survivors, excluded] = expected[sid];
  await textIncludes(page, '#replay-tally', `${survivors} survivors · ${excluded} exclusions`);
  assert.equal(await page.locator('.replay-map-badge[data-role="SOURCE"]').count(), 1);
  assert.equal(await page.locator('.replay-map-badge[data-role="EXCLUDED"]').count(), excluded);
  assert.equal(await page.locator('#replay-candidates .replay-candidate').count(), 26);
  assert.equal(await page.locator('#replay-candidates [data-role="CANDIDATE_ALTERNATIVE"]').count(), survivors);
  const marker = await page.locator('.leaflet-marker-icon').first().getAttribute('title');
  assert.ok(marker.includes(`Scenario ${sid}`));
}

async function run(name, engine, executablePath) {
  if (!fs.existsSync(executablePath)) {
    report.browsers.push({ name, status: 'UNAVAILABLE', executablePath }); return;
  }
  const result = { name, status: 'RUNNING', checks: [], executablePath };
  report.browsers.push(result);
  const browser = await engine.launch({ headless: true, executablePath });
  result.version = browser.version();
  const errors = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base);
    await page.locator('.leaflet-marker-icon').nth(26).waitFor();
    await textIncludes(page, '#replay-context', 'No precomputed scenario at this timestamp.');
    assert.equal(await page.locator('.replay-map-badge').count(), 0);
    result.checks.push('12:00 asset-only initial state');

    // Inspect the genuine tile outcome separately; never substitute geographic imagery.
    try { await page.waitForFunction(() => [...document.querySelectorAll('.leaflet-tile')].some(i => i.complete && i.naturalWidth > 0), null, { timeout: 8000 }); }
    catch {}
    result.actualBasemap = await page.locator('.leaflet-tile').evaluateAll(imgs => ({loaded: imgs.filter(i => i.complete && i.naturalWidth > 0).length, failed: imgs.filter(i => i.complete && !i.naturalWidth).length}));
    await page.screenshot({ path: path.join(out, `${name}-actual-basemap.png`) });

    for (const sid of Object.keys(expected)) { await scenario(page, sid); await bindings(page, sid); }
    result.checks.push('All S1–S8 source/survivor/excluded map and list counts');
    await textIncludes(page, '.replay-panel', 'includes out-of-reach assets');
    await page.getByText('Recorded exclusion groups', {exact:true}).click();
    await textIncludes(page, '.replay-panel', 'ACCESSIBILITY_CONSTRAINT: 15');
    await textIncludes(page, '.replay-panel', 'OUTDOOR_EXPOSURE_TOO_HIGH: 6');
    await textIncludes(page, '.replay-panel', 'CLOSED_AT_TIMESTAMP: 5');
    result.checks.push('S8 recorded first-failure groups and universe wording');

    await scenario(page, 'S4'); await candidate(page, 'A24', true);
    await textIncludes(page, '#replay-facts', 'INSUFFICIENT_EVIDENCE');
    await textIncludes(page, '#replay-facts', 'UNSTABLE');
    await page.locator('[data-artifact="scenarios"] summary').click();
    await textIncludes(page, '[data-artifact="scenarios"]', 'scenario=S4; candidate_id=A24');
    await textIncludes(page, '[data-artifact="scenarios"]', 'SHA-256:');
    assert.ok((await page.locator('[data-artifact="scenarios"] a').getAttribute('href')).includes('036c50b273b539140260097760a148893176f7ec'));
    await page.screenshot({ path: path.join(out, `${name}-a24-evidence.png`) });
    await page.getByRole('button', {name:'Back to scenario overview', exact:true}).click();
    await selected(page, 'A26');
    await scenario(page, 'S7'); await selected(page, 'A24');
    await textIncludes(page, '#replay-facts', 'Source — not evaluated as its own candidate');
    await textIncludes(page, '#replay-facts', 'UNSTABLE');
    result.checks.push('A24 excluded candidate vs uncertain source; keyboard candidate selection; pinned provenance; back navigation');

    // A non-source candidate retains its scenario; changing time must clear it.
    await scenario(page, 'S1'); await candidate(page, 'A01');
    await textIncludes(page, '#replay-facts', 'Not physically modelled for indoor assets.');
    await page.getByText('12:00', {exact:true}).click();
    await page.waitForFunction(() => !document.querySelector('.replay-panel'));
    await textIncludes(page, '#replay-context', 'No precomputed scenario at this timestamp.');
    assert.equal(await page.locator('.replay-map-badge').count(), 0);
    assert.equal(await page.getByRole('button', {name:'Back to scenario overview', exact:true}).count(), 0);
    await scenario(page, 'S8'); await page.reload();
    await page.locator('.leaflet-marker-icon').nth(26).waitFor();
    await textIncludes(page, '#replay-context', 'No precomputed scenario at this timestamp.');
    assert.equal(await page.locator('.replay-panel').count(), 0);
    result.checks.push('Candidate/time invalidation, no stale back link, refresh resets to valid 12:00 state');

    await scenario(page, 'S1');
    const marker = page.locator('.leaflet-marker-icon[title^="A03 "]');
    await marker.focus(); await page.keyboard.press('Space'); await selected(page, 'A03');
    await page.locator('#limitations-open').click();
    await page.getByRole('dialog').waitFor();
    await page.keyboard.press('Escape');
    await page.getByRole('dialog').waitFor({state:'hidden'});
    await page.getByRole('button', {name:'Close inspection', exact:true}).click();
    await page.waitForFunction(() => document.querySelector('#side-panel').className.includes('--closed'));
    assert.equal(await page.locator('.replay-map-badge').count(), 0);
    result.checks.push('Space marker activation, Escape overlay, close clears scenario/panel');

    for (const width of [900, 390]) {
      await page.setViewportSize({width, height:844});
      await scenario(page, 'S1'); await candidate(page, 'A01', true);
      await bindings(page, 'S1');
      assert.ok(await page.locator('#replay-evidence').isVisible());
      const dimensions = await page.evaluate(() => ({width:innerWidth, doc:document.documentElement.scrollWidth, map:document.querySelector('#map-canvas').getBoundingClientRect().height, panel:document.querySelector('#side-panel').getBoundingClientRect().height, headerTop:document.querySelector('.command-bar').getBoundingClientRect().top, panelBottom:document.querySelector('#side-panel').getBoundingClientRect().bottom, height:innerHeight}));
      assert.ok(dimensions.doc <= dimensions.width + 1, JSON.stringify(dimensions));
      assert.ok(dimensions.map >= 180 && dimensions.panel >= 200, JSON.stringify(dimensions));
      assert.ok(dimensions.headerTop >= -1 && dimensions.panelBottom <= dimensions.height + 1, JSON.stringify(dimensions));
      await page.screenshot({path:path.join(out, `${name}-${width}px.png`)});
    }
    result.checks.push('900px and 390px layout, no horizontal overflow, keyboard selection');

    const blocked = await browser.newPage({ viewport:{width:1440,height:900} });
    await blocked.route('**/*.basemaps.cartocdn.com/**', route => route.abort());
    await blocked.goto(base); await blocked.locator('.leaflet-marker-icon').nth(26).waitFor();
    await scenario(blocked, 'S1'); await candidate(blocked, 'A01');
    await blocked.locator('#map-surface[data-tiles="failed"]').waitFor();
    await textIncludes(blocked, '.tile-fallback', 'pinned local snapshot');
    await bindings(blocked, 'S1');
    await blocked.screenshot({path:path.join(out, `${name}-blocked-tiles.png`)});
    result.checks.push('Blocked genuine tile requests preserve map markers and scientific records');

    if (process.env.HATI_PYTHON) {
      const child = spawn(process.env.HATI_PYTHON, ['-B', 'tests/replay/serve_integrity_failure.py'], {windowsHide:true, stdio:'ignore'});
      try {
        const failure = await browser.newPage();
        for (let tries = 0; tries < 50; tries++) {
          try { await failure.goto('http://127.0.0.1:8051'); break; }
          catch { await new Promise(r => setTimeout(r, 200)); }
        }
        await failure.locator('#replay-integrity-error').waitFor();
        await textIncludes(failure, '#replay-integrity-error', 'SHA-256 mismatch');
        assert.equal(await failure.locator('.leaflet-marker-icon, .replay-panel').count(), 0);
        result.checks.push('Real hash failure in temporary test copy blocks scientific display');
      } finally { child.kill(); }
    } else result.integrityBrowser = 'NOT RUN: set HATI_PYTHON';
    assert.deepEqual(errors, []);
    result.status = 'PASS';
  } catch (error) {
    result.status = 'FAIL'; result.error = error.stack;
    const pages = browser.contexts().flatMap(context => context.pages());
    if (pages.length) await pages[0].screenshot({path:path.join(out, `${name}-failure.png`)});
    process.exitCode = 1;
  } finally { await browser.close(); }
}

(async () => {
  await run('chromium', chromium, process.env.CHROMIUM_EXECUTABLE || chromium.executablePath());
  await run('firefox', firefox, process.env.FIREFOX_EXECUTABLE || firefox.executablePath());
  fs.writeFileSync(path.join(out, 'browser-results.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
