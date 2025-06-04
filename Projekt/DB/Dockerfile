# BD/Dockerfile
FROM redis:6.2-alpine

# Kopiujemy własny plik konfiguracyjny Redis
COPY redis.conf /usr/local/etc/redis/redis.conf

# Tworzymy katalog /data, gdzie Redis będzie zapisywał AOF / RDB
RUN mkdir -p /data && chown redis:redis /data

# Uruchamiamy Redis z naszą konfiguracją
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
