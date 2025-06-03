# scraper_worker.py

#!/usr/bin/env python3
import re
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup

# ================= SCRAPING FUNKCJE ====================

def get_books_links(page_url, base_url=None):
    """
    Pobiera wszystkie linki do książek znajdujące się na stronie katalogu.
    - page_url: pełny URL strony np. https://books.toscrape.com/catalogue/page-1.html
    - base_url: podstawowy URL dla łączenia (np. https://books.toscrape.com/catalogue/)
      Jeśli nie podano, próbuje wywnioskować z page_url.
    Zwraca listę pełnych URLi do podstron z pojedynczymi książkami.
    """
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = []
    # jeśli base_url nie podano, wyciągamy z page_url
    if not base_url:
        # np. https://books.toscrape.com/catalogue/page-1.html -> https://books.toscrape.com/catalogue/
        parts = page_url.split('/')[:-1]
        base_url = '/'.join(parts) + '/'

    for a in soup.select('h3 a'):
        href = a['href'].replace('../../../', '')
        links.append(f"{base_url}{href}")
    return links

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_book(session, url):
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('h1').text
    price = soup.select_one('.price_color').text

    raw_availability = soup.select_one('.instock.availability').text.strip()
    match = re.search(r'(\d+)', raw_availability)
    if match:
        availability = int(match.group(1))
    else:
        availability = 0

    category = soup.select('ul.breadcrumb li')[2].text.strip()
    img_relative_url = soup.select_one('.item.active img')['src']
    # Budujemy pełny URL obrazka z książki:
    if img_relative_url.startswith('http'):
        image_url = img_relative_url
    else:
        # Zakładamy, że podajemy zawsze base_url zawierający katalog główny, np. https://books.toscrape.com/catalogue/
        base = '/'.join(url.split('/')[:-3]) + '/'
        image_url = base + img_relative_url.replace('../../', '')

    return {
        'title': title,
        'price': price,
        'availability': availability,
        'category': category,
        'image_url': image_url
    }

async def scrape_page(session, page_url, base_url=None):
    """
    Pobiera wszystkie linki książek z danej strony, a następnie asynchronicznie scrapuje każdą książkę.
    Zwraca listę słowników z danymi książek.
    """
    links = get_books_links(page_url, base_url)
    tasks = [scrape_book(session, url) for url in links]
    books = await asyncio.gather(*tasks)
    return books

def scrape_page_books(page_url):
    """
    Funkcja wykonywana przez multiprocessing.Pool.
    Tworzy event loop asyncio, otwiera sesję i wywołuje scrape_page.
    Zwraca listę książek (słowników).
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def wrapper():
        async with aiohttp.ClientSession() as session:
            return await scrape_page(session, page_url)
    result = loop.run_until_complete(wrapper())
    loop.close()
    return result

def get_all_pages(base_url):
    """
    Generuje listę wszystkich stron katalogu do scrapowania:
    - base_url: np. "https://books.toscrape.com/catalogue/"
    Zwraca listę URLi typu:
      https://books.toscrape.com/catalogue/page-1.html,
      https://books.toscrape.com/catalogue/page-2.html, ...
    """
    first_page = base_url.rstrip('/') + '/page-1.html'
    resp = requests.get(first_page)
    soup = BeautifulSoup(resp.text, 'html.parser')
    total_text = soup.select_one('.current').text.strip()  # np. "Page 1 of 50"
    total_pages = int(total_text.split()[-1])
    pages = [first_page]
    for i in range(2, total_pages + 1):
        pages.append(base_url.rstrip('/') + f'/page-{i}.html')
    return pages
