#!/usr/bin/env /usr/local/bin/python
# encoding: utf-8
# Author: Zhuangwei Kang

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import Controller as controller

def main(choice):
    publisher_image_tag = 'publisher:latest'
    publisher_container_name = 'Publisher'
    publisher_image_path = 'zhuangweikang/publisher'

    def testPub():
        print('--------------------------------------')
        print('Test case 1: Dump and restore Publisher container')
        controller.executor(publisher_image_path, publisher_image_tag, publisher_container_name, True)

    def testSub():
        print('--------------------------------------')
        print('Test case 2: Dump and restore Subscriber container')
        controller.executor(publisher_image_path, publisher_image_tag, publisher_container_name, False)

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