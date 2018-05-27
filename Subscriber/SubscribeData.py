#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import logging
import ZMQHelper as zmq


address = '129.59.107.138'
port = '3000'

def main():
    logger = doLog()
    socket = zmq.connect(address, port)
    zmq.subscribeTopic(socket, 'number')
    while True:
        data = socket.recv()
        number = data.split()
        logger.info(number)

def doLog():
    logger = logging.getLogger('SubLogger')
    logger.setLevel(logging.DEBUG)

    fl = logging.FileHandler('Sub.log')
    fl.setLevel(logging.DEBUG)

    cl = logging.StreamHandler()
    cl.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fl.setFormatter(formatter)
    cl.setFormatter(formatter)

    logger.addHandler(fl)
    logger.addHandler(cl)

    return logger