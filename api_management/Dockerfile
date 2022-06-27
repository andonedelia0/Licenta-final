FROM python:3.10.2

RUN pip install flask
RUN pip install pymongo
RUN pip install Flask-PyMongo
RUN pip install requests

RUN apt-get update 
RUN apt-get install docker.io -y

WORKDIR /opt/app
COPY . /opt/app/

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x kubectl

ENV KUBECONFIG /opt/app/config.yaml

ENTRYPOINT ["python3", "./server.py"]
