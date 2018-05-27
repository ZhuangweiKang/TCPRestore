#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import docker
import os

def setClient():
    return docker.from_env()

def buildImage(client, path, tag):
    return client.images.build(path=path, tag=tag)

def runContainer(client, image, name):
    return client.containers.run(image=image, name=name, STDIN=True, tty=True, detach=True)

def getContainer(client, name):
    return client.containers.get(name)

def checkImage(client, tag):
    images = client.images.list()
    for image in images:
        if tag in image.tags:
            return True
    return False

def checkContainer(client, container_name):
    try:
        client.containers.get(container_name)
        return True
    except docker.errors.NotFound:
        return False

def deleteContainer(container):
    container.remove(force=True)

def getContainerID(container):
    return container.id

def checkpoint(checkpoint_name, containerID):
    checkpoint_cmd = 'docker checkpoint create ' + containerID + ' ' + checkpoint_name
    print(os.popen(checkpoint_cmd, 'r').read())

def restore(containerID, checkpoint_name):
    checkpoint_dir = '/var/lib/docker/containers/%s/checkpoints/'
    restore_cmd = 'docker start --checkpoint-dir=%s --checkpoint=%s %s' % (checkpoint_dir, checkpoint_name, containerID)
    print(os.popen(restore_cmd, 'r').read())