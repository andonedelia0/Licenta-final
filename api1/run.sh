docker build -t gateway/api1 .
docker rm -f gw-api1 || true
docker network create gw || true

docker run -d \
--net gw \
--name gw-api1 \
-p 5001:5000 \
gateway/api1
