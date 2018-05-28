#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import time
import random
import DockerHelper as dHelper

def executor(imagePath, imageTag, containerName, doDump=False):

    # create docker client
    client = dHelper.setClient()

    # check container if exists
    if dHelper.checkContainer(client, containerName) is True:
        container = dHelper.getContainer(client, containerName)
        dHelper.deleteContainer(container)

    # check if image exists
    if dHelper.checkImage(client, imageTag) is False:
        dHelper.buildImage(client, imagePath, imageTag)

    # Run a subscriber container
    container = dHelper.runContainer(client, imageTag, containerName)

    if doDump:
        print('\n-------------------\nWaiting 30 seconds...')

        time.sleep(30)

        # checkpoint the container
        checkpoint_name = 'checkpoint_' + str(random.randint(1, 100))
        dHelper.checkpoint(checkpoint_name, dHelper.getContainerID(container))

        print('\n-------------------\nWaiting for 20 seconds...')
        time.sleep(20)

        # restore the container
        dHelper.restore(dHelper.getContainerID(container), checkpoint_name)