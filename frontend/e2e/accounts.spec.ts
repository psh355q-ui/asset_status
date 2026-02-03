import { test, expect } from '@playwright/test';

test.describe('Account Management', () => {
    test.beforeEach(async ({ page }) => {
        // Login before each test
        await page.goto('/login');
        await page.fill('input[name="email"]', 'test@example.com');
        await page.fill('input[name="password"]', 'Password123!');
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    });

    test('should create a new account', async ({ page }) => {
        // Click "Add Account" button
        await page.click('button:has-text("Add Account")');

        // Wait for modal to appear
        await page.waitForSelector('.modal', { timeout: 5000 });

        // Fill account form
        await page.fill('input[name="name"]', 'Test Brokerage Account');
        await page.selectOption('select[name="broker"]', 'KB증권');
        await page.selectOption('select[name="account_type"]', 'STOCK');

        // Submit
        await page.click('.modal button[type="submit"]');

        // Wait for modal to close and account to appear
        await page.waitForSelector('text=Test Brokerage Account', { timeout: 10000 });
    });

    test('should add a transaction', async ({ page }) => {
        // Assume at least one account exists
        await page.click('button:has-text("Add Transaction")');

        // Wait for modal
        await page.waitForSelector('.modal', { timeout: 5000 });

        // Fill transaction form
        await page.selectOption('select[name="account_id"]', { index: 0 });
        await page.fill('input[name="symbol"]', '005930.KS');
        await page.selectOption('select[name="transaction_type"]', 'BUY');
        await page.fill('input[name="quantity"]', '10');
        await page.fill('input[name="price"]', '70000');
        await page.fill('input[name="transaction_date"]', '2024-01-15');

        // Submit
        await page.click('.modal button[type="submit"]');

        // Wait for modal to close
        await page.waitForSelector('.modal', { state: 'hidden', timeout: 10000 });
    });
});
