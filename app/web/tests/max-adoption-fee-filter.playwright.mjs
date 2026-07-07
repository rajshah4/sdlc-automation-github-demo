#!/usr/bin/env node
/**
 * Playwright UI evidence for issue #101: Filter pets by max adoption fee.
 *
 * Covers the required scenarios:
 *   - below-threshold filter: max fee $80 excludes Scout ($125), shows Mochi ($75) + Pip ($45)
 *   - exact-boundary filter: max fee $75 includes Mochi at exactly the boundary
 *   - clearing max fee restores the full available-pet list
 *   - empty-state when max fee is below all available pets
 *   - family-friendly + max-fee combined filtering
 */
import { createRequire } from "node:module";
import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";

const require = createRequire(import.meta.url);
const execFileAsync = promisify(execFile);

function parseArgs(argv) {
  const args = {
    url: process.env.PETSTORE_WEB_URL || "http://localhost:4173",
    artifactDir:
      process.env.PLAYWRIGHT_ARTIFACT_DIR ||
      "/tmp/sdlc-petstore-playwright/max-adoption-fee-filter",
  };

  for (let index = 2; index < argv.length; index += 1) {
    const item = argv[index];
    if (item === "--url") {
      args.url = argv[++index];
    } else if (item === "--artifact-dir") {
      args.artifactDir = argv[++index];
    } else {
      throw new Error(`Unknown argument: ${item}`);
    }
  }

  return args;
}

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    console.error("Playwright is not available in this runtime.");
    console.error("Use NODE_PATH to point to an existing node_modules or install Playwright before running this script.");
    console.error(`Original error: ${error.message}`);
    process.exit(2);
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

async function names(page) {
  return page.locator("#results .pet strong").allTextContents();
}

async function assertNames(page, expected, scenario) {
  const actual = await names(page);
  assert(
    JSON.stringify(actual) === JSON.stringify(expected),
    `${scenario}: expected [${expected.join(", ") || "empty"}], got [${actual.join(", ") || "empty"}]`,
  );
}

async function commandExists(command) {
  try {
    await execFileAsync(command, ["-version"]);
    return true;
  } catch {
    return false;
  }
}

async function convertVideoToGif(videoPath, gifPath) {
  if (!(await commandExists("ffmpeg"))) {
    return false;
  }
  await execFileAsync("ffmpeg", [
    "-y",
    "-i",
    videoPath,
    "-vf",
    "fps=8,scale=960:-1:flags=lanczos",
    gifPath,
  ]);
  return true;
}

async function writeReport({ artifactDir, url, screenshotPath, videoPath, gifPath, gifCreated, scenarios }) {
  const reportPath = path.join(artifactDir, "qa-report.md");
  const targetUrl = new URL(url);
  const targetPort = targetUrl.port || (targetUrl.protocol === "https:" ? "443" : "80");
  const nodePathLine = process.env.NODE_PATH
    ? `NODE_PATH=${process.env.NODE_PATH} \\`
    : "# Set NODE_PATH=/path/to/node_modules if Playwright is installed outside this repo";
  const lines = [
    "# Playwright QA Report: Max Adoption Fee Filter (Issue #101)",
    "",
    "Status: pass",
    "",
    "## Target",
    "",
    `- URL: ${url}`,
    "- Change: Max fee ($) numeric input filters available pets by adoption fee",
    "",
    "## Browser Scenarios",
    "",
    ...scenarios.map((s) => `- [x] ${s}`),
    "",
    "## Artifacts",
    "",
    `- Screenshot: ${path.basename(screenshotPath)}`,
    `- Video: ${path.basename(videoPath)}`,
    gifCreated ? `- GIF preview: ${path.basename(gifPath)}` : "- GIF preview: not created (ffmpeg unavailable)",
    "",
    "## Commands",
    "",
    "```bash",
    nodePathLine,
    "python3 skills/sdlc-qa/scripts/with_server.py \\",
    `  --server "python3 -m http.server ${targetPort} --directory app/web" \\`,
    `  --port ${targetPort} \\`,
    "  -- node app/web/tests/max-adoption-fee-filter.playwright.mjs \\",
    `     --url ${url} \\`,
    `     --artifact-dir ${artifactDir}`,
    "```",
    "",
    "## Notes",
    "",
    "- Pet fees: Mochi=$75, Scout=$125, Pip=$45. Nova is pending and never appears.",
    "- Boundary is inclusive: a pet whose fee equals the max is shown (tested at $75 = Mochi's exact fee).",
    "- Family-friendly + max-fee coexistence is covered in this script.",
  ];

  await fs.writeFile(reportPath, `${lines.join("\n")}\n`, "utf8");
  return reportPath;
}

