FROM python:3

WORKDIR /usr/src/app

RUN pip install pyzmq

COPY ./ZMQHelper.py ./
COPY ./Publisher/PublishData.py ./

CMD ["python", "./PublishData.py"]

EXPOSE 3000