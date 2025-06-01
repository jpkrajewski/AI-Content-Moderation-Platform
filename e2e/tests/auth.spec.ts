import { test, expect } from '@playwright/test';

test('user can log in with valid credentials', async ({ page }) => {
  // Visit login page
  await page.goto('/login');

  // Fill in form fields
  await page.fill('input#email', 'admin@example.com');
  await page.fill('input#password', 'admin');

  // Submit form
  await page.click('button[type="submit"]');

  // Wait for navigation or dashboard content
  await page.waitForURL('**/secure/dashboard/summary');

  // Optional: assert something on the dashboard
  await expect(page).toHaveURL(/.*\/secure\/dashboard\/summary/);
});

test('user cannot access secured view without login', async ({ page }) => {
  await page.goto('/secure/dashboard/summary');

  // Expect to be redirected to login page
  await expect(page).toHaveURL(/.*\/login/);

  // Optional: assert presence of login form
  await expect(page.locator('input#email')).toBeVisible();
  await expect(page.locator('input#password')).toBeVisible();
});