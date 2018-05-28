FROM python:3

WORKDIR /usr/src/app

RUN pip install --default-timeout=100 pyzmq

COPY ../ZMQHelper.py ./
COPY ./SubscribeData.py ./

CMD ['python', './SubscribeData.py']

