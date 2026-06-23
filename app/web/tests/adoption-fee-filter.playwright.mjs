#!/usr/bin/env node
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const baseUrl = process.env.PETSTORE_UI_URL ?? "http://127.0.0.1:4173";
const artifactDir = process.env.PLAYWRIGHT_ARTIFACT_DIR ?? "/tmp/sdlc-petstore-playwright";
const browserChannel = process.env.PLAYWRIGHT_BROWSER_CHANNEL;

async function petNames(page) {
  return page.locator("#results .pet strong").allTextContents();
}

async function assertPetNames(page, expected) {
  assert.deepEqual(await petNames(page), expected);
}

const browser = await chromium.launch({
  headless: true,
  ...(browserChannel ? { channel: browserChannel } : {}),
});
const page = await browser.newPage({ viewport: { width: 1280, height: 840 } });

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

  console.log("Playwright UI smoke passed");
  console.log(`Screenshot: ${screenshotPath}`);
} finally {
  await browser.close();
}
