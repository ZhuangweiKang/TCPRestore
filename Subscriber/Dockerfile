FROM python:3

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 pyzmq

COPY ./ZMQHelper.py ./
COPY ./Subscriber/SubscribeData.py ./

CMD ['python', './SubscribeData.py']

