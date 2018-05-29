#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import os, sys
import time
import tarfile
import shutil
import socket
import struct
import random
import DockerHelper as dHelper
import ZMQHelper as zmq

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

def executorSwarm(logger, image, containerName, network, doDump=False, dst_address=None):
    # create docker client
    client = dHelper.setClient()

    logger.info('Checking if container exists.')

    # check container if exists
    if dHelper.checkContainer(client, containerName) is True:
        container = dHelper.getContainer(client, containerName)
        dHelper.deleteContainer(container)
        logger.info('Old container exists, deleting old container.')

    # check if image exists
    if dHelper.checkImage(client, image) is False:
        dHelper.pullImage(client, image)

    logger.info('Image doesn\'t exist, building image.')

    # Run a container
    container = dHelper.runContainer(client, image, containerName, network=network)

    logger.info('Creat and run a container.')

    if doDump:
        # TODO: notify dst node to download base image
        _socket = zmq.csConnect(dst_address, '3200')
        _socket.send_string('image:%s' % image)
        _socket.recv_string()
        logger.info('Current host has notified destination node to download base image.')

        logger.info('\n-------------------\nWaiting for 30 seconds, Publisher/Subscriber is sending/receiving messages.')

        time.sleep(30)

        # checkpoint the container
        checkpoint_name = 'checkpoint_' + str(random.randint(1, 100))

        dHelper.checkpoint(checkpoint_name, dHelper.getContainerID(container))

        logger.info('\nContainer has been dumped.')

        # TODO: tar dumped image files
        tarFiles(checkpoint_name, dHelper.getContainerID(container), checkpoint_name)
        logger.info('Tar dumped image files.')

        # TODO: send tar file to new host
        try:
            logger.info('Prepare to send tar file to destination host.')
            tarSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tarSocket.connect((dst_address, 3300))
            logger.info('Connection has been set up.')
        except socket.error as msg:
            logger.error(msg)
            sys.exit(1)
        fileName = checkpoint_name + '.tar'
        if os.path.isfile(fileName):
            fileinfo_size = struct.calcsize('128sl')
            fhead = struct.pack('128sl', os.path.basename(fileName), os.stat(fileName).st_size)
            tarSocket.send(fhead)

            fp = open(fileName, 'rb')
            while True:
                data = fp.read(1024)
                if not data:
                    break
                tarSocket.sendall(data)

            logger.info('Tar file has been sent.')

            fp.close()
            tarSocket.close()
        else:
            logger.error('File %s not exists.' % fileName)
            sys.exit(1)
    else:
        # TODO: listen message from source host to pull image
        iSocket = zmq.csBind('3200')
        msg = iSocket.recv_string()
        msg = msg.split(':')
        if msg[0] == 'image':
            dHelper.pullImage(client, msg[1])
        iSocket.send_string('Ack')

        # receive tar file
        try:
            recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            recvSocket.bind(('', 3300))
            recvSocket.listen(20)
            logger.info('Waiting for client to connect...')
            conn,addr = recvSocket.accept()
            logger.info('Client %s has connected to server...' % addr)
            goToWorkDir()
            fileinfo_size = struct.calcsize('128sl')
            fhead = conn.recv(fileinfo_size)
            fileName, fileSize = struct.unpack('128sl', fhead)
            logger.info('Received file info: %s' % fileName)
            logger.info('File size: ' + fileSize)

            tarFile = open(fileName, 'wb')
            logger.info('Start receiving file...')
            tempSize = fileSize
            while True:
                if tempSize > 1024:
                    data = conn.recv(1024)
                else:
                    data = conn.recv(tempSize)
                if not data:
                    break
                tarFile.write(data)
                tempSize -= len(data)
                if tempSize == 0:
                    break
            logger.info('Receiving file finished, connection will be closed...')
            tarFile.close()
            conn.close()
            recvSocket.close()
            logger.info('Connection has been closed...')

            # TODO: untar the received file
            untarFile(fileName)
            logger.info('Image file has been untared...')

            # TODO: restore container using untared file
            checkpoint_name = fileName.split('.')[0]
            checkpoint_dir = '/var/lib/docker/tmp'
            newContainer = 'newContainerFrom'+checkpoint_name
            dHelper.restore(newContainer, checkpoint_dir, checkpoint_name)
            logger.info('Container has been restored...')
        except Exception as ex:
            logger.error(ex)

def getWorkDir():
    return '/var/lib/docker/tmp'

def goToWorkDir():
    workDir = '/var/lib/docker/tmp'
    os.chdir(workDir)

def tarFiles(checkpointTar, containerID, checkpointName):
    checkpointDir = '/var/lib/docker/containers/%s/checkpoints/%s' % (containerID, checkpointName)
    os.chdir(checkpointDir)
    tar_file = tarfile.TarFile.open(name=checkpointTar, mode='w')
    tar_file.add('./')
    tar_file.close()
    shutil.move(checkpointTar, getWorkDir())
    goToWorkDir()

def untarFile(tarFile):
    goToWorkDir()
    tar = tarfile.TarFile.open(name=tarFile, mode='r')
    tar.extract('./')
    tar.close()
    os.remove(tarFile)

