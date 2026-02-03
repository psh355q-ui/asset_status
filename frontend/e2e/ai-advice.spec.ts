import { test, expect } from '@playwright/test';

test.describe('AI Advice Feature', () => {
    test.beforeEach(async ({ page }) => {
        // Login
        await page.goto('/login');
        await page.fill('input[name="email"]', 'test@example.com');
        await page.fill('input[name="password"]', 'Password123!');
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    });

    test('should navigate to AI advice page', async ({ page }) => {
        // Click AI Advice button
        await page.click('button:has-text("AI Advice")');

        // Should navigate to AI advice page
        await expect(page).toHaveURL('/ai-advice', { timeout: 10000 });
        await expect(page.locator('text=AI Investment Advice')).toBeVisible();
    });

    test('should request AI advice for a stock', async ({ page }) => {
        await page.goto('/ai-advice');

        // Wait for page to load
        await expect(page.locator('text=AI Investment Advice')).toBeVisible();

        // Enter stock symbol
        await page.fill('input[placeholder*="stock symbol"]', '005930.KS');

        // Click generate button
        await page.click('button:has-text("Get AI Advice")');

        // Wait for advice to be generated (may take several seconds)
        await page.waitForSelector('.advice-card', { timeout: 20000 });

        // Verify advice card appears
        await expect(page.locator('.advice-card')).toBeVisible();
        await expect(page.locator('text=005930.KS')).toBeVisible();
    });

    test('should display advice history', async ({ page }) => {
        await page.goto('/ai-advice');

        // Check if history section exists
        await expect(page.locator('text=Advice History')).toBeVisible();

        // Disclaimer should always be visible
        await expect(page.locator('text=참고용')).toBeVisible();
    });
});
