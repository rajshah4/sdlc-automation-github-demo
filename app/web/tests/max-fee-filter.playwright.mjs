#!/usr/bin/env node
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
      "/tmp/sdlc-petstore-playwright/max-fee-filter",
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
    console.error("Install it outside the timed automation run, or set NODE_PATH to an existing node_modules directory.");
    console.error(`Original error: ${error.message}`);
    process.exit(2);
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

async function visiblePetNames(page) {
  return page.locator("#results .pet strong").allTextContents();
}

async function assertNames(page, expected, scenario) {
  const actual = await visiblePetNames(page);
  assert(
    JSON.stringify(actual) === JSON.stringify(expected),
    `${scenario}: expected ${expected.join(", ") || "no pets"}, got ${actual.join(", ") || "no pets"}`,
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
  const lines = [
    "# Playwright QA Report: Maximum Adoption Fee Filter",
    "",
    "Status: pass",
    "",
    "## Target",
    "",
    `- URL: ${url}`,
    "- App: static Petstore web UI",
    "- Feature: KAN-119 maximum adoption fee filter",
    "",
    "## Browser Scenarios",
    "",
    ...scenarios.map((scenario) => `- [x] ${scenario}`),
    "",
    "## Artifacts",
    "",
    `- Screenshot: ${path.basename(screenshotPath)}`,
    `- Video: ${path.basename(videoPath)}`,
    gifCreated ? `- GIF preview: ${path.basename(gifPath)}` : "- GIF preview: not created because ffmpeg was unavailable",
    "",
    "## Commands",
    "",
    "```bash",
    "python3 skills/sdlc-qa/scripts/with_server.py \\",
    "  --server \"python3 -m http.server 4173 --directory app/web\" \\",
    "  --port 4173 \\",
    "  -- node app/web/tests/max-fee-filter.playwright.mjs \\",
    "     --url http://localhost:4173 \\",
    "     --artifact-dir /tmp/sdlc-petstore-playwright/max-fee-filter",
    "```",
    "",
    "## Notes",
    "",
    "- This test validates the maximum adoption fee filter (KAN-119).",
    "- Test data: Mochi ($75), Pip ($45), Scout ($125), Nova ($110, pending).",
    "- UI converts dollars to cents for backend filtering.",
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
    
    // Verify max fee input is visible
    const maxFeeInput = page.getByLabel("Max Adoption Fee");
    await maxFeeInput.waitFor();
    assert(await maxFeeInput.isVisible(), "Max Adoption Fee input should be visible");
    scenarios.push("Max Adoption Fee input field is visible in search form");

    // Scenario 1: No filter (baseline)
    await assertNames(page, ["Mochi", "Scout", "Pip"], "default no filter");
    scenarios.push("Without max fee filter, all available pets are shown (Mochi $75, Scout $125, Pip $45)");

    // Scenario 2: Filter by $100 - should show Mochi ($75) and Pip ($45), exclude Scout ($125)
    await maxFeeInput.fill("100");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Pip"], "max fee $100");
    scenarios.push("Max fee $100 includes Mochi ($75) and Pip ($45), excludes Scout ($125)");

    // Scenario 3: Filter by $75 (exact boundary) - should include Mochi at exactly $75
    await maxFeeInput.fill("75");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Pip"], "max fee $75 boundary");
    scenarios.push("Max fee $75 includes Mochi at exact boundary ($75) and Pip ($45)");

    // Scenario 4: Filter by $50 - should show only Pip ($45)
    await maxFeeInput.fill("50");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Pip"], "max fee $50");
    scenarios.push("Max fee $50 shows only Pip ($45), excludes higher-priced pets");

    // Scenario 5: Clear filter - should show all pets again
    await maxFeeInput.clear();
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Scout", "Pip"], "cleared filter");
    scenarios.push("Clearing max fee filter restores all available pets");

    // Scenario 6: Combine with species filter
    await page.getByLabel("Species").selectOption("dog");
    await maxFeeInput.fill("120");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await page.locator("#results .empty").waitFor();
    const emptyText = await page.locator("#results .empty").textContent();
    assert(emptyText === "No available pets match this search.", "dog under $120 should show empty");
    scenarios.push("Combined filters work: dog species + max fee $120 shows empty (Scout is $125)");

    // Take final screenshot showing the max fee input
    await page.getByLabel("Species").selectOption("");
    await maxFeeInput.clear();
    await maxFeeInput.fill("75");
    await page.getByRole("button", { name: "Find Pets" }).click();
    const screenshotPath = path.join(artifactDir, "max-fee-filter.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });

    await context.close();
    await browser.close();

    const capturedVideoPath = await video.path();
    const stableVideoPath = path.join(artifactDir, "max-fee-filter.webm");
    await fs.copyFile(capturedVideoPath, stableVideoPath);
    await fs.rm(videosDir, { recursive: true, force: true }).catch(() => {});

    const gifPath = path.join(artifactDir, "max-fee-filter.gif");
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

    console.log("Playwright UI QA passed");
    console.log(`Screenshot: ${screenshotPath}`);
    console.log(`Video: ${stableVideoPath}`);
    console.log(gifCreated ? `GIF: ${gifPath}` : "GIF: not created");
    console.log(`Report: ${reportPath}`);
  } catch (error) {
    await page.screenshot({ path: path.join(artifactDir, "max-fee-filter-failure.png"), fullPage: true }).catch(() => {});
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
    throw error;
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
