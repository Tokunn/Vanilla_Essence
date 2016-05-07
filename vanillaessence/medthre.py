#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vanilla Essence Mediator Thread Program
H28 May 6
"""

from multiprocessing import Process, Queue
import socket
#from contextlib import closing
import random


class ThreadInfo(object):
    """ Thread Infomation """
    def __init__(self, topic, ipaddr, port):
        self.topic = topic
        self.ipaddr = ipaddr
        self.port = port
    def set(self):
        """ set """
        pass
    def get(self):
        """ get """
        pass


class NodeInfo(object):
    """ Node Information """
    def __init__(self, ipaddr, port):
        self.ipaddr = ipaddr
        self.port = port
    def set(self):
        """ set """
        pass
    def get(self):
        """ get """
        pass




def mediator_thread(threinfo, nodeque):
    """ Mediator Thread """
    try:
        print("[INFO] [mediator_thread] Starting {} Topic on {} ...".format(
            threinfo.topic, threinfo.port))
        # Make subscriber node list
        sub_node_list = []

        # Make socket
        medi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        medi_sock.bind((threinfo.ipaddr, threinfo.port))

        # Mediator main loop
        while True:
            # recive UDP
            b_recvdata, recvaddr = medi_sock.recvfrom(4096)
            print("[DEBUG] [mediator_thread] RECV <  {}:{} : {}".format(
                recvaddr[0], recvaddr[1], b_recvdata.decode()))

            # Check new subscriber node
            while True:
                if nodeque.empty():
                    break
                else:
                    new_sub = nodeque.get_nowait()
                    sub_node_list.append(new_sub)
                    tmp = "{}:{}".format(new_sub.ipaddr, new_sub.port)
                    print("[DEBUG] [mediator_thread] NEW SUB:" + tmp)

            # Send to each sub node
            for sub_node in sub_node_list:
                medi_sock.sendto(b_recvdata, (sub_node.ipaddr, sub_node.port))
                print("[DEBUG] [mediator_thread] SEND  > {}:{} : {}".format(
                    sub_node.ipaddr, sub_node.port, b_recvdata.decode()))

        medi_sock.close()
    except KeyboardInterrupt:
        pass
    return


class MediatorThread(object):
    """ Mediator Thread Process """
    def __init__(self, topic):
        self.topic = topic
        self.ipaddr = '127.0.0.1' # TODO
        self.port = random.randrange(49152, 65535)
        self.__queue = Queue()
        threinfo = ThreadInfo(self.topic, self.ipaddr, self.port)
        self.__process = Process(target=mediator_thread, args=(threinfo, self.__queue,))
    def start(self):
        """ Make new thread """
        self.__process.start()
    def set_sub(self, sub_addr):
        """ Set Subscriber to thread """
        nodeinfo = NodeInfo(sub_addr[0], sub_addr[1])
        self.__queue.put(nodeinfo)


#----- main() -----#
def main():
    """ main """
    print("Hello, world!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C -> END")

