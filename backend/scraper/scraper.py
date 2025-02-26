from playwright.async_api import async_playwright
import logging
from extractor import extract_data_from_page, extract_links

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def crawl_site(start_url, base_url, session):
    """Crawl the site starting from the start_url and save the data to Cassandra."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        visited = set()
        to_visit = [start_url]

        while to_visit:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue

            visited.add(current_url)
            data = await extract_data_from_page(current_url, page)
            if data:
                session.save_data([data])

            await page.goto(current_url)
            await page.wait_for_timeout(5000)
            new_links = await extract_links(page) 

            # Modificando o código para garantir que todos os links comecem com base_url
            full_links = [link if link.startswith(base_url) else base_url + link for link in new_links]

            for link in full_links:
                if link not in visited:
                    to_visit.append(link)

        await browser.close()