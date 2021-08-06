FROM redis:latest
EXPOSE 6379
COPY redis-dump.csv /
COPY start-redis.sh /
CMD ["sh", "/start-redis.sh"]
