docker build -t gateway/api3 .
docker rm -f gw-api3 || true
docker network create gw || true

docker run -d \
--net gw \
--name gw-api3 \
-p 5003:5000 \
gateway/api3
