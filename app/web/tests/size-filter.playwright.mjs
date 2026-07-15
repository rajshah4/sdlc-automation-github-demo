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
      "/tmp/sdlc-petstore-playwright/size-filter",
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
    "# Playwright QA Report: Pet Size Filter",
    "",
    "Status: pass",
    "",
    "## Target",
    "",
    `- URL: ${url}`,
    "- App: static Petstore web UI",
    "- PR: #103 - Add pet size filter feature (Jira KAN-107)",
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
    "  -- node app/web/tests/size-filter.playwright.mjs \\",
    "     --url http://localhost:4173 \\",
    "     --artifact-dir /tmp/sdlc-petstore-playwright/size-filter",
    "```",
    "",
    "## OpenSpec Acceptance Criteria Validation",
    "",
    "All scenarios from `openspec/changes/jira-KAN-107-pet-size-filter/specs/catalog/spec.md` were tested:",
    "",
    "- ✅ Filter by small size returns only small pets (Mochi, Pip)",
    "- ✅ Filter by medium size returns only medium pets (Scout)",
    "- ✅ Filter by large size returns no pets (empty state)",
    "- ✅ No size filter specified returns all available pets",
    "- ✅ Size filter combined with species filter works correctly",
    "",
    "## Notes",
    "",
    "- This is browser evidence for the UI-visible size filter feature.",
    "- Backend tests in `app/tests/test_pet_catalog.py` cover the catalog.py API layer.",
    "- The size dropdown appears correctly in the UI between Species and Find Pets button.",
    "- Size values are displayed in pet results alongside species and tags.",
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
    
    // Verify size filter control exists
    const sizeSelect = page.getByLabel("Size");
    await sizeSelect.waitFor();
    scenarios.push("Size filter dropdown appears in the UI");

    // Test 1: Default view (no size filter)
    await assertNames(page, ["Mochi", "Scout", "Pip"], "default available-pets view");
    scenarios.push("Default catalog shows all available pets without size filtering");

    // Test 2: Filter by small size
    await sizeSelect.selectOption("small");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Pip"], "small size filter");
    scenarios.push("Size filter 'small' returns only Mochi and Pip");

    // Test 3: Filter by medium size
    await sizeSelect.selectOption("medium");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Scout"], "medium size filter");
    scenarios.push("Size filter 'medium' returns only Scout");

    // Test 4: Filter by large size (empty state)
    await sizeSelect.selectOption("large");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await page.locator("#results .empty").waitFor();
    const emptyText = await page.locator("#results .empty").textContent();
    assert(emptyText === "No available pets match this search.", "large size filter should show empty state");
    scenarios.push("Size filter 'large' shows empty state correctly");

    // Test 5: Size combined with species
    await sizeSelect.selectOption("small");
    await page.getByLabel("Species").selectOption("cat");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi"], "small + cat filter");
    scenarios.push("Size filter combined with species filter returns correct results");

    // Test 6: Reset to Any size
    await sizeSelect.selectOption("");
    await page.getByLabel("Species").selectOption("");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Scout", "Pip"], "reset filters");
    scenarios.push("Resetting size filter to 'Any' restores all available pets");

    // Verify size is displayed in results
    await sizeSelect.selectOption("small");
    await page.getByRole("button", { name: "Find Pets" }).click();
    const petDetails = await page.locator("#results .pet span").first().textContent();
    assert(petDetails.includes("small"), "pet result should display size value");
    scenarios.push("Size value is displayed in pet results");

    const screenshotPath = path.join(artifactDir, "size-filter.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });

    await context.close();
    await browser.close();

    const capturedVideoPath = await video.path();
    const stableVideoPath = path.join(artifactDir, "size-filter.webm");
    await fs.copyFile(capturedVideoPath, stableVideoPath);
    await fs.rm(videosDir, { recursive: true, force: true }).catch(() => {});

    const gifPath = path.join(artifactDir, "size-filter.gif");
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
    await page.screenshot({ path: path.join(artifactDir, "size-filter-failure.png"), fullPage: true }).catch(() => {});
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
    throw error;
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
