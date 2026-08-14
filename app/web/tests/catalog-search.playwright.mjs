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
      "/tmp/sdlc-petstore-playwright/catalog-search",
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
    "# Playwright QA Report: Petstore Catalog Search",
    "",
    "Status: pass",
    "",
    "## Target",
    "",
    `- URL: ${url}`,
    "- App: static Petstore web UI",
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
    "  -- node app/web/tests/catalog-search.playwright.mjs \\",
    "     --url http://localhost:4173 \\",
    "     --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search",
    "```",
    "",
    "## Notes",
    "",
    "- This is the preferred browser-evidence path for UI-visible changes.",
    "- If Playwright is unavailable in a remote automation runtime, fall back to dependency-free checks and say so explicitly.",
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
    await assertNames(page, ["Mochi", "Scout", "Pip"], "default available-pets view");
    scenarios.push("Default catalog shows available pets and excludes pending pets");

    await page.getByLabel("Species").selectOption("dog");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Scout"], "species filter");
    scenarios.push("Species filter narrows results to available dogs");

    await page.getByLabel("Species").selectOption("");
    await page.getByLabel("Pet name").fill("pip");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Pip"], "name search");
    scenarios.push("Name search finds a matching available pet");

    const screenshotPath = path.join(artifactDir, "catalog-search.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });

    await page.getByLabel("Pet name").fill("nova");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await page.locator("#results .empty").waitFor();
    const emptyText = await page.locator("#results .empty").textContent();
    assert(emptyText === "No available pets match this search.", "pending pet search should show empty state");
    scenarios.push("Pending pet remains hidden and shows the empty state");

    // Max adoption fee filter: $100 keeps Mochi ($75) and Pip ($45), drops Scout ($125)
    await page.getByLabel("Pet name").fill("");
    await page.getByLabel("Max adoption fee ($)").fill("100");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Pip"], "max fee filter at $100");
    scenarios.push("Max adoption fee filter hides pets above budget");

    // Clearing the max fee field restores all available pets
    await page.getByLabel("Max adoption fee ($)").fill("");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertNames(page, ["Mochi", "Scout", "Pip"], "max fee cleared restores full list");
    scenarios.push("Clearing max fee input restores all available pets");

    await context.close();
    await browser.close();

    const capturedVideoPath = await video.path();
    const stableVideoPath = path.join(artifactDir, "catalog-search.webm");
    await fs.copyFile(capturedVideoPath, stableVideoPath);
    await fs.rm(videosDir, { recursive: true, force: true }).catch(() => {});

    const gifPath = path.join(artifactDir, "catalog-search.gif");
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
    await page.screenshot({ path: path.join(artifactDir, "catalog-search-failure.png"), fullPage: true }).catch(() => {});
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
    throw error;
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
