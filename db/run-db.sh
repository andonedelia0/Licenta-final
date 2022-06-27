docker network create gw || true

docker rm -f mongodb || true
docker run -d -p 27018:27017 \
  --name mongodb \
  --network gw \
  -e "MONGO_INITDB_ROOT_USERNAME: mongo" \
  -e "MONGO_INITDB_ROOT_PASSWORD: mongo" \
  -v /my/own/datadir:/data/db \
  mongo
