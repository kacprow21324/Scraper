# Silnik/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 1. Skopiuj i zainstaluj zależności
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2. Skopiuj kod silnika (both scraper_worker.py i scraper_master.py)
COPY scraper_worker.py scraper_master.py ./

# 3. Ustaw zmienne środowiskowe do Redisa:
ENV REDIS_HOST=redis-service
ENV REDIS_PORT=6379
ENV REDIS_DB=0
# 4. Ustaw BASE_URL (domyślnie, możesz nadpisać w Kubernetesie)
ENV BASE_URL="https://books.toscrape.com/catalogue/page-1.html"

# 5. Uruchom „scraper_master.py”
CMD ["python", "scraper_master.py"]
