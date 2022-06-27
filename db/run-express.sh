docker network create gw || true

docker rm -f mongo-express || true
docker run -d --name mongo-express \
  --network gw \
  --link mongodb:mongodb \
  -e "ME_CONFIG_BASICAUTH_USERNAME=mongo" \
  -e "ME_CONFIG_BASICAUTH_PASSWORD=mongo" \
  -e "ME_CONFIG_MONGODB_SERVER=mongodb" \
  -p 8081:8081 \
  mongo-express:0.54.0
