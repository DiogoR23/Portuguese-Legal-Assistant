from playwright.sync_api import sync_playwright
import logging
from scraper.extractor import extract_data_from_page, extract_links
from scraper.storage import save_data_to_cassandra

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def crawl_site(start_url, base_url, session):
    """Crawl the site starting from the start_url and save the data to Cassandra."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        visited = set()
        to_visit = [start_url]

        while to_visit:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue

            visited.add(current_url)
            data = extract_data_from_page(current_url, page)
            if data:
                save_data_to_cassandra(session, [data])

            page.goto(current_url)
            page.wait_for_timeout(5000)
            new_links = extract_links(page) 
            full_links = [base_url + link if link.startswith('/') else link for link in new_links]

            for link in full_links:
                if link not in visited:
                    to_visit.append(link)

        browser.close()