async function main() {
  const args = parseArgs(process.argv);
  const { chromium } = loadPlaywright();
  const artifactDir = path.resolve(args.artifactDir);
  const videosDir = path.join(artifactDir, "videos");
  await fs.mkdir(videosDir, { recursive: true });

  const launchOptions = { headless: true };
  if (process.env.PLAYWRIGHT_BROWSER_CHANNEL) {
    launchOptions.channel = process.env.PLAYWRIGHT_BROWSER_CHANNEL;
  }

  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    recordVideo: { dir: videosDir, size: { width: 1280, height: 800 } },
  });
  const page = await context.newPage();
  const video = page.video();
  const scenarios = [];

  try {
    await page.goto(args.url);
    await page.getByRole("heading", { name: "Petstore SDLC Demo" }).waitFor();

    // --- Scenario 1: default view ---
    await assertNames(page, ["Mochi", "Scout", "Pip"], "default available-pets view");
    scenarios.push("Default view shows all 3 available pets with no max-fee filter");

    // --- Scenario 2: below-threshold filter (max fee $80) ---
    // Mochi=$75 ✓, Pip=$45 ✓, Scout=$125 excluded
    const maxFeeInput = page.locator("#max-fee");
    await maxFeeInput.fill("80");
    await assertNames(page, ["Mochi", "Pip"], "below-threshold filter: max fee $80");
    scenarios.push("Below-threshold filter: max fee $80 shows Mochi ($75) and Pip ($45), excludes Scout ($125)");

    const screenshotPath = path.join(artifactDir, "max-fee-below-threshold.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });

    // --- Scenario 3: exact-boundary filter (max fee $75) ---
    // Mochi=$75 ✓ (inclusive boundary), Pip=$45 ✓, Scout=$125 excluded
    await maxFeeInput.fill("75");
    await assertNames(page, ["Mochi", "Pip"], "exact-boundary filter: max fee $75 = Mochi's fee");
    scenarios.push("Exact-boundary filter: max fee $75 includes Mochi at exactly $75 (inclusive)");

    // --- Scenario 4: empty state (max fee $44, below all available pets) ---
    await maxFeeInput.fill("44");
    await page.locator("#results .empty").waitFor();
    const emptyText = await page.locator("#results .empty").textContent();
    assert(emptyText === "No available pets match this search.", "max fee below all fees should show empty state");
    scenarios.push("Max fee $44 (below all available pets) shows the empty-state message");

    // --- Scenario 5: clearing max fee restores full list ---
    await maxFeeInput.fill("");
    await assertNames(page, ["Mochi", "Scout", "Pip"], "clearing max fee restores full available list");
    scenarios.push("Clearing max-fee input restores the full 3-pet available list");

    // --- Scenario 6: combined family-friendly + high max fee includes Scout ---
    const familyFriendlyCheckbox = page.locator("#family-friendly");
    await familyFriendlyCheckbox.check();
    await maxFeeInput.fill("150");
    await assertNames(page, ["Scout"], "family-friendly + max fee $150 includes Scout");
    scenarios.push("Family-friendly + max fee $150 shows Scout ($125)");

    // --- Scenario 7: combined family-friendly + low max fee excludes Scout ---
    await maxFeeInput.fill("100");
    await page.locator("#results .empty").waitFor();
    const combinedEmptyText = await page.locator("#results .empty").textContent();
    assert(
      combinedEmptyText === "No available pets match this search.",
      "family-friendly + max fee $100 should exclude Scout and show empty state",
    );
    scenarios.push("Family-friendly + max fee $100 excludes Scout ($125) and shows the empty state");

    await familyFriendlyCheckbox.uncheck();
    await maxFeeInput.fill("");
    await assertNames(page, ["Mochi", "Scout", "Pip"], "clearing combined filters restores full list");

    await context.close();
    await browser.close();

    const capturedVideoPath = await video.path();
    const stableVideoPath = path.join(artifactDir, "max-adoption-fee-filter.webm");
    await fs.copyFile(capturedVideoPath, stableVideoPath);
    await fs.rm(videosDir, { recursive: true, force: true }).catch(() => {});

    const gifPath = path.join(artifactDir, "max-adoption-fee-filter.gif");
    const gifCreated = await convertVideoToGif(stableVideoPath, gifPath);
    const reportPath = await writeReport({
      artifactDir,
      url: args.url,
      screenshotPath,
      videoPath: stableVideoPath,
      gifPath,
      gifCreated,
      scenarios,
    });

    console.log("Playwright max-adoption-fee-filter QA passed");
    console.log(`Screenshot: ${screenshotPath}`);
    console.log(`Video: ${stableVideoPath}`);
    console.log(gifCreated ? `GIF: ${gifPath}` : "GIF: not created (ffmpeg unavailable)");
    console.log(`Report: ${reportPath}`);
  } catch (error) {
    await page.screenshot({ path: path.join(artifactDir, "max-adoption-fee-filter-failure.png"), fullPage: true }).catch(() => {});
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
    throw error;
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
