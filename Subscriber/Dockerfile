FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common nano
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install pyzmq

COPY ./ZMQHelper.py ./
COPY ./Subscriber/SubscribeData.py ./

CMD ['python', './SubscribeData.py']

