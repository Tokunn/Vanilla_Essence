#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vanilla Essence Mediator Thread Program
H28 May 6
"""

from multiprocessing import Process, Queue
import socket
from contextlib import closing


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
    print("[DEBUG] [mediator_thread] Starting {} on {} ...".format(threinfo.topic, threinfo.port))
    # Make subscriber node list
    sub_node_list = []

    # Make socket
    medi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with closing(medi_sock):
        medi_sock.bind((threinfo.ipaddr, threinfo.port))

        # Mediator main loop
        while True:
            # recive UDP
            b_recvdata = medi_sock.recv(4096)
            print("[DEBUG] [mediator_thread] RCV VALUE: {}".format(b_recvdata.decode()))

            # Check new subscriber node
            while True:
                if nodeque.empty():
                    break
                else:
                    new_sub = nodeque.get_nowait()
                    sub_node_list.append(new_sub)
                    print("[DEBUG] [mediator_thread] NEW SUB: {}".format(new_sub))

            # Send to each sub node
            for sub_node in sub_node_list:
                medi_sock.sendto(b_recvdata, (sub_node.ipaddr, sub_node.port))
                print("[DEBUG] [mediator_thread]  {}:{} {}".format(
                    sub_node.ipaddr, sub_node.port, b_recvdata.decode()))

    return


class MediatorThread(object):
    """ Mediator Thread Process """
    def __init__(self, topic):
        self.topic = topic
        self.ipaddr = '127.0.0.1' # TODO
        self.port = 11321 # TODO
        self.__queue = Queue()
        threinfo = ThreadInfo(self.topic, self.ipaddr, self.port)
        self.__process = Process(target=mediator_thread, args=(threinfo, self.__queue,))
    def start(self):
        """ Make new thread """
        self.__process.start()
    def set_sub(self, sub_ipaddr, sub_port):
        """ Set Subscriber to thread """
        nodeinfo = NodeInfo(sub_ipaddr, sub_port)
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

