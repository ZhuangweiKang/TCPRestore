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

def csConnect(address, port):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    connect_str = 'tcp://%s:%s' % (address, port)
    socket.connect(connect_str)
    return socket

def subscribeTopic(socket, topic):
    topicfilter = topic
    socket.setsockopt(zmq.SUBSCRIBE, topicfilter)


def unsubscribeTopic(socket, topic):
    socket.unsubscribe(topic)

def csBind(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:%s' % port)
    return socket

def bind(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://*:%s' % port)
    return socket