#!/usr/bin/env python3
import os
import multiprocessing
import time
import redis
from scraper_worker import generate_all_page_urls, scrape_pages_chunk

# ==================== KONFIGURACJA REDISA ====================
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB   = int(os.getenv("REDIS_DB", 0))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def chunkify(lst: list, n: int) -> list[list]:
    """
    Dzieli listę lst na n niemal równolicznych kawałków.
    Zwraca listę n list.
    """
    if not lst:
        return []
    k, m = divmod(len(lst), n)
    return [
        lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
        for i in range(n)
    ]

if __name__ == "__main__":
    """
    Główny silnik scrapera:
    1. Łączy się do Redisa i w nieskończonej pętli wywołuje BLPOP na 'scrape_queue'.
    2. Gdy otrzyma URL (np. 'https://books.toscrape.com/catalogue/page-1.html'),
       generuje listę wszystkich stron listingowych (paginacji).
    3. Dzieli tę listę na kawałki wg liczby CPU.
    4. Uruchamia multiprocessing.Pool(...).map(scrape_pages_chunk, chunks), co
       w każdym procesie odpala asynchroniczne pobieranie stron i zapis do Redisa.
    5. Po skończeniu przechodzi od razu do następnego BLPOP i czeka na kolejny URL.
    """
    print("[Scraper Master] Startujemy. Oczekuję na URL-e w kolejce 'scrape_queue'...")

    while True:
        # BLPOP: czeka w nieskończoność, aż ktoś wrzuci URL do listy 'scrape_queue'
        item = redis_client.blpop("scrape_queue", timeout=0)
        if not item:
            # (teoretycznie nie nastąpi, bo timeout=0 → czeka do skutku)
            continue

        _, url_to_scrape = item
        url_to_scrape = url_to_scrape.decode("utf-8").strip()
        if not url_to_scrape:
            # pusta linia? pomijamy
            continue

        print(f"[Scraper Master] Otrzymałem URL do scrapowania: {url_to_scrape}")

        # 1. Wygeneruj listę wszystkich stron listingowych (paginacja)
        all_page_urls = generate_all_page_urls(url_to_scrape)
        num_pages = len(all_page_urls)
        print(f"[Scraper Master] Znaleziono {num_pages} stron listingowych do zeskrobania.")

        if num_pages == 0:
            print(f"[Scraper Master] Brak stron do zeskrobania lub błąd pobrania: {url_to_scrape}")
            # od razu powrót do BLPOP
            continue

        # 2. Oblicz liczbę procesów = liczba rdzeni CPU (możesz to zmienić)
        n_procs = multiprocessing.cpu_count()
        print(f"[Scraper Master] Użyję {n_procs} procesów do przetworzenia {num_pages} stron.")

        # 3. Podziel listę URL-i na n_proc kawałków
        chunks = chunkify(all_page_urls, n_procs)

        if not chunks:
            # pusta lista → nic do roboty, powrót do nasłuchiwania
            continue

        # 4. Uruchom pool procesów, każdy wywoła scrape_pages_chunk(...) na swoim fragmencie
        with multiprocessing.Pool(processes=n_procs) as pool:
            pool.map(scrape_pages_chunk, chunks)

        print(f"[Scraper Master] Scraping dla {url_to_scrape} zakończony.\n")
        # Pętla wraca do BLPOP – oczekujemy na kolejne URL-e
        time.sleep(1)  # krótka pauza przed następnym cyklem (opcjonalnie)
