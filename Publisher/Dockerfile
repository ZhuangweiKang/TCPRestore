FROM python:3

WORKDIR /usr/src/app

RUN pip3 install --default-timeout=1000 pyzmq

COPY ./ZMQHelper.py ./
COPY ./Publisher/PublishData.py ./

CMD ["python", "./PublishData.py"]

EXPOSE 3000