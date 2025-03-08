from extractor import extract_data_from_page, extract_links

from playwright.async_api import async_playwright

import logging
import random
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEADLESS_MODE = True # Don't see the Browser while running main
MAX_RETRIES = 3 # Number of attempts in case of error

async def crawl_site(start_url, base_url, session):
    """Crawl the site starting from the start_url and save the data to Cassandra."""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS_MODE)
        page = await browser.new_page()

        # Simulate a real user
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
        })

        visited = set()
        to_visit = [start_url]

        while to_visit:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue

            visited.add(current_url)

            # Retry logic to avoid failures on some pages
            for attempt in range(MAX_RETRIES):
                try:
                    logging.info(f"Visiting: {current_url} (Attempt {attempt + 1}/{MAX_RETRIES})")
                    data = await extract_data_from_page(current_url, page)
                    if data:
                        session.save_data([data])
                    break # If the exctraction is a success, break the attempt loop 

                except Exception as e:
                    logging.warning(f"Error extracting {current_url}: {e}")
                    await asyncio.sleep(random.uniform(5, 10)) # Short break before the new attempt.

            await asyncio.sleep(random.uniform(2, 5)) # Random delay to avoid blocking

            new_links = await extract_links(page)
            full_links = {link if link.startswith(base_url) else base_url + link for link in new_links}

            for link in full_links:
                if link not in visited:
                    to_visit.append(link)

        await browser.close()