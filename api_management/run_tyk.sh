docker rm -f gw-tyk{{port1}} || true

docker run -d \
  --name gw-tyk{{port1}} \
  --network gw \
  --link redis:redis \
  -p {{port1}}:8080 \
  -v /mnt/c/Users/andon/Desktop/licenta/api_management/tyk.standalone.conf:/opt/tyk-gateway/tyk.conf \
  -v /mnt/c/Users/andon/Desktop/licenta/api_management/apps{{port1}}:/opt/tyk-gateway/apps \
  docker.tyk.io/tyk-gateway/tyk-gateway:latest