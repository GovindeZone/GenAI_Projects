from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Open demo form website
    page.goto("https://demoqa.com/text-box")

    # Fill form fields
    page.fill("#userName", "Test User")
    page.fill("#userEmail", "testuser@gmail.com")
    page.fill("#currentAddress", "Chennai, India")
    page.fill("#permanentAddress", "Tamil Nadu, India")

    # Click Submit button
    page.click("#submit")

    # Keep browser open to see result
    time.sleep(300)