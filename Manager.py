#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import time
import random
import threading
import argparse
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

        print('\n-------------------\nWaiting for 30 seconds...')
        time.sleep(20)

        # restore the container
        dHelper.restore(dHelper.getContainerID(container), checkpoint_name)

def main(choice):
    publisher_image_tag = 'publisher:latest'
    publisher_container_name = 'Publisher'
    publisher_image_path = './Publisher/'

    subscriber_image_tag = 'subscriber:latest'
    subscriber_container_name = 'Subscriber'
    subscriber_image_path = './Subscriber/'

    def testPub():
        print('--------------------------------------')
        print('Test case 1: Dump and restore Publisher container')

        pubThr = threading.Thread(target=executor, args=(publisher_image_path, publisher_image_tag, publisher_container_name, True, ))
        subThr = threading.Thread(target=executor, args=(subscriber_image_path, subscriber_image_tag, subscriber_container_name, False, ))

        pubThr.setDaemon(True)
        subThr.setDaemon(True)

        pubThr.start()
        subThr.start()

    def testSub():
        print('--------------------------------------')
        print('Test case 2: Dump and restore Subscriber container')

        pubThr = threading.Thread(target=executor, args=(publisher_image_path, publisher_image_tag, publisher_container_name, False,))
        subThr = threading.Thread(target=executor, args=(subscriber_image_path, subscriber_image_tag, subscriber_container_name, True,))

        pubThr.setDaemon(True)
        subThr.setDaemon(True)

        pubThr.start()
        subThr.start()

    if choice == 1:
        testPub()
    else:
        testSub()

    while True:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--choice', type=int, default=1, help='1. Test Publisher, 2. Test Subscriber')
    args = parser.parse_args()
    choice = args.choice
    main(choice)