from playwright.sync_api import sync_playwright
from openpyxl import Workbook
import time

# Create Excel file
wb = Workbook()
ws = wb.active
ws.title = "Jobs"

# Header
ws.append(["Job Title", "Company", "Location", "Link"])

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Open jobs site
    page.goto("https://remoteok.com", timeout=60000)

    print("Status: Page opened")

    time.sleep(5)  # allow jobs to load

    # Locate job rows
    jobs = page.locator("tr.job")

    count = jobs.count()
    print(f"Total jobs found: {count}")

    for i in range(min(count, 20)):

        job = jobs.nth(i)

        try:
            title = job.locator("h2").inner_text()
        except:
            title = "N/A"

        try:
            company = job.locator("h3").inner_text()
        except:
            company = "N/A"

        try:
            location = job.locator(".location").inner_text()
        except:
            location = "Remote"

        try:
            link = job.locator("a").first.get_attribute("href")
            link = "https://remoteok.com" + link
        except:
            link = "N/A"

        # Write to Excel
        ws.append([title, company, location, link])

    # Save Excel file
    wb.save("jobs_output.xlsx")

    print("Status: Excel file created → jobs_output.xlsx")

    input("Press ENTER to close...")

    browser.close()