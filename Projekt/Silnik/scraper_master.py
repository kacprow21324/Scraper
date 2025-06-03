import os
import json
import argparse
import redis
from multiprocessing import Pool, cpu_count
from scraper_worker import get_all_pages, scrape_page_books

# ================= KONFIGURACJA REDISA =================
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB   = int(os.getenv('REDIS_DB', 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# ================= ZAPIS DO REDISA ====================
def save_to_redis(book_data):
    """
    book_data to słownik:
    {
      'title': "...",
      'price': "£51.77",
      'availability': 3,
      'category': "Science Fiction",
      'image_url': "https://..."
    }
    Zapisujemy każdą książkę jako JSON pod kluczem np. "book:<unikalne_id>".
    """
    book_id = redis_client.incr("book_id_counter")
    key = f"book:{book_id}"
    redis_client.set(key, json.dumps(book_data, ensure_ascii=False))
    redis_client.rpush("books_list", key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master scraper: dzieli pracę pomiędzy procesy.")
    parser.add_argument("--base-url", type=str, default="https://books.toscrape.com/catalogue/",
                        help="Podstawowy URL strony, np. https://books.toscrape.com/catalogue/")
    parser.add_argument("--pages", nargs="*", help="Lista manualna stron do scrapingu (jeśli podano, używamy tych zamiast generowania automatycznego)")
    args = parser.parse_args()

    # Jeśli użytkownik podał listę stron, używamy jej. W przeciwnym wypadku generujemy pełny katalog.
    if args.pages:
        all_pages = args.pages
    else:
        all_pages = get_all_pages(args.base_url)

    # Uruchamiamy pulę procesów równoległych
    with Pool(cpu_count()) as pool:
        # mapujemy funkcję scrape_page_books (zwraca listę książek dla każdej strony) na wszystkie strony
        results = pool.map(scrape_page_books, all_pages)

    # Spłaszczamy listę: każda strona -> lista książek
    all_books = [book for page_books in results for book in page_books]

    # Zapis do Redisa
    for book in all_books:
        save_to_redis(book)

    print(f"Całkowicie pobrano i zapisano do Redisa: {len(all_books)} książek.")
