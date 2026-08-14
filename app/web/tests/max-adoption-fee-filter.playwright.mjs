#!/usr/bin/env node
/**
 * Focused Playwright QA for the max adoption fee filter (issue #88).
 *
 * Covers:
 *   1. Below-threshold filter: $80 limit → Mochi ($75) and Pip ($45) visible; Scout ($125) hidden
 *   2. Exact-boundary: max fee exactly $75 → Mochi included (inclusive), Scout excluded, Pip included
 *   3. Below-all: max fee $10 → empty state message
 *   4. Clear fee: removing the limit restores all three available pets
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
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--url") {
      args.url = argv[++i];
    } else if (arg === "--artifact-dir") {
      args.artifactDir = argv[++i];
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return args;
}

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    console.error("Playwright is not available in this runtime.");
    console.error(
      "Set NODE_PATH to an existing node_modules directory that contains playwright.",
    );
    console.error(`Original error: ${error.message}`);
    process.exit(2);
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function visiblePetNames(page) {
  return page.locator("#results .pet strong").allTextContents();
}

async function assertNames(page, expected, scenario) {
  const actual = await visiblePetNames(page);
  assert(
    JSON.stringify(actual) === JSON.stringify(expected),
    `${scenario}: expected [${expected.join(", ") || "none"}], got [${actual.join(", ") || "none"}]`,
  );
}

async function convertVideoToGif(videoPath, gifPath) {
  try {
    await execFileAsync("ffmpeg", [
      "-y", "-i", videoPath,
      "-vf", "fps=8,scale=960:-1:flags=lanczos",
      gifPath,
    ]);
    return true;
  } catch {
    return false;
  }
}

async function writeReport({ artifactDir, url, screenshotPaths, videoPath, gifPath, gifCreated, scenarios }) {
  const reportPath = path.join(artifactDir, "qa-report.md");
  const lines = [
    "# Playwright QA Report: Max Adoption Fee Filter",
    "",
    "Status: pass",
    "",
    "## Target",
    "",
    `- URL: ${url}`,
    "- Feature: issue #88 — filter pets by max adoption fee",
    "",
    "## Scenarios",
    "",
    ...scenarios.map((s) => `- [x] ${s}`),
    "",
    "## Screenshots",
    "",
    ...screenshotPaths.map((p) => `- ${path.basename(p)}`),
    "",
    "## Video",
    "",
    `- ${path.basename(videoPath)}`,
    gifCreated ? `- GIF preview: ${path.basename(gifPath)}` : "- GIF: not created (ffmpeg unavailable)",
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
  const screenshotPaths = [];

  try {
    await page.goto(args.url);
    await page.getByRole("heading", { name: "Petstore SDLC Demo" }).waitFor();

    // Baseline: all three available pets visible before any fee filter
    await assertNames(page, ["Mochi", "Scout", "Pip"], "baseline");
    scenarios.push("Baseline shows all three available pets before fee filter");

    // Scenario 1: below-threshold filter — $80 limit keeps Mochi ($75) and Pip ($45), drops Scout ($125)
    await page.getByLabel("Max adoption fee ($)").fill("80");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Pip"], "below-threshold $80 filter");
    scenarios.push("Below-threshold $80 filter: Mochi and Pip shown, Scout hidden");

    const shot1 = path.join(artifactDir, "fee-below-threshold.png");
    await page.screenshot({ path: shot1, fullPage: true });
    screenshotPaths.push(shot1);

    // Scenario 2: exact-boundary — $75 limit must include Mochi (feeCents === maxFeeCents)
    await page.getByLabel("Max adoption fee ($)").fill("75");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Pip"], "exact-boundary $75 filter");
    scenarios.push("Exact-boundary $75: Mochi ($75 === limit, inclusive) and Pip ($45) shown; Scout ($125) excluded");

    const shot2 = path.join(artifactDir, "fee-exact-boundary.png");
    await page.screenshot({ path: shot2, fullPage: true });
    screenshotPaths.push(shot2);

    // Scenario 3: budget below all pets → empty state
    await page.getByLabel("Max adoption fee ($)").fill("10");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await page.locator("#results .empty").waitFor();
    const emptyText = await page.locator("#results .empty").textContent();
    assert(
      emptyText === "No available pets match this search.",
      `empty state message mismatch: "${emptyText}"`,
    );
    scenarios.push("Budget below all pets ($10) shows empty-state message");

    // Scenario 4: clearing fee restores all available pets
    await page.getByLabel("Max adoption fee ($)").fill("");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Scout", "Pip"], "fee cleared");
    scenarios.push("Clearing max fee input restores all three available pets");

    const shot3 = path.join(artifactDir, "fee-cleared.png");
    await page.screenshot({ path: shot3, fullPage: true });
    screenshotPaths.push(shot3);

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
      screenshotPaths,
      videoPath: stableVideoPath,
      gifPath,
      gifCreated,
      scenarios,
    });

    console.log("Max adoption fee Playwright QA passed");
    for (const p of screenshotPaths) console.log(`Screenshot: ${p}`);
    console.log(`Video: ${stableVideoPath}`);
    console.log(gifCreated ? `GIF: ${gifPath}` : "GIF: not created");
    console.log(`Report: ${reportPath}`);
  } catch (error) {
    const failShot = path.join(artifactDir, "failure.png");
    await page.screenshot({ path: failShot, fullPage: true }).catch(() => {});
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
    throw error;
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
