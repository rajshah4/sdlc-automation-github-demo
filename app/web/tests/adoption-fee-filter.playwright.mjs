#!/usr/bin/env node
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { existsSync } from "node:fs";
import { mkdir, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const baseUrl = process.env.PETSTORE_UI_URL ?? "http://127.0.0.1:4173";
const artifactDir = process.env.PLAYWRIGHT_ARTIFACT_DIR ?? "/tmp/sdlc-petstore-playwright";
const browserChannel = process.env.PLAYWRIGHT_BROWSER_CHANNEL;
const videoDir = path.join(artifactDir, "videos");

async function petNames(page) {
  return page.locator("#results .pet strong").allTextContents();
}

async function assertPetNames(page, expected) {
  assert.deepEqual(await petNames(page), expected);
}

function commandExists(command) {
  return spawnSync("which", [command], { encoding: "utf8" }).status === 0;
}

async function latestFile(directory, extension) {
  if (!existsSync(directory)) {
    return null;
  }
  const entries = await readdir(directory, { withFileTypes: true });
  const files = entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(extension))
    .map((entry) => path.join(directory, entry.name));
  return files.at(-1) ?? null;
}

async function writeReport({ screenshotPath, videoPath, gifPath }) {
  const reportPath = path.join(artifactDir, "qa-report.md");
  const lines = [
    "# Petstore UI QA Report",
    "",
    "## Status",
    "",
    "PASS",
    "",
    "## Browser Scenarios",
    "",
    "- Default catalog shows Mochi, Scout, and Pip.",
    "- Pending pet Nova is not visible by default.",
    "- Max adoption fee `80` hides Scout and leaves Mochi/Pip visible.",
    "- Max adoption fee `40` shows the empty-state message.",
    "- Negative fee `-1` shows inline validation.",
    "",
    "## Artifacts",
    "",
    `- Screenshot: ${screenshotPath}`,
    videoPath ? `- Video: ${videoPath}` : "- Video: not captured",
    gifPath ? `- GIF: ${gifPath}` : "- GIF: not generated",
    "",
  ];
  await writeFile(reportPath, `${lines.join("\n")}\n`, "utf8");
  return reportPath;
}

await mkdir(videoDir, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  ...(browserChannel ? { channel: browserChannel } : {}),
});
const context = await browser.newContext({
  viewport: { width: 1280, height: 840 },
  recordVideo: { dir: videoDir, size: { width: 1280, height: 840 } },
});
const page = await context.newPage();

try {
  await page.goto(baseUrl);
  await page.getByRole("heading", { name: "Petstore SDLC Demo" }).waitFor();

  await assertPetNames(page, ["Mochi", "Scout", "Pip"]);
  assert.equal(await page.getByText("Nova").count(), 0, "pending pets should not appear by default");

  await page.getByLabel("Max adoption fee").fill("80");
  await page.getByRole("button", { name: "Find Pets" }).click();
  await assertPetNames(page, ["Mochi", "Pip"]);
  assert.equal(await page.getByText("Scout").count(), 0, "Scout should be hidden above the fee ceiling");

  await page.getByLabel("Max adoption fee").fill("40");
  await page.getByRole("button", { name: "Find Pets" }).click();
  await assertPetNames(page, []);
  await page.getByText("No available pets match this search.").waitFor();

  await page.getByLabel("Max adoption fee").fill("-1");
  await page.getByRole("button", { name: "Find Pets" }).click();
  await page.getByText("Enter a maximum fee of 0 or more.").waitFor();

  await mkdir(artifactDir, { recursive: true });
  const screenshotPath = path.join(artifactDir, "adoption-fee-filter.png");
  await page.screenshot({ path: screenshotPath, fullPage: true });
  await context.close();

  const videoPath = await latestFile(videoDir, ".webm");
  const gifPath = path.join(artifactDir, "adoption-fee-filter.gif");
  let generatedGifPath = null;
  if (videoPath && commandExists("ffmpeg")) {
    const result = spawnSync(
      "ffmpeg",
      ["-y", "-i", videoPath, "-vf", "fps=8,scale=960:-1:flags=lanczos", gifPath],
      { encoding: "utf8" },
    );
    if (result.status === 0) {
      generatedGifPath = gifPath;
    }
  }
  const reportPath = await writeReport({ screenshotPath, videoPath, gifPath: generatedGifPath });

  console.log("Playwright UI smoke passed");
  console.log(`Screenshot: ${screenshotPath}`);
  if (videoPath) {
    console.log(`Video: ${videoPath}`);
  }
  if (generatedGifPath) {
    console.log(`GIF: ${generatedGifPath}`);
  }
  console.log(`Report: ${reportPath}`);
} finally {
  if (!page.isClosed()) {
    await context.close();
  }
  await browser.close();
}
