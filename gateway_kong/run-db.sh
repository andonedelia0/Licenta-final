docker network create gw || true

docker rm -f gw-kongdb || true
docker run -d --name gw-kongdb \
  --net gw \
  -e "POSTGRES_USER=kong" \
  -e "POSTGRES_DB=kong" \
  -e "POSTGRES_PASSWORD=kong" \
  -p 5432:5432 \
  -v /tmp/postgres-data:/var/lib/postgresql/data \
  postgres:9.6
