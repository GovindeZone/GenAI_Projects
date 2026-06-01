from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
from automation_helpers import _get_title_from_card, _get_company_from_card, _get_job_id_from_card, _get_job_link, _get_location_from_card, _get_posted_date_from_card, _get_salary_from_card, _is_easy_apply, _scrape_detail_panel


SESSION_FILE = "linkedin_session.json"


def run_job_search(job_role: str, location: str, max_jobs: int = 15) -> dict:

    jobs_data = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            slow_mo=50      
        )

        context = browser.new_context(
            storage_state=SESSION_FILE,
            viewport={"width": 1400, "height": 900}
        )

        page = context.new_page()

        # Navigate
        search_url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={job_role}&location={location}"
        )
        print(f"\n🔍  Searching: {job_role} in {location}")
        page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        # Scroll to load all visible cards 
        print("Scrolling to load job cards...")
        for scroll_step in range(6):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(800)

        # Scroll back to top so we iterate from the first card
        page.keyboard.press("Control+Home")
        page.wait_for_timeout(1000)

        # Collect all job card list items 
        job_cards = page.locator("li[data-occludable-job-id]")
        total_found = job_cards.count()
        print(f"Found {total_found} job card slots")

        limit = min(total_found, max_jobs)
        seen_jobs: set = set()

        for i in range(total_found):

            if len(jobs_data) >= limit:
                break

            card = job_cards.nth(i)

            # Scroll card into view to unocclude it 
            try:
                card.scroll_into_view_if_needed(timeout=3000)
                page.wait_for_timeout(400)
            except Exception:
                pass

            # Extract list-card fields 
            try:
                title = _get_title_from_card(card)
                if not title:
                    print(f"  [card {i}] No title found, skipping")
                    continue

                company     = _get_company_from_card(card)
                location_   = _get_location_from_card(card)
                salary      = _get_salary_from_card(card)
                posted_date = _get_posted_date_from_card(card)
                easy_apply  = _is_easy_apply(card)
                job_link    = _get_job_link(card)
                job_id      = _get_job_id_from_card(card)

                unique_key = f"{title.lower()}-{company.lower()}"
                if unique_key in seen_jobs:
                    print(f"  [card {i}] Duplicate: {title} @ {company}")
                    continue
                seen_jobs.add(unique_key)

                print(f"  [{i+1}] {title} @ {company} | {location_}")

            except Exception as e:
                print(f"  [card {i}] Error reading card: {e}")
                continue

            # Click card to open detail panel 
            detail = {}
            try:
                # Click the title link (more reliable than clicking the whole card)
                link_el = card.locator("a.job-card-container__link").first
                if link_el.count() > 0:
                    link_el.click(timeout=5000)
                    page.wait_for_timeout(2000)
                    detail = _scrape_detail_panel(page)
            except Exception as e:
                print(f"      ⚠ Could not open detail panel: {e}")

            # Save record 
            record = {
                "Title":                title,
                "Company":              company,
                "Location":             location_,
                "Salary":               salary,
                "Work Type":            detail.get("Work Type", "Not Mentioned"),
                "Job Type":             detail.get("Job Type", "Not Mentioned"),
                "Posted Date":          posted_date,
                "Applicants":           detail.get("Applicants", "Not Mentioned"),
                "Easy Apply":           easy_apply,
                "Application Last Date":"Not Mentioned",
                "Company Industry":     detail.get("Company Industry", "Not Available"),
                "Company Size":         detail.get("Company Size", "Not Available"),
                "Job Description":      detail.get("Job Description", "Not Available"),
                "Job Link":             job_link,
                "Job ID":               job_id,
            }

            jobs_data.append(record)

        # Close browser 
        context.close()
        browser.close()

    # Save to Excel 
    df = pd.DataFrame(jobs_data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"jobs_{timestamp}.xlsx"

    # Column order
    col_order = [
        "Title", "Company", "Location", "Salary", "Work Type", "Job Type",
        "Posted Date", "Applicants", "Easy Apply", "Application Last Date",
        "Company Industry", "Company Size", "Job Description", "Job Link", "Job ID"
    ]
    df = df[[c for c in col_order if c in df.columns]]

    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Jobs")

        # Auto-size columns for readability
        ws = writer.sheets["Jobs"]
        for col_cells in ws.columns:
            max_len = max(
                (len(str(cell.value)) if cell.value else 0)
                for cell in col_cells
            )
            ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 4, 60)

    print(f"\n  Saved {len(jobs_data)} jobs → {file_name}")

    return {
        "message": f"{len(jobs_data)} LinkedIn jobs saved",
        "file_path": file_name,
        "jobs": [
            {k: v for k, v in r.items() if k != "Job Description"}
            for r in jobs_data
        ]
    }