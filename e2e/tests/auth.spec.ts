import { test, expect } from '@playwright/test';

test('user can log in with valid credentials', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input#email', 'admin@example.com');
  await page.fill('input#password', 'admin');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/secure/dashboard/summary');
  await expect(page).toHaveURL(/.*\/secure\/dashboard\/summary/);
});

test('user cannot access secured view without login', async ({ page }) => {
  await page.goto('/secure/dashboard/summary');
  await expect(page).toHaveURL(/.*\/login/);
  await expect(page.locator('input#email')).toBeVisible();
  await expect(page.locator('input#password')).toBeVisible();
});