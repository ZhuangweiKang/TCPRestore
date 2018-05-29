#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import utl
import  time
import Controller as controller
import DockerHelper as dHelper
import ZMQHelper as zmq

def main(worker_address, choice):
    publisher_container_name = 'Publisher'
    publisher_image = 'zhuangweikang/publisher'
    logger = utl.doLog('PubControllLogger', 'PubController.log')

    # init swarm environment, publisher host is manager node
    client = dHelper.setClient()
    advertise_addr = os.popen('ip addr show dev ens3 | grep inet | awk \'{print $2}\' | head -n 1', 'r').read()
    advertise_addr = advertise_addr.split('/')[0]
    dHelper.initSwarm(client, advertise_addr=advertise_addr)
    logger.info('Init Swarm environment. This is manager node.')

    # build overlay network
    network = 'kangNetwork'
    dHelper.createNetwork(client, name=network, subset='10.10.26.136/24')
    logger.info('Build overlay network: kangNetwork.')

    # send address and token to worker node, notify worker nodes to join the environment
    advertise_addr = advertise_addr + ':2377'
    join_token = dHelper.getJoinToken()

    socket= zmq.csConnect(worker_address, '3100')

    send_str = advertise_addr + ' ' + join_token
    socket.send_string(send_str)
    socket.recv_string()

    logger.info('Send manager address and join token to worker node.')

    time.sleep(5)

    logger.info('Start doing main activity.')

    if choice == 1:
        # build publisher container
        controller.executorSwarm()
    else:
        # build publisher container
        controller.executorSwarm()


if __name__ == '__main__':
    main()