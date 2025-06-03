from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

books = [
    {"title": "Survival 101", "category": "survivalowa", "price": 49.99, "amount": 10},
    {"title": "Kuchnia Polska", "category": "gotowanie", "price": 39.99, "amount": 5},
    {"title": "Góry i Wspinaczka", "category": "survivalowa", "price": 59.99, "amount": 2},
    {"title": "JavaScript dla Początkujących", "category": "informatyka", "price": 79.99, "amount": 7},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('scrape_url')
        print(f"Link do scrapowania: {url}")
        # Tu dodaj logikę scrapowania po URL
        return redirect(url_for('index'))

    sort = request.args.get('sort')
    category_filter = request.args.get('category', '').lower()

    filtered_books = [book for book in books if category_filter in book['category'].lower()]

    if sort == 'name-asc':
        filtered_books.sort(key=lambda x: x['title'])
    elif sort == 'name-desc':
        filtered_books.sort(key=lambda x: x['title'], reverse=True)
    elif sort == 'price-asc':
        filtered_books.sort(key=lambda x: x['price'])
    elif sort == 'price-desc':
        filtered_books.sort(key=lambda x: x['price'], reverse=True)
    elif sort == 'amount-asc':
        filtered_books.sort(key=lambda x: x['amount'])
    elif sort == 'amount-desc':
        filtered_books.sort(key=lambda x: x['amount'], reverse=True)

    return render_template('index.html', books=filtered_books)

if __name__ == '__main__':
    app.run(debug=True)