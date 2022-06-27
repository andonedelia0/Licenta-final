docker network create gw || true

docker rm -f gw-konga || true

docker run -d -p 1337:1337 \
  --network=gw \
  --name gw-konga \
  -v /var/data/kongadata:/app/kongadata \
  -e "NODE_ENV=production" \
  pantsel/konga

  # -v /var/data/kongadata:/app/kongadata \
