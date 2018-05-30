#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import utl
import  time
import random
import Controller as controller
import DockerHelper as dHelper
import ZMQHelper as zmqHelper


class Publisher:
    def __init__(self, name, image, network, subnet):
        self.host_addr = utl.getHostIP()

        self.name = name
        self.image = image

        self.network = network
        self.subnet = subnet

        self.logger = utl.doLog('PubControllLogger', 'PubController.log')
        self.dockerClient = dHelper.setClient()
        self.infoSocket = zmqHelper.bind('3100')

    def initSwarmEnv(self):
        dHelper.initSwarm(self.dockerClient, advertise_addr=self.host_addr)
        self.logger.info('Init Swarm environment. This is manager node.')

    def createOverlayNetwork(self):
        dHelper.createNetwork(self.dockerClient, name=self.network, driver='overlay', subnet=self.subnet)
        self.logger.info('Build overlay network: kangNetwork.')

    def notifyWorkerJoin(self):
        remote_addr = self.host_addr + ':2377'
        join_token = dHelper.getJoinToken()
        send_str = 'join-token %s %s' % (remote_addr, join_token)
        zmqHelper.publish(self.infoSocket, send_str)
        self.logger.info('Send manager address and join token to worker node.')

    def deleteOldContainer(self):
        if dHelper.checkContainer(self.dockerClient, self.name) is True:
            container = dHelper.getContainer(self.dockerClient, self.name)
            dHelper.deleteContainer(container)
            self.logger.info('Old container exists, deleting old container.')

    def pullImage(self):
        if dHelper.checkImage(self.dockerClient, self.image) is False:
            dHelper.pullImage(self.dockerClient, self.image)
            self.logger.info('Image doesn\'t exist, building image.')

    def runContainer(self):
        container = dHelper.runContainer(self.dockerClient, self.image, self.name, network=self.network)
        return container

    def publishContainerIP(self):
        containerIP = dHelper.getContainerIP(self.name)
        msg = 'container-ip %s' % containerIP
        zmqHelper.publish(self.infoSocket, msg)

    def publishImageInfo(self):
        msg = 'image %s' % self.image
        zmqHelper.publish(self.infoSocket, msg)

    def dumpContainer(self):
        checkpoint_name = 'checkpoint_' + str(random.randint(1, 100))
        tarName = checkpoint_name + '.tar'
        dHelper.checkpoint(checkpoint_name, dHelper.getContainerID(self.name))


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
    dHelper.createNetwork(client, name=network, driver='overlay', subnet='10.10.26.136/24')
    logger.info('Build overlay network: kangNetwork.')

    # send host address and token to worker node, notify worker nodes to join the environment
    advertise_addr = advertise_addr + ':2377'
    join_token = dHelper.getJoinToken()

    socket= zmq.csConnect(worker_address, '3100')
    send_str = advertise_addr + ' ' + join_token
    socket.send_string(send_str)
    socket.recv_string()

    logger.info('Send manager address and join token to worker node.')

    time.sleep(3)

    logger.info('Start doing main activity.')

    if choice == 1:
        # build publisher container
        controller.executorSwarm(logger, publisher_image, publisher_container_name, network, True, worker_address)
    else:
        # build publisher container
        controller.executorSwarm(logger, publisher_image, publisher_container_name, network, False, worker_address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--choice', type=int, default=1, help='1. Test Publisher, 2. Test Subscriber')
    args = parser.parse_args()
    choice = args.choice
    main('129.59.107.139', choice)