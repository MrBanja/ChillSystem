cd ../ && \
mkdir redis && \
mv app/Dockerfile_redis redis/Dockerfile && \
touch redis/redis.conf && \
mv app/docker-compose.yml .
