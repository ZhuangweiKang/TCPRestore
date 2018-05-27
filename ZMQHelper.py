#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang


import zmq


def connect(address, port):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    connect_str = 'tcp://%s:%s' % (address, port)
    socket.connect(connect_str)
    return socket


def subscribeTopic(socket, topic):
    socket.subscribe(topic)


def unsubscribeTopic(socket, topic):
    socket.unsubscribe(topic)


def bind(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://*:%s' % port)
    return socket