import { test as base } from '@playwright/test';

export const test = base.extend<{
  authenticatedPage: any;
}>({
  authenticatedPage: async ({ page }, use) => {
  await page.goto('/login');
  await page.fill('input#email', 'admin@example.com');
  await page.fill('input#password', 'admin');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/secure/dashboard/summary');
  await use(page);
},
    });

export { expect } from '@playwright/test';

