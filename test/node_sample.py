#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
/test/node_sample.py
Vaninode Sample
H28 May 8
"""

import os
import sys
import time

#PATH = os.path.join(os.path.dirname(__file__), '../vanillaessence/')
#sys.path.append(PATH)
#import logprint
PATH = os.path.join(os.path.dirname(__file__), '../nodelib/')
sys.path.append(PATH)
import vaninode

#----- main() -----#
def main():
    """ main """
    debug_class = vaninode.VaniEssNode('/debug')
    debug_class.regist_subscriber()
    #debug_class.regist_publisher()

    sensor_class = vaninode.VaniEssNode('/sensor_value')
    sensor_class.regist_subscriber()

    print("")
    for i in range(20, -1, -1):
        print("\033[1m\033[1ACount : {}\033[0m ".format(i/10))
        time.sleep(0.05)
    print("\033[1A")

    debug_class.publish("Hello, world!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C -> END")

