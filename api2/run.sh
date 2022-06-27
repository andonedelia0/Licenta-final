docker build -t gateway/api2 .
docker rm -f gw-api2 || true
docker network create gw || true

docker run -d \
--net gw \
--name gw-api2 \
-p 5002:5000 \
gateway/api2
