FROM python:3

WORKDIR /usr/src/app

RUN pip install pyzmq

COPY ../ZMQHelper.py ./
COPY SubscribeData.py ./

CMD ['python', './SubscribeData.py']

