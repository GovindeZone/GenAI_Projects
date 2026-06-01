from playwright.sync_api import sync_playwright
import time
import random
import pyautogui

output_file = "amazon_products.txt"

with sync_playwright() as p:

    # ✅ Use REAL Chrome profile (VERY IMPORTANT)
    context = p.chromium.launch_persistent_context(
        user_data_dir="C:/Users/Swedh/AppData/Local/Google/Chrome/User Data",
        headless=False,
        slow_mo=300,
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = context.new_page()

    # Open Amazon mobiles page
    page.goto(
        "https://www.amazon.in/mobile-phones/b/?ie=UTF8&node=1389401031",
        timeout=60000
    )

    print("Status: Page opened")

    # ✅ Human-like delay
    time.sleep(random.uniform(4, 7))

    # ✅ Small mouse movement (anti-bot)
    page.mouse.move(300, 400)
    time.sleep(random.uniform(2, 4))

    # ✅ Scroll slowly like human
    for _ in range(6):
        page.mouse.wheel(0, 3000)
        time.sleep(random.uniform(2, 4))

    # ✅ Locate products
    items = page.locator("div.s-main-slot div[data-component-type='s-search-result']")
    count = items.count()

    print(f"Total products found: {count}")

    with open(output_file, "w", encoding="utf-8") as f:

        if count == 0:
            f.write("No products found (still blocked or layout changed)\n")
            pyautogui.alert("No products found (Amazon still blocking)")
        else:
            for i in range(min(count, 10)):

                item = items.nth(i)

                try:
                    name = item.locator("h2 span").inner_text(timeout=5000)
                except:
                    name = "N/A"

                try:
                    price = item.locator("span.a-price-whole").first.inner_text(timeout=5000)
                except:
                    price = "N/A"

                try:
                    link = item.locator("h2 a").get_attribute("href")
                    link = "https://www.amazon.in" + link
                except:
                    link = "N/A"

                f.write(f"Product {i+1}\n")
                f.write(f"Name  : {name}\n")
                f.write(f"Price : {price}\n")
                f.write(f"Link  : {link}\n")
                f.write("-" * 50 + "\n")

            pyautogui.alert("Completed: Data saved successfully")

    print("Status: Process completed")

    # ✅ Controlled exit (no freezing)
    input("Press ENTER to close browser...")

    context.close()