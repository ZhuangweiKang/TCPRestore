#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import docker
import os

def setClient():
    return docker.from_env()

def buildImage(client, path, tag):
    return client.images.build(path=path, tag=tag)

def pullImage(client, repository):
    client.images.pull(repository)

def runContainer(client, image, name, network=None):
    return client.containers.run(image=image, name=name, detach=True, ports={'3000/tcp':3000}, network=network)

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

def restore(containerID, checkpoint_dir, checkpoint_name):
    # checkpoint_dir = '/var/lib/docker/containers/%s/checkpoints/' % containerID
    restore_cmd = 'docker start --checkpoint-dir=%s --checkpoint=%s %s' % (checkpoint_dir, checkpoint_name, containerID)
    print(os.popen(restore_cmd, 'r').read())

def initSwarm(client, advertise_addr):
    client.swarm.init(advertise_addr=advertise_addr)

def joinSwarm(client, token, address):
    client.swarm.join(remote_addrs=[address], join_token=token)

def leaveSwarm(client):
    client.swarm.leave()

def getNodeList(client):
    return client.nodes.list(filter={'role': 'worker'})

def getJoinToken():
    cmd = 'docker swarm join-token worker -q'
    return os.popen(cmd, 'r').read()

def deleteNode(node_name):
    cmd = 'docker node rm %s' % node_name
    os.system(cmd)

def createNetwork(client, name, driver='overlay', attachable=True, subnet=None):
    ipam_pool = docker.types.IPAMPool(subnet=subnet)
    ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
    client.networks.create(name=name, driver=driver, ipam=ipam_config, attachable=attachable)

def getContainerIP(container_name):
    cmd = 'docker inspect -f \'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}\' %s' % container_name
    return os.popen(cmd, 'r').read()

def createContainer(client, image, name, network=None):
    client.containers.create(image=image, name=name, detach=True, network=network)