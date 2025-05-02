"""
extactor.py

This module contains functions to extract data from a webpage using the Playwright Library.
It uses BeautifulSoup to parse the HTML content and extract the title and content of the page.
`extract_data_from_page` function is used to extract the title and content from a given page URL.
`extract_links` function is used to extract all the links from a giver page.

It uses the Playwright library to navigate to the page and extract the HTML content.
It also uses the BeautifulSoup library to parse the HTML content and extract the title and content of the page.
"""

from bs4 import BeautifulSoup

import logging
import random
import asyncio


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


async def extract_data_from_page(url, page):
    """Extract title and content from a given page URL."""
    try:
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(random.uniform(3, 6))

        try:
            await page.wait_for_selector("div.texto-integral, div.content, div.artigo", timeout=8000)
        except:
            logging.warning(f"The content may not have loaded correctly: {url}")

        page_html = await page.content()
        soup = BeautifulSoup(page_html, "html.parser")

        title_div = soup.find("h1")
        content_div = soup.find("div", class_="content")

        title = title_div.get_text(strip=True) if title_div else "Title not Found"

        content = None
        possible_selectors = ["div.texto-integral", "div.content", "div.artigo", "div.corpo"]

        for selector in possible_selectors:
            element =soup.select_one(selector)
            if element:
                content = element.get_text("\n", strip=True)
                break # Stop as the first valid match
        
        if not content:
            content = "Content not Found"

        # DEBUG: Temporary print to chech the page's HTML
        logging.debug(f"URL: {url} | Title: {title} | Content Sample: {content[:500]}")

        extraction = {
            "url": url,
            "title": title,
            "content": content,
        }

        return extraction

    except Exception as e:
        logging.error(f"Error extracting data from page {url}: {e}")
        return None


async def extract_links(page):
    """Extract links from the page."""
    try:
        await asyncio.sleep(random.uniform(1, 3))

        containers = page.locator("div.list.list-group.OSFillParent")
        links = []

        count = await containers.count()

        for index in range(count):
            container = containers.nth(index)
            container_html = await container.inner_html()
            soup = BeautifulSoup(container_html, "html.parser")

            # Extract links and remove Duplicated
            new_links = {a['href'] for a in soup.find_all("a", href=True)}
            links.extend(new_links)
        
        return list(set(links))

    except Exception as e:
        logging.error(f"Error extracting links: {e}")
        return []