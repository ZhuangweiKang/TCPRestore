#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import ZMQHelper as zmq

# Message Type: Host IP Address
def sendHostIP(socket, hostIP):
    msg = 'hostIP %s' %  hostIP
    socket.send_string(msg)
    socket.recv_string()

# Message Type: Swarm Join Token
def sendJoinToken(socket, token):
    msg = 'joinToken %s' % token
    socket.send_string(msg)
    socket.recv_string()

# Message Type: Image Name
def sendImageName(socket, imageName):
    msg = 'imageName %s' % imageName
    socket.send_string(msg)
    socket.recv_string()

# Message Type: Container IP Address
def sendContainerIP(socket, containerIP):
    msg = 'containerIP %s' % containerIP
    socket.send_string(msg)
    socket.recv_string()

def sendNetworkName(socket, networkName):
    msg = 'networkName %s' % networkName
    socket.send_string(msg)
    socket.recv_string()

#################################################

def recvMsg(socket, target):


