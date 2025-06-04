# Interfejs/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 1. Kopiujemy requirements i instalujemy Flask + Redis
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2. Kopiujemy cały kod interfejsu (app.py, templates/, static/)
COPY . .

# 3. Ustaw ENV do Redisa
ENV REDIS_HOST=redis-service
ENV REDIS_PORT=6379
ENV REDIS_DB=0

# 4. Ustawiamy dla Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]
