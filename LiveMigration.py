#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import utl
import random
import time
import DockerHelper as dHelper
import ZMQHelper as zmqHelper


def executor(image, containerName, doDump=False):

    # create docker client
    client = dHelper.setClient()

    print('Checking if container exists...')

    # check container if exists
    if dHelper.checkContainer(client, containerName) is True:
        container = dHelper.getContainer(client, containerName)
        dHelper.deleteContainer(container)
        print('Old container exists, deleting old container...')

    # check if image exists
    if dHelper.checkImage(client, image) is False:
        dHelper.pullImage(client, image)

    print('Image doesn\'t exist, building image...')

    # Run a container
    container = dHelper.runContainer(client, image, containerName)

    print('Creat and run a container...')

    if doDump:
        print('\n-------------------\nWaiting 30 seconds...')

        time.sleep(30)

        # checkpoint the container
        checkpoint_name = 'checkpoint_' + str(random.randint(1, 100))
        dHelper.checkpoint(checkpoint_name, dHelper.getContainerID(container))

        print('\n-------------------\nWaiting for 20 seconds...')
        time.sleep(20)

        # restore the container
        checkpoint_dir = '/var/lib/docker/containers/%s/checkpoints/' % dHelper.getContainerID(container)
        dHelper.restore(dHelper.getContainerID(container), checkpoint_dir, checkpoint_name)