import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
    test('should register a new user', async ({ page }) => {
        await page.goto('/register');

        // Wait for page to load
        await expect(page.locator('h2:has-text("회원가입")')).toBeVisible();

        // Fill registration form
        const timestamp = Date.now();
        await page.fill('input[name="email"]', `test${timestamp}@example.com`);
        await page.fill('input[name="password"]', 'Password123!');
        await page.fill('input[name="confirmPassword"]', 'Password123!');

        // Submit form and handle alert
        page.on('dialog', dialog => dialog.accept());
        await page.click('button[type="submit"]');

        // Should redirect to login after successful registration
        await expect(page).toHaveURL('/login', { timeout: 10000 });
    });

    test('should login with existing user', async ({ page }) => {
        await page.goto('/login');

        // Wait for login page
        await expect(page.locator('h2:has-text("로그인")')).toBeVisible();

        // Fill login form
        await page.fill('input[name="email"]', 'test@example.com');
        await page.fill('input[name="password"]', 'Password123!');

        // Submit
        await page.click('button[type="submit"]');

        // Should redirect to dashboard
        await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
        await expect(page.locator('text=Asset Overview')).toBeVisible();
    });

    test('should logout successfully', async ({ page }) => {
        // Login first
        await page.goto('/login');
        await page.fill('input[name="email"]', 'test@example.com');
        await page.fill('input[name="password"]', 'Password123!');
        await page.click('button[type="submit"]');

        // Wait for dashboard
        await expect(page).toHaveURL('/dashboard', { timeout: 10000 });

        // Find and click logout button (last btn-secondary)
        const logoutBtn = page.locator('button.btn-secondary').last();
        await logoutBtn.click();

        // Should redirect to login
        await expect(page).toHaveURL('/login', { timeout: 10000 });
    });
});
