docker rm -f gw-tyk || true
docker network create gw || true

docker run -d \
  --name gw-tyk \
  --network gw \
  --link redis:redis \
  -p 8080:8080 \
  -v $(pwd)/tyk.standalone.conf:/opt/tyk-gateway/tyk.conf \
  -v $(pwd)/apps:/opt/tyk-gateway/apps \
  docker.tyk.io/tyk-gateway/tyk-gateway:latest