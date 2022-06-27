docker network create gw || true

docker run --rm \
  --net gw \
  --link gw-kongdb:gw-kongdb \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=gw-kongdb" \
  -e "KONG_PG_USER=kong" \
  -e "KONG_PG_PASSWORD=kong" \
  -e "KONG_CASSANDRA_CONTACT_POINTS=gw-kongdb" \
  kong kong migrations bootstrap
