docker rm -f redis || true
docker network create gw || true

docker run -td \
--net gw \
--name redis \
-p 6379:6379 \
redis
