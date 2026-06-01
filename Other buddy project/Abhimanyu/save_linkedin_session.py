from playwright.sync_api import sync_playwright

SESSION_FILE = "linkedin_session.json"

with sync_playwright() as p:

    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://www.linkedin.com/login")

    print("Log in manually in browser...")

    input("After successful login press ENTER here...")

    context.storage_state(path=SESSION_FILE)

    print(f"Session saved successfully to {SESSION_FILE}")

    browser.close()