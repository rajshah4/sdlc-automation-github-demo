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
      "/tmp/sdlc-petstore-playwright/catalog-count",
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

async function getCountText(page) {
  return page.locator("#count").textContent();
}

async function assertCount(page, expected, scenario) {
  const actual = await getCountText(page);
  assert(
    actual === expected,
    `${scenario}: expected "${expected}", got "${actual}"`,
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
    "# Playwright QA Report: Petstore Catalog Count",
    "",
    "Status: pass",
    "",
    "## Target",
    "",
    `- URL: ${url}`,
    "- App: static Petstore web UI",
    "- Feature: Available pet count display (KAN-120)",
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
    "  -- node app/web/tests/catalog-count.playwright.mjs \\",
    "     --url http://localhost:4173 \\",
    "     --artifact-dir /tmp/sdlc-petstore-playwright/catalog-count",
    "```",
    "",
    "## Notes",
    "",
    "- Tests the count display added in PR #116 (KAN-120)",
    "- Verifies count updates with filters and handles singular/plural correctly",
    "- Confirms pending pets are excluded from available count",
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
    
    await assertCount(page, "3 pets available", "default available count");
    scenarios.push("Default catalog shows count of 3 available pets");

    await page.getByLabel("Species").selectOption("dog");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertCount(page, "1 pet available", "species filter count with singular");
    scenarios.push("Count updates to 1 pet (singular) when filtering by species");

    await page.getByLabel("Species").selectOption("cat");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertCount(page, "1 pet available", "cat species count");
    scenarios.push("Count shows 1 available cat (Mochi)");

    await page.getByLabel("Species").selectOption("");
    await page.getByLabel("Pet name").fill("Mochi");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertCount(page, "1 pet available", "name search count");
    scenarios.push("Count updates correctly with name search");

    await page.getByLabel("Pet name").fill("");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertCount(page, "3 pets available", "reset to all available count with plural");
    scenarios.push("Count returns to 3 pets (plural) after clearing filters");

    await page.getByLabel("Pet name").fill("nova");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertCount(page, "0 pets available", "pending pet excluded from count");
    scenarios.push("Count shows 0 when searching for pending pet (Nova)");

    await page.getByLabel("Pet name").fill("nonexistent");
    await page.getByRole("button", { name: "Find Pets" }).click();
    await assertCount(page, "0 pets available", "zero count for no matches");
    scenarios.push("Count shows 0 for non-existent pet name");

    const screenshotPath = path.join(artifactDir, "catalog-count.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });

    await context.close();
    await browser.close();

    const capturedVideoPath = await video.path();
    const stableVideoPath = path.join(artifactDir, "catalog-count.webm");
    await fs.copyFile(capturedVideoPath, stableVideoPath);
    await fs.rm(videosDir, { recursive: true, force: true }).catch(() => {});

    const gifPath = path.join(artifactDir, "catalog-count.gif");
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
    await page.screenshot({ path: path.join(artifactDir, "catalog-count-failure.png"), fullPage: true }).catch(() => {});
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
    throw error;
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
