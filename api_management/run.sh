docker build -t api_management .
docker rm -f api_management || true
docker network create gw || true

docker run -d \
--net gw \
--link mongodb:mongodb \
--name api_management \
-p 5008:5000 \
-v /mnt/c/Users/andon/AppData/Roaming/SPB_16.6/.minikube/ca.crt:/opt/app/ca.crt \
-v /mnt/c/Users/andon/AppData/Roaming/SPB_16.6/.minikube/profiles/minikube/client.crt:/opt/app/client.crt \
-v /mnt/c/Users/andon/AppData/Roaming/SPB_16.6/.minikube/profiles/minikube/client.key:/opt/app/client.key \
-v /var/run/docker.sock:/var/run/docker.sock \
--add-host kubernetes:192.168.65.2 \
api_management
