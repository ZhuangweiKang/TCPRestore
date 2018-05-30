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
    subscriber_container_name = 'Subscriber'
    subscriber_image = 'zhuangweikang/subscriber'
    logger = utl.doLog('SubControllLogger', 'SubController.log')
    network = 'kangNetwork'

    # join the swarm environment
    socket = zmq.csBind('3100')
    msg = socket.recv_string()
    advertise_addr = str(msg.split()[0].strip())
    join_token = str(msg.split()[1].strip())
    socket.send_string('Ack')

    client = dHelper.setClient()
    dHelper.joinSwarm(client, join_token, advertise_addr)

    logger.info('Worker node join the Swarm environment.')

    time.sleep(3)

    logger.info('Start doing main activity.')

    if choice == 1:
        # build subscriber container
        controller.executorSwarm(logger, subscriber_image, subscriber_container_name, network, False, worker_address, sSocket=socket)
    else:
        # build subscriber container
        controller.executorSwarm(logger, subscriber_image, subscriber_container_name, network, True, worker_address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--choice', type=int, default=1, help='1. Test Publisher, 2. Test Subscriber')
    args = parser.parse_args()
    choice = args.choice
    main('129.59.107.138', choice)

