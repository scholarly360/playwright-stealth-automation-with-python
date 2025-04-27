
from playwright.sync_api import sync_playwright, Page
from bs4 import BeautifulSoup
import random

def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Clean HTML and extract visible text
def extract_clean_text(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted tags
    for tag in soup(['script', 'style', 'noscript', 'header', 'footer', 'svg']):
        tag.decompose()

    # Get text and strip extra whitespace
    text = soup.get_text(separator='\n')
    clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    return clean_text
    
# Main Playwright function
def browse_and_print(urls):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # Headless browsers are easier to detect
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent=random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 " +
                "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
            ]),
            viewport={"width": 1280, "height": 800},
            locale="en-US"
        )

        page =  context.new_page()

        # Stealth tweaks (navigator.webdriver, plugins, etc.)
        context.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
              get: () => [1, 2, 3]
            });
            Object.defineProperty(navigator, 'languages', {
              get: () => ['en-US', 'en']
            });
            """)

        for url in urls:
            print(f"\nVisiting: {url}")
            try:
                page.goto(url, timeout=20000)
                page.wait_for_timeout(random.randint(1000, 3000))  # simulate human reading time
                html = page.content()
                clean_text = extract_clean_text(html)
                print(clean_text[:1000])  # show part of content
            except Exception as e:
                print(f"Failed to open {url}: {e}")
                continue

        browser.close()