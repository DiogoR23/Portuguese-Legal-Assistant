from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


async def extract_data_from_page(url, page):
    """Extract title and content from a given page URL."""
    try:
        await page.goto(url)
        await page.wait_for_timeout(5000)

        page_html = await page.content()
        soup = BeautifulSoup(page_html, 'html.parser')

        title = soup.find('h1').get_text(strip=True)
        content = soup.find('div', class_='content').get_text(strip=True)

        return {
            'url': url,
            'title': title,
            'content': content
        }
    except Exception as e:
        logging.error(f"Error extracting data from page {url}: {e}")
        return None


async def extract_links(page):
    """Extract links from the page."""
    try:
        containers = page.locator('div.list.list-group.OSFillParent')
        links = []

        count = await containers.count()

        for index in range(count):
            container = containers.nth(index)
            container_html = await container.inner_html()
            soup = BeautifulSoup(container_html, 'html.parser')

            links.extend([a.get('href') for a in soup.find_all('a', href=True)])

        return links

    except Exception as e:
        logging.error(f"Error extracting links: {e}")
        return []