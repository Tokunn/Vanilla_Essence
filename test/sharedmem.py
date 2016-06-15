#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time
from multiprocessing import Process, Value
import ctypes

class SharedMem(object):
    def __init__(self):
        self.msg = Value(ctypes.c_char, "DEFAULT".encode())
        self.process = Process(target=self.sub_process, args=(self.msg, ))
        self.process.start()

    def get_value(self):
        return self.msg.value

    def sub_process(self, p_msg):
        i = 0
        while True:
            time.sleep(1)
            i += 1
            p_msg.value = str(i)
            

#----- main() -----#
def main():
    sharemem = SharedMem()
    while True:
        time.sleep(0.1)
        print(sharemem.get_value())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C -> END")

