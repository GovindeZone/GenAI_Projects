from playwright.sync_api import TimeoutError as PlaywrightTimeout
import re

def _clean(text: str) -> str:
    """Strip whitespace, collapse inner spaces, remove zero-width chars."""
    if not text:
        return ""
    text = text.replace("\u200b", "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def _safe_text(locator, timeout: int = 3000) -> str:
    """Return text_content or '' on any error."""
    try:
        if locator.count() == 0:
            return ""
        val = locator.first.text_content(timeout=timeout)
        return _clean(val or "")
    except Exception:
        return ""


def _safe_attr(locator, attr: str, timeout: int = 3000) -> str:
    """Return attribute value or '' on any error."""
    try:
        if locator.count() == 0:
            return ""
        val = locator.first.get_attribute(attr, timeout=timeout)
        return (val or "").strip()
    except Exception:
        return ""


def _get_title_from_card(card) -> str:
    """
    Extract job title from job card.

    Primary  : aria-label on the <a class="job-card-container__link">
               e.g. "GenAI Python Developer"
               Note: aria-label may say "…with verification" — strip that suffix.
    Fallback : <strong> inside the link (text_content is noisy but workable).
    """
    link = card.locator("a.job-card-container__link").first
    if link.count() == 0:
        return ""

    # aria-label is the cleanest source
    aria = _safe_attr(link, "aria-label")
    if aria:
        aria = re.sub(r"\s+with verification\s*$", "", aria, flags=re.IGNORECASE)
        return _clean(aria)

    # fallback: <strong> text
    strong = card.locator("a.job-card-container__link strong").first
    text = _safe_text(strong)
    return text


def _get_company_from_card(card) -> str:
    """
    Company name is inside:
      .artdeco-entity-lockup__subtitle span   (class like koVkgGSR…)
    """
    # The outer subtitle div → first span child
    locator = card.locator(".artdeco-entity-lockup__subtitle span")
    return _safe_text(locator) or "Not Available"


def _get_location_from_card(card) -> str:
    """
    Location lives in .artdeco-entity-lockup__caption ul li span
    (class motaTUQO…).
    There may be two metadata-wrappers on a card (location + salary row).
    The first one is always location.
    """
    locator = card.locator(".artdeco-entity-lockup__caption .job-card-container__metadata-wrapper li span")
    return _safe_text(locator) or "Not Available"


def _get_salary_from_card(card) -> str:
    """
    Salary row is in .artdeco-entity-lockup__metadata ul li span
    (only present on some cards, e.g. "$50/hr - $75/hr").
    """
    locator = card.locator(".artdeco-entity-lockup__metadata .job-card-container__metadata-wrapper li span")
    return _safe_text(locator) or "Not Mentioned"


def _get_posted_date_from_card(card) -> str:
    """
    Posted date is inside <time datetime="…"> in the footer.
    Many cards show 'Promoted' instead – those return 'Not Available'.
    """
    time_loc = card.locator("time")
    text = _safe_text(time_loc)
    if text:
        # Remove the visually-hidden sub-text e.g. "Within the past 24 hours"
        text = text.split("\n")[0].strip()
        return text
    return "Not Available"


def _is_easy_apply(card) -> str:
    """Check if the footer contains 'Easy Apply'."""
    locator = card.locator(
        ".job-card-list__footer-wrapper span[dir='ltr']"
    )
    count = locator.count()
    for i in range(count):
        try:
            txt = _clean(locator.nth(i).text_content(timeout=1000))
            if "easy apply" in txt.lower():
                return "Yes"
        except Exception:
            pass
    return "No"


def _get_job_link(card) -> str:
    """
    Build the job URL from the href on the card's title link.
    href is like /jobs/view/4411311481/?…
    """
    link = card.locator("a.job-card-container__link").first
    href = _safe_attr(link, "href")
    if href:
        if href.startswith("http"):
            return href
        return "https://www.linkedin.com" + href
    return "Not Available"


def _get_job_id_from_card(card) -> str:
    """Extract job ID from data-job-id attribute on the inner container div."""
    container = card.locator("div[data-job-id]").first
    return _safe_attr(container, "data-job-id") or ""

def _scrape_detail_panel(page) -> dict:
    """
    After clicking a job card the right-hand detail panel loads.
    Returns a dict with extra fields extracted from that panel.

    Structure observed in After_click_a_job_card.txt:
      - Title      : h1.t-24 inside .job-details-jobs-unified-top-card__job-title
      - Location   : .job-details-jobs-unified-top-card__sticky-header .t-14.truncate  (fallback)
      - Work type  : .job-details-fit-level-preferences button span  (Remote / Hybrid / On-site)
      - Job type   : same row                                         (Full-time / Part-time …)
      - Applicants : .job-details-jobs-unified-top-card__tertiary-description-container span
      - Apply type : button#jobs-apply-button-id text (Easy Apply / Apply)
      - Description: #job-details full text
      - Company industry + size : .jobs-company .t-14 mt5
    """
    detail = {
        "Work Type": "Not Mentioned",
        "Job Type": "Not Mentioned",
        "Applicants": "Not Mentioned",
        "Job Description": "Not Available",
        "Company Industry": "Not Available",
        "Company Size": "Not Available",
    }

    try:
        # Wait for detail panel to appear
        page.wait_for_selector(
            ".jobs-search__job-details--container",
            timeout=8000
        )
    except PlaywrightTimeout:
        return detail

    # Work Type & Job Type (Remote/Hybrid, Full-time etc.) 
    try:
        pref_buttons = page.locator(
            ".job-details-fit-level-preferences button span"
        )
        btn_count = pref_buttons.count()
        work_texts = []
        for i in range(btn_count):
            t = _clean(pref_buttons.nth(i).text_content(timeout=1000))
            if t:
                work_texts.append(t)

        if len(work_texts) >= 1:
            # First button is typically work-mode (Remote / Hybrid / On-site)
            detail["Work Type"] = work_texts[0]
        if len(work_texts) >= 2:
            # Second button is employment type (Full-time etc.)
            detail["Job Type"] = work_texts[1]
    except Exception:
        pass

    # Applicant count 
    try:
        desc_spans = page.locator(
            ".job-details-jobs-unified-top-card__tertiary-description-container span"
        )
        span_count = desc_spans.count()
        for i in range(span_count):
            t = _clean(desc_spans.nth(i).text_content(timeout=1000))
            if "applicant" in t.lower():
                detail["Applicants"] = t
                break
    except Exception:
        pass

    # Job Description 
    try:
        desc_elem = page.locator("#job-details").first
        if desc_elem.count() > 0:
            raw = desc_elem.text_content(timeout=5000) or ""
            detail["Job Description"] = _clean(raw)[:3000]  # cap at 3000 chars
    except Exception:
        pass

    # Company industry & size 
    try:
        company_info = page.locator(".jobs-company__box .t-14").first
        info_text = _safe_text(company_info, timeout=2000)
        if info_text:
            detail["Company Industry"] = info_text

        size_spans = page.locator(".jobs-company__inline-information")
        if size_spans.count() > 0:
            detail["Company Size"] = _clean(
                size_spans.first.text_content(timeout=1000) or ""
            )
    except Exception:
        pass

    return detail