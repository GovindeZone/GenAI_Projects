from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime
import time
import os


def scrape_website(url):

    try:
        with sync_playwright() as p:

            # ---------------------------------------------------
            # Launch Browser
            # ---------------------------------------------------
            browser = p.chromium.launch(
                headless=False,
                slow_mo=200,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            # ---------------------------------------------------
            # Create Browser Context
            # ---------------------------------------------------
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1400, "height": 900}
            )

            # Remove automation detection
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # Open Page
            page = context.new_page()

            # ---------------------------------------------------
            # Increase Timeouts
            # ---------------------------------------------------
            page.set_default_timeout(120000)
            page.set_default_navigation_timeout(120000)
            

            print(f"\nOpening Website: {url}")

            # ---------------------------------------------------
            # Retry Logic
            # ---------------------------------------------------
            max_retries = 3

            for attempt in range(max_retries):

                try:

                    print(f"\nAttempt: {attempt + 1}")

                    # Open Website
                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=120000
                    )

                    # Additional wait
                    page.wait_for_timeout(5000)

                    # Scroll slowly to trigger lazy loading
                    page.mouse.wheel(0, 3000)

                    # Wait again
                    page.wait_for_timeout(3000)

                    print("Website Loaded Successfully")

                    break

                except TimeoutError:

                    print("Timeout occurred... Retrying")

                    if attempt == max_retries - 1:
                        raise Exception("Page load failed after retries")

            # ---------------------------------------------------
            # Extract Title
            # ---------------------------------------------------
            try:
                title = page.title()
            except:
                title = "Title Not Found"

            print(f"\nTitle: {title}")

            # ---------------------------------------------------
            # Extract Meta Tags
            # ---------------------------------------------------
            metadata = []

            try:

                meta_tags = page.locator("meta")

                count = meta_tags.count()

                print(f"\nMeta Tags Found: {count}")

                for i in range(count):

                    try:
                        meta = meta_tags.nth(i)

                        metadata.append({
                            "name": meta.get_attribute("name"),
                            "property": meta.get_attribute("property"),
                            "content": meta.get_attribute("content"),
                            "charset": meta.get_attribute("charset")
                        })

                    except Exception as meta_error:
                        print(f"Meta Tag Error: {meta_error}")

            except Exception as e:
                print(f"Meta Extraction Error: {e}")

            # ---------------------------------------------------
            # Extract Body Content
            # ---------------------------------------------------
            try:

                body_content = page.locator("body").inner_text()

            except Exception as e:

                print(f"Body Extraction Error: {e}")

                body_content = "Body Content Not Available"

            # ---------------------------------------------------
            # Create Output Folder
            # ---------------------------------------------------
            output_folder = "output"

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # ---------------------------------------------------
            # Create Output File
            # ---------------------------------------------------
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            filename = f"{output_folder}/amazon_data_{timestamp}.txt"

            # ---------------------------------------------------
            # Save Data
            # ---------------------------------------------------
            with open(filename, "w", encoding="utf-8") as file:

                file.write("=" * 80 + "\n")
                file.write("WEBSITE SCRAPING REPORT\n")
                file.write("=" * 80 + "\n\n")

                file.write(f"URL: {url}\n")
                file.write(f"TITLE: {title}\n")
                file.write(f"SCRAPED TIME: {datetime.now()}\n\n")

                # Metadata
                file.write("=" * 80 + "\n")
                file.write("META DATA INFORMATION\n")
                file.write("=" * 80 + "\n\n")

                for idx, meta in enumerate(metadata, start=1):

                    file.write(f"\nMeta Tag #{idx}\n")
                    file.write(f"Name      : {meta['name']}\n")
                    file.write(f"Property  : {meta['property']}\n")
                    file.write(f"Content   : {meta['content']}\n")
                    file.write(f"Charset   : {meta['charset']}\n")
                    file.write("-" * 50 + "\n")

                # Body Content
                file.write("\n\n")
                file.write("=" * 80 + "\n")
                file.write("BODY CONTENT\n")
                file.write("=" * 80 + "\n\n")

                file.write(body_content)

            print(f"\nData Saved Successfully")
            print(f"File: {filename}")

            # ---------------------------------------------------
            # Close Browser
            # ---------------------------------------------------
            browser.close()

    except Exception as e:

        print(f"\nMain Error: {e}")


# ---------------------------------------------------
# Main Function
# ---------------------------------------------------
if __name__ == "__main__":

    url = "https://www.amazon.in/Apple-Bluetooth-Headphones-Personalised-Effortless/dp/B0DGJLL7V1/ref=s9_acsd_al_ot_c2_x_0_t?_encoding=UTF8&pf_rd_m=A21TJRUUN4KGV&pf_rd_s=merchandised-search-19&pf_rd_r=B5VR89DSTNMSNNPQXJRS&pf_rd_p=a576b225-f734-43c9-b385-867639276c0e&pf_rd_t=&pf_rd_i=78382736031"

    scrape_website(url)