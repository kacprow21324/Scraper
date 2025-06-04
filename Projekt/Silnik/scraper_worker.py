#!/usr/bin/env python3
import os
import json
import asyncio
import aiohttp
import redis
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ==================== KONFIGURACJA REDISA ====================
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB   = int(os.getenv("REDIS_DB", 0))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# ==================== FUNKCJE ASYNC DO POBIERANIA ====================
async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                return await response.text()
            else:
                return ""
    except Exception:
        return ""

def parse_listing_page(html: str, base_url: str) -> list[str]:
    detail_urls = []
    if not html:
        return detail_urls
    soup = BeautifulSoup(html, "html.parser")
    pods = soup.select("article.product_pod h3 a")
    for a in pods:
        rel = a.get("href", "")
        full = urljoin(base_url, rel)
        detail_urls.append(full)
    return detail_urls

def parse_detail_page(html: str, detail_url: str) -> dict:
    if not html:
        return {}
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.select_one("div.product_main h1")
    title = title_tag.text.strip() if title_tag else "brak tytułu"

    price_tag = soup.select_one("p.price_color")
    price = price_tag.text.strip().lstrip("£") if price_tag else "0"

    avail_tag = soup.select_one("p.availability")
    availability = avail_tag.text.strip() if avail_tag else "Unavailable"

    category = "nieznana"
    bread = soup.select("ul.breadcrumb li a")
    if len(bread) >= 3:
        category = bread[2].text.strip()

    img_tag = soup.select_one("div.carousel-inner img")
    if img_tag and img_tag.get("src"):
        image_url = urljoin(detail_url, img_tag["src"])
    else:
        image_url = ""

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "category": category,
        "image_url": image_url
    }

def save_to_redis(book_data: dict):
    if not book_data or "title" not in book_data:
        return
    key = f"book:{book_data['title']}"
    redis_client.set(key, json.dumps(book_data))
    redis_client.lpush("books_list", key)

async def process_pages_async(page_urls: list[str]) -> None:
    sem = asyncio.Semaphore(20)

    async def bound_fetch(session: aiohttp.ClientSession, url: str) -> str:
        async with sem:
            return await fetch(session, url)

    async with aiohttp.ClientSession() as session:
        listing_tasks = [bound_fetch(session, url) for url in page_urls]
        listing_htmls = await asyncio.gather(*listing_tasks)

        detail_urls = []
        for html, base_url in zip(listing_htmls, page_urls):
            detail_urls.extend(parse_listing_page(html, base_url))

        detail_tasks = [bound_fetch(session, url) for url in detail_urls]
        detail_htmls = await asyncio.gather(*detail_tasks)

        for html, detail_url in zip(detail_htmls, detail_urls):
            data = parse_detail_page(html, detail_url)
            save_to_redis(data)

def scrape_pages_chunk(page_urls: list[str]) -> None:
    try:
        asyncio.run(process_pages_async(page_urls))
    except Exception as e:
        print(f"[Scraper Worker] Błąd w procesie przy chunk {page_urls[:1]}: {e}")

def generate_all_page_urls(base_first_page: str) -> list[str]:
    import requests
    from bs4 import BeautifulSoup

    urls = []
    current = base_first_page
    while current:
        urls.append(current)
        try:
            resp = requests.get(current, timeout=20)
        except Exception as e:
            print(f"[Paginator] Błąd pobierania {current}: {e}")
            break
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        next_btn = soup.select_one(".next a")
        if next_btn and next_btn.get("href"):
            current = urljoin(current, next_btn["href"])
        else:
            current = None
    return urls
