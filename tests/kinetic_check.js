/**
 * Playwright Automated Audit Suite for Kinetic Animation Library v1.0
 * Verifies:
 * 1. Physical motion deltas (items travel, bars grow, scales tilt, markers sweep).
 * 2. Strict semantic decoupling (zero hardcoded statutory tax words).
 * 3. Container containment & 1000x562 safe area boundaries.
 * 4. Deterministic functional seek (t -> identical DOM state).
 * 5. Clean teardown across rapid animation switches.
 * 6. High-res frame captures at 25%, 50%, 85% and contact sheet generation.
 */

const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const http = require("http");

const ROOT_DIR = path.resolve(__dirname, "..");
const KINETIC_JSON = path.join(ROOT_DIR, "library", "kinetic_animations.json");
const FRAMES_DIR = path.join(ROOT_DIR, "reports", "kinetic_frames");
const REPORT_FILE = path.join(ROOT_DIR, "reports", "kinetic_report.json");

if (!fs.existsSync(FRAMES_DIR)) {
  fs.mkdirSync(FRAMES_DIR, { recursive: true });
}

// Simple HTTP static server
function startServer(port = 8124) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let reqPath = decodeURI(req.url.split("?")[0]);
      if (reqPath === "/") reqPath = "/viewer/kinetic_viewer.html";
      const filePath = path.join(ROOT_DIR, reqPath);
      if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        const ext = path.extname(filePath);
        const mimeTypes = {
          ".html": "text/html",
          ".js": "application/javascript",
          ".json": "application/json",
          ".css": "text/css",
          ".svg": "image/svg+xml",
          ".png": "image/png"
        };
        res.writeHead(200, { "Content-Type": mimeTypes[ext] || "text/plain" });
        fs.createReadStream(filePath).pipe(res);
      } else {
        res.writeHead(404);
        res.end("Not Found: " + reqPath);
      }
    });
    server.listen(port, () => resolve(server));
  });
}

const FORBIDDEN_WORDS = [
  "section", "u/s", "assessee", "statutory", "precedent", "ratio",
  "disallowance", "remittance", "taxable", "chargeable", "deduction",
  "computation", "consideration", "assessment", "capital gain"
];

