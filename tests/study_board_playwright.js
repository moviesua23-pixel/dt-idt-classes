const { chromium } = require("playwright");
const path = require("path");

const TARGET_URL = process.env.TARGET_URL || "http://127.0.0.1:4173/";
const SHOT_DIR = process.env.SCREENSHOT_DIR || path.join(require("os").tmpdir(), "study-board-playwright");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on("pageerror", error => errors.push(`pageerror: ${error.message}`));
  page.on("console", message => {
    if (message.type() === "error") {
      const text = message.text();
      const loc = message.location();
      const url = loc ? (loc.url || "") : "";
      if (text.includes("Failed to load resource") && (url.includes(".mp3") || url.includes(".wav") || url.includes("data/audio") || text.includes(".mp3") || text.includes(".wav") || text.includes("data/audio"))) {
        console.warn(`[audio 404 ignored]: ${url || text}`);
        return;
      }
      errors.push(`console: ${text}${url ? ` (${url})` : ""}`);
    }
  });

  try {
    await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
    await page.waitForFunction(() => window.D?.qna?.length > 0, { timeout: 20000 });
    await page.waitForFunction(() => window.__pipelineUpdateLoaded === true && window.__sheetScriptFinished === true, { timeout: 30000 });
    const questions = await page.evaluate(() => window.D.qna.map(q => ({
      qid: `dt-c${q.ch}-q${q.n}`,
      hash: `#dt-c${q.ch}-q${q.n}`,
      title: q.title || "",
      ch: q.ch,
      n: q.n,
    })));
    const fs = require("fs");
    fs.mkdirSync(SHOT_DIR, { recursive: true });
    const failures = [];
    let totalBeats = 0;

    for (const question of questions) {
      console.log(`Checking ${question.qid}`);
      await page.goto(`${TARGET_URL.replace(/#.*$/, "")}${question.hash}`, { waitUntil: "domcontentloaded" });
      await page.waitForFunction(qid => window.__explainer?.sp?.question_id === qid && window.__explainer?.beatEls?.length > 0, question.qid, { timeout: 20000 });
      await page.waitForFunction(() => document.querySelector("#vtheater")?.classList.contains("open"), undefined, { timeout: 10000 });
      const meta = await page.evaluate(() => ({
        qid: window.__explainer.sp.question_id,
        beats: window.__explainer.sp.beats.map(beat => ({ id: beat.id, layout: beat.layout, start: beat.start, end: beat.end, title: beat.title?.text || "" })),
        templates: window.LAYOUTS,
        body: document.body.innerText,
      }));
      totalBeats += meta.beats.length;
      if (meta.qid !== question.qid) failures.push(`${question.qid}: loaded ${meta.qid}`);
      if (!meta.body.includes(question.title.slice(0, 32))) failures.push(`${question.qid}: visible study board title does not match the question`);

      for (let index = 0; index < meta.beats.length; index++) {
        const beat = meta.beats[index];
        if (!meta.templates.includes(beat.layout)) failures.push(`${question.qid}/${beat.id}: unknown layout ${beat.layout}`);
        const midpoint = Math.max(0, (Number(beat.start) + Number(beat.end)) / 2);
        const hasActiveBeat = await page.evaluate(time => { window.__explainer.seek(time); return !!document.querySelector(".beat.active"); }, midpoint);
        if (!hasActiveBeat) { failures.push(`${question.qid}/${beat.id}: seeking did not activate a presentation beat`); continue; }
        const visible = await page.evaluate(() => {
          const beat = document.querySelector(".beat.active");
          const text = beat?.innerText || "";
          const svg = beat?.querySelector("svg");
          let overflow = [];
          if (svg) {
            const view = svg.viewBox.baseVal;
            for (const node of svg.querySelectorAll("text")) {
              try {
                const box = node.getBBox();
                if (box.x < -2 || box.y < -2 || box.x + box.width > view.width + 2 || box.y + box.height > view.height + 2) overflow.push(node.textContent);
              } catch (error) {}
            }
          }
          const htmlOverflow = [...(beat?.querySelectorAll("*") || [])].filter(node => node.childElementCount === 0 && node.textContent?.trim() && node.clientWidth > 0 && node.scrollWidth > node.clientWidth + 3 && getComputedStyle(node).overflowX !== "visible").map(node => node.className?.baseVal || node.className || node.tagName).slice(0, 5);
          return { text, overflow, htmlOverflow };
        });
        if (/\bBeat\s+\d+\b/i.test(visible.text)) failures.push(`${question.qid}/${beat.id}: generic Beat N label`);
        if (visible.overflow.length) failures.push(`${question.qid}/${beat.id}: SVG text overflow ${visible.overflow.join(" | ")}`);
        if (visible.htmlOverflow.length) failures.push(`${question.qid}/${beat.id}: HTML text overflow ${visible.htmlOverflow.join(" | ")}`);
        await page.locator("#expFocal").screenshot({ path: path.join(SHOT_DIR, `${question.qid}-${String(index + 1).padStart(2, "0")}-${beat.layout}.png`), animations: "disabled", timeout: 60000 });
      }
    }

    const nativeSamples = {
      example_scene: { actors: [{ label: "Assessee", icon: "person" }], transaction: "Asset transfer", facts: [{ label: "Illustrative amount", value: "₹ 10,00,000" }] },
      decision_tree: { root: "Apply Section 54", branches: [{ label: "Condition met", detail: "Eligible" }, { label: "Condition not met", detail: "No exemption" }] },
      checklist_gate: { conditions: [{ label: "Ownership condition", status: "Check" }, { label: "Time condition", status: "Check" }], outcome: "All conditions must pass" },
      timeline_windows: { events: [{ label: "Transfer", date: "1 April 2025" }, { label: "Deadline", date: "31 March 2026" }], window_label: "Statutory reinvestment period" },
      flow_actors: { actors: [{ label: "Payer", icon: "person" }, { label: "Payee", icon: "bank" }, { label: "Government", icon: "document" }], edges: [{ label: "Deduct tax" }, { label: "Deposit TDS" }] },
      compare_regimes: { regimes: [{ label: "Regime A", detail: "First treatment" }, { label: "Regime B", detail: "Alternative treatment" }] },
      slab_ladder: { tiers: [{ label: "First slab", value: "0%" }, { label: "Next slab", value: "5%" }, { label: "Balance", value: "20%" }] },
      ledger: { rows: [{ label: "Gross amount", value: "₹ 10,00,000" }, { label: "Less: deduction", value: "₹ 2,00,000" }], total: "Net amount · ₹ 8,00,000" },
      waterfall: { stages: [{ label: "Income", value: "₹ 10,00,000" }, { label: "Set off", value: "₹ 2,00,000" }, { label: "Balance", value: "₹ 8,00,000" }] },
      deemed_value: { actual: { label: "Actual consideration", value: "₹ 8,00,000" }, deemed: { label: "Stamp value", value: "₹ 10,00,000" }, rule: "Apply the statutory substitution rule" },
      case_card: { case_name: "CIT v. Taxpayer", court: "High Court", principle: "Legal principle", application: "Applied to the example" },
      statute_quote: { rule: "The statutory rule applies to the described transaction.", citation: "Section 54", application: "Check the stated conditions" },
      takeaway: { rules: [{ label: "Check eligibility" }, { label: "Check the date" }, { label: "Compute the result" }] },
    };
    for (const [layout, visual_data] of Object.entries(nativeSamples)) {
      const screenplay = { question_id: "dt-c99-q1", duration_sec: 12, context_pill: `Renderer check · ${layout}`, beats: [{ id: "b1", layout, start: 0, end: 12, animation_role: "key_fact", voice_sync_text: "Illustrative amount ₹ 10,00,000 and date 1 April 2025.", title: { text: `Renderer check · ${layout}`, at: 0.2 }, visual_data }] };
      await page.evaluate(async value => { window.__explainer.pause(); await window.__explainer.load(value.question_id, value); window.__explainer.seek(4); }, screenplay);
      const mounted = await page.evaluate(() => {
        const beat = document.querySelector(".beat.active");
        const svg = beat?.querySelector("svg");
        if (!beat || !svg) return { ok: false, overflow: [] };
        const view = svg.viewBox.baseVal;
        const overflow = [...svg.querySelectorAll("text")].filter(node => { const box=node.getBBox(); return box.x < -2 || box.y < -2 || box.x+box.width > view.width+2 || box.y+box.height > view.height+2; }).map(node=>node.textContent);
        return { ok: true, overflow };
      });
      if (!mounted.ok) failures.push(`${layout}: native renderer failed to mount a beat`);
      if (mounted.overflow.length) failures.push(`${layout}: native SVG text overflow ${mounted.overflow.join(" | ")}`);
      else if (mounted.ok) await page.locator("#expFocal").screenshot({ path: path.join(SHOT_DIR, `native-layout-${layout}.png`), animations: "disabled", timeout: 60000 });
    }

    if (errors.length) failures.push(...errors);
    console.log(JSON.stringify({ questions: questions.length, beats: totalBeats, nativeLayouts: Object.keys(nativeSamples).length, screenshots: SHOT_DIR, consoleErrors: errors.length, failures }, null, 2));
    if (failures.length) process.exitCode = 1;
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
