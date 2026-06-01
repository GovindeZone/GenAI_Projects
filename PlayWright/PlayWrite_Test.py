from playwright.async_api import async_playwright
import asyncio
import pyautogui

async def main():

    async with async_playwright() as p:

        print("status: Starting Playwright Test")

        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        print("status: Browser Launched")

        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        )

        page = await context.new_page()

        await page.goto("https://www.bing.com", timeout=60000)

        await page.wait_for_selector("textarea[name='q']", timeout=15000)

        print("status: web")

        pyautogui.alert("Status: Search Process Started")

        await page.fill("textarea[name='q']", "Playwright Python test")

        await page.keyboard.press("Enter")

        await page.wait_for_load_state("networkidle")

        await page.wait_for_timeout(5000)

        pyautogui.alert("Status: Search Process Completed")

        await asyncio.sleep(300)

# ✅ THIS LINE WAS MISSING
asyncio.run(main())