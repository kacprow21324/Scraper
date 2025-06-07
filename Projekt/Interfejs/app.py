from flask import Flask, render_template, request, redirect, url_for
import os
import json
import redis

app = Flask(__name__)

# Konfiguracja Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('scrape_url')
        if url:
            redis_client.rpush("scrape_queue", url)
        return redirect(url_for('index'))

    # Pobieramy wszystkie książki
    all_keys = redis_client.lrange("books_list", 0, -1)
    books = []
    for raw_key in all_keys:
        key = raw_key.decode("utf-8")
        raw_data = redis_client.get(key)
        if not raw_data:
            continue
        entry = json.loads(raw_data)
        title = entry.get("title", "brak")
        price = float(entry.get("price", "0"))
        availability = entry.get("availability", "")
        amount = 0
        if "(" in availability and ")" in availability:
            try:
                inside = availability.split("(")[1].split(")")[0]
                amount = int(inside.split()[0])
            except:
                amount = 0
        category = entry.get("category", "nieznana")
        image_url = entry.get("image_url", "")

        books.append({
            "title": title,
            "category": category,
            "price": price,
            "amount": amount,
            "image_url": image_url,
            "redis_key": key
        })

    # POBIERANIE PARAMETRÓW Z URLA
    sort = request.args.get("sort", "")
    category_filter = request.args.get("category", "").lower()
    search_query = request.args.get("search", "").lower()

    # FILTROWANIE
    filtered = books
    if category_filter:
        filtered = [b for b in filtered if category_filter in b["category"].lower()]
    if search_query:
        filtered = [b for b in filtered if search_query in b["title"].lower()]

    # SORTOWANIE
    if sort == "name-asc":
        filtered.sort(key=lambda x: x["title"])
    elif sort == "name-desc":
        filtered.sort(key=lambda x: x["title"], reverse=True)
    elif sort == "price-asc":
        filtered.sort(key=lambda x: x["price"])
    elif sort == "price-desc":
        filtered.sort(key=lambda x: x["price"], reverse=True)
    elif sort == "amount-asc":
        filtered.sort(key=lambda x: x["amount"])
    elif sort == "amount-desc":
        filtered.sort(key=lambda x: x["amount"], reverse=True)

    # PRZEKAZUJEMY TEŻ LICZNIK
    return render_template("index.html", books=filtered, total=len(filtered))

# === TRASA USUWANIA ===
@app.route('/delete', methods=['POST'])
def delete_book():
    key_to_delete = request.form.get("key")

    # Przechwycenie parametrów filtrów
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    sort = request.args.get("sort", "")

    if key_to_delete:
        redis_client.delete(key_to_delete)
        redis_client.lrem("books_list", 0, key_to_delete)

    # Przekierowanie z powrotem z tymi samymi parametrami
    return redirect(url_for('index', search=search, category=category, sort=sort))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
