FROM python:3.10.2

RUN pip install flask
RUN pip install flasgger

WORKDIR /opt/app
COPY . /opt/app/

ENTRYPOINT ["python3", "./server.py"]
