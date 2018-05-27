FROM python:3

WORKDIR /usr/src/app

RUN pip install pyzmq

COPY ./ZMQHelper.py ./
COPY /Subscriber/SubscribeData.py ./

CMD ['python', './SubscribeData.py']