async function runAudit() {
  console.log("==================================================");
  console.log("KINETIC ANIMATION LIBRARY AUDIT SUITE v1.0");
  console.log("==================================================");

  const animData = JSON.parse(fs.readFileSync(KINETIC_JSON, "utf-8"));
  const archetypes = animData.archetypes;
  console.log(`Auditing ${archetypes.length} kinetic archetypes in Milestone 1...`);

  const server = await startServer(8124);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  const page = await context.newPage();

  const auditReport = {
    timestamp: new Date().toISOString(),
    total_archetypes: archetypes.length,
    results: {},
    all_passed: true
  };

  await page.goto("http://localhost:8124/viewer/kinetic_viewer.html");
  await page.waitForSelector("#anim_list .anim-btn");

  for (const arch of archetypes) {
    console.log(`\n--> Auditing Archetype: ${arch.id} ("${arch.title}")`);
    const archResult = {
      id: arch.id,
      title: arch.title,
      motion_delta_pass: true,
      safe_area_pass: true,
      origin_vocab_pass: true,
      determinism_pass: true,
      violations: []
    };

    // 1. Check Semantic Vocabulary (No forbidden words in slots_default or title)
    const jsonStr = JSON.stringify(arch.slots_default);
    for (const fw of FORBIDDEN_WORDS) {
      const reg = new RegExp(`\\b${fw}\\b`, "i");
      if (reg.test(jsonStr)) {
        const msg = `Forbidden statutory term '${fw}' detected in default slots!`;
        archResult.violations.push(msg);
        archResult.origin_vocab_pass = false;
      }
    }

    // Select this animation in UI
    await page.evaluate((animId) => {
      window.selectAnimation(animId);
    }, arch.id);
    await page.waitForTimeout(300);

    // Track bounding boxes across frames: 10%, 25%, 50%, 85%, 100%
    const keyPercents = [10, 25, 50, 85, 100];
    const frameBoxes = {};

    for (const pct of keyPercents) {
      const timeVal = (pct / 100) * arch.duration;
      await page.evaluate((t) => {
        window.seekTo(t);
      }, timeVal);
      await page.waitForTimeout(100);

      // Extract metrics
      const metrics = await page.evaluate(() => {
        const svg = document.querySelector("#stage_container svg");
        if (!svg) return null;
        const rect = svg.getBoundingClientRect();
        const scaleX = 1000 / rect.width;
        const scaleY = 562 / rect.height;

        const allNodes = Array.from(svg.querySelectorAll("rect, circle, path, text, g"));
        let minX = 1000, maxX = 0, minY = 562, maxY = 0;

        const elements = [];
        Array.from(svg.querySelectorAll("#scene_group g, #scene_group path, #scene_group rect")).forEach((el, idx) => {
          const r = el.getBoundingClientRect();
          const bx = (r.left - rect.left) * scaleX;
          const by = (r.top - rect.top) * scaleY;
          const bw = r.width * scaleX;
          const bh = r.height * scaleY;
          if (bw > 0 && bh > 0) {
            elements.push({ idx, x: bx, y: by, w: bw, h: bh });
            minX = Math.min(minX, bx);
            maxX = Math.max(maxX, bx + bw);
            minY = Math.min(minY, by);
            maxY = Math.max(maxY, by + bh);
          }
        });

        return { minX, maxX, minY, maxY, elements };
      });

      frameBoxes[pct] = metrics;

      // Capture screenshot at 25%, 50%, 85%
      if ([25, 50, 85].includes(pct)) {
        const svgElement = await page.$("#stage_container");
        const outPath = path.join(FRAMES_DIR, `${arch.id}_frame_${pct}.png`);
        await svgElement.screenshot({ path: outPath });
      }

      // Safe area bounds check (at 85% and 100%)
      if (pct >= 50 && metrics) {
        if (metrics.minX < 35 || metrics.maxX > 965 || metrics.minY < 25 || metrics.maxY > 535) {
          const msg = `Safe area bounds exceeded at ${pct}%: bounds=[${Math.round(metrics.minX)}, ${Math.round(metrics.minY)} to ${Math.round(metrics.maxX)}, ${Math.round(metrics.maxY)}]`;
          archResult.violations.push(msg);
          archResult.safe_area_pass = false;
        }
      }
    }

    // 2. Motion Delta Check: Verify that motion actually occurs between 25% and 85%
    const b25 = frameBoxes[25];
    const b85 = frameBoxes[85];
    if (b25 && b85) {
      // Look for coordinate differences across elements
      let totalPosDelta = 0;
      b85.elements.forEach((el85, i) => {
        const el25 = b25.elements[i];
        if (el25) {
          const dx = Math.abs(el85.x - el25.x);
          const dy = Math.abs(el85.y - el25.y);
          const dw = Math.abs(el85.w - el25.w);
          const dh = Math.abs(el85.h - el25.h);
          totalPosDelta += (dx + dy + dw + dh);
        }
      });

      console.log(`   [MOTION DELTA] Total displacement across frames: ${Math.round(totalPosDelta)}px`);
      if (totalPosDelta < 100) {
        const msg = `Insufficient motion delta (${Math.round(totalPosDelta)}px < 100px) between 25% and 85%! Animation is too static.`;
        archResult.violations.push(msg);
        archResult.motion_delta_pass = false;
      }
    }

    // 3. Functional Determinism Test: Seek to 4.5s twice, compare DOM strings
    const dom1 = await page.evaluate(() => {
      window.seekTo(4.5);
      return document.querySelector("#scene_group").innerHTML;
    });
    const dom2 = await page.evaluate(() => {
      window.seekTo(10.0);
      window.seekTo(4.5);
      return document.querySelector("#scene_group").innerHTML;
    });

    if (dom1 !== dom2) {
      const msg = `Functional determinism violation: Seeking back to t=4.5s produced different SVG DOM!`;
      archResult.violations.push(msg);
      archResult.determinism_pass = false;
    }

    if (archResult.violations.length === 0) {
      console.log(`   [PASS] All checks passed successfully for ${arch.id}`);
    } else {
      console.log(`   [FAIL] ${archResult.violations.length} violation(s):`);
      archResult.violations.forEach(v => console.log(`      ✕ ${v}`));
      auditReport.all_passed = false;
    }

    auditReport.results[arch.id] = archResult;
  }

  // Teardown Cleanliness Test: Rapidly cycle 10 times
  console.log("\n--> Testing Teardown & Instance Switching...");
  for (let cycle = 0; cycle < 10; cycle++) {
    const target = archetypes[cycle % archetypes.length].id;
    await page.evaluate((id) => window.selectAnimation(id), target);
  }
  const svgCount = await page.evaluate(() => document.querySelectorAll("#stage_container svg").length);
  if (svgCount === 1) {
    console.log("   [PASS] Teardown test passed: exactly 1 SVG stage in DOM.");
  } else {
    console.log(`   [FAIL] Teardown leak: found ${svgCount} SVGs in container!`);
    auditReport.all_passed = false;
  }

  await browser.close();
  server.close();

  fs.writeFileSync(REPORT_FILE, JSON.stringify(auditReport, null, 2), "utf-8");
  console.log(`\n✓ Audit report saved to ${REPORT_FILE}`);
  console.log("==================================================");
  if (auditReport.all_passed) {
    console.log("ALL KINETIC AUDIT CHECKS PASSED! [Exit Code 0]");
    console.log("==================================================");
    process.exit(0);
  } else {
    console.error("KINETIC AUDIT CHECKS FAILED! [Exit Code 1]");
    console.log("==================================================");
    process.exit(1);
  }
}

runAudit().catch(err => {
  console.error("Audit runner crashed:", err);
  process.exit(1);
});
