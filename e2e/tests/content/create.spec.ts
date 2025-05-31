import { test, expect } from '../fixtures';
import * as path from 'path';

test('should fill form and submit content', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/secure/content/submit');

  await authenticatedPage.fill('input[placeholder="Post title"]', 'Test Title');
  await authenticatedPage.fill('textarea[placeholder="Enter your content..."]', 'This is the test body.');
  await authenticatedPage.fill('input[placeholder="e.g., news, politics"]', 'news, test');
  await authenticatedPage.fill('input[placeholder="e.g., acme_corp"]', 'test_source');
  await authenticatedPage.selectOption('select', 'en');
  const imagePath = path.resolve(__dirname, '../fixtures/test-jpg.jpg');
  const [fileChooserImage] = await Promise.all([
    authenticatedPage.waitForEvent('filechooser'),
    authenticatedPage.click('text=Choose Images'),
  ]);
  await fileChooserImage.setFiles(imagePath);
  const docPath = path.resolve(__dirname, '../fixtures/test-doc.docx');
  const [fileChooserDoc] = await Promise.all([
    authenticatedPage.waitForEvent('filechooser'),
    authenticatedPage.click('text=Choose Documents'),
  ]);
  await fileChooserDoc.setFiles(docPath);
  await authenticatedPage.click('button[type="submit"]');
  await expect(authenticatedPage.locator('text=Content submitted successfully!')).toBeVisible();
});
