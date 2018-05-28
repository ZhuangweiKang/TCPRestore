#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import Controller as controller

def main(choice):
    subscriber_image_tag = 'subscriber:latest'
    subscriber_container_name = 'Subscriber'
    subscriber_image_path = './Subscriber/'

    def testPub():
        print('--------------------------------------')
        print('Test case 1: Dump and restore Publisher container')
        controller.executor(subscriber_image_path, subscriber_image_tag, subscriber_container_name, False)

    def testSub():
        print('--------------------------------------')
        print('Test case 2: Dump and restore Subscriber container')
        controller.executor(subscriber_image_path, subscriber_image_tag, subscriber_container_name, True)

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