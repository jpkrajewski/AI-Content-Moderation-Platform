import { test, expect } from '../fixtures';
import * as path from 'path';

test('should fill form and submit content with images, videos, audios, and documents', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/secure/content/submit');

  await authenticatedPage.fill('input[placeholder="Post title"]', 'Test Title');
  await authenticatedPage.fill('textarea[placeholder="Enter your content..."]', 'This is the test body.');
  await authenticatedPage.fill('input[placeholder="e.g., news, politics"]', 'news, test');
  await authenticatedPage.fill('input[placeholder="e.g., acme_corp"]', 'test_source');
  await authenticatedPage.selectOption('select', 'en');

  // Upload image
  const imagePath = path.resolve(__dirname, '../fixtures/test-jpg.jpg');
  const [fileChooserImage] = await Promise.all([
    authenticatedPage.waitForEvent('filechooser'),
    authenticatedPage.click('text=Choose Images'),
  ]);
  await fileChooserImage.setFiles(imagePath);

  // Upload video
  const videoPath = path.resolve(__dirname, '../fixtures/test-mp4.mp4');
  const [fileChooserVideo] = await Promise.all([
    authenticatedPage.waitForEvent('filechooser'),
    authenticatedPage.click('text=Choose Videos'),
  ]);
  await fileChooserVideo.setFiles(videoPath);

  // Upload audio
  const audioPath = path.resolve(__dirname, '../fixtures/test-audio.wav');
  const [fileChooserAudio] = await Promise.all([
    authenticatedPage.waitForEvent('filechooser'),
    authenticatedPage.click('text=Choose Audios'),
  ]);
  await fileChooserAudio.setFiles(audioPath);

  // Upload document
  const docPath = path.resolve(__dirname, '../fixtures/test-doc.docx');
  const [fileChooserDoc] = await Promise.all([
    authenticatedPage.waitForEvent('filechooser'),
    authenticatedPage.click('text=Choose Documents'),
  ]);
  await fileChooserDoc.setFiles(docPath);

  await authenticatedPage.click('button[type="submit"]');
  await expect(authenticatedPage.locator('text=Content submitted successfully!')).toBeVisible();
});
