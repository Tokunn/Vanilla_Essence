#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vanilla Essence Main Program
H28 May 4
"""

from multiprocessing import Process, Queue
import socket
from contextlib import closing

class MediatorNode(object):
    """ Thread Infomation """
    def __init__(self, threinfo):
        self.topic = threinfo.topic
        self.ipaddr = threinfo.ipaddr
        self.port = threinfo.port
        self.queue = Queue()
        self.process = Process(target=mediator_thread, args=(threinfo, queue,))
    def start(self):
        """ Make new thread """
        self.process.start()


class ThreadInfo(object):
    """ Thread Infomation """
    def __init__(self, topic, ipaddr, port):
        self.topic = topic
        self.ipaddr = ipaddr
        self.port = port
    def get_topic(self):
        """ get topic """
        return self.topic
    def get_ipaddr(self):
        """ get ipaddr """
        return self.ipaddr
    def get_port(self):
        """ get port """
        return self.port

class NodeInfo(object):
    """ Node Information """
    def __init__(self, ipaddr, port):
        self.ipaddr = ipaddr
        self.port = port
    def get_ipaddr(self):
        """ get ipaddr """
        return self.ipaddr
    def get_port(self):
        """ get port """
        return self.port


def mediator_thread(threinfo, nodeque):
    """ Mediator Thread """
    print("Start {}".format(threinfo.topic))
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

            # Check new subscriber node
            while True:
                if nodeque.empty():
                    break
                else:
                    new_sub = nodeque.get_nowait()
                    sub_node_list.append(new_sub)

            # Send to each sub node
            for sub_node in sub_node_list:
                medi_sock.sendto(b_recvdata, (sub_node.ipaddr, sub_node.port))
                print("{}:{} {}".format(
                    sub_node.ipaddr, sub_node.port, b_recvdata.decode()))

    return


def main():
    """ main function """

    topic_list = {}

    # Make Debug Topic TODO it can be function
    debug_queue = Queue()
    debug_threadinfo = ThreadInfo('/debug', '127.0.0.1', 11312) # TODO Ctrl topic port
    debug_process = Process(target=mediator_thread, args=(debug_threadinfo, debug_queue,))
    debug_process.start()
    topic_list[debug_threadinfo.topic] = debug_threadinfo # Register topic thread info

    # TCP listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bufsize = 4096

    sock.bind(('127.0.0.1', 11311))
    sock.listen(10)

    # Main Loop
    #while True: TODO while 
    # Recive Control
    conn, address = sock.accept()

    ctrl_msg = conn.recv(bufsize).decode()
    ctrl_msg = "SUB:/debug" # TODO test

    # Return Thread Information
    rcv_topic_name = ctrl_msg[4:]
    print("RCV TOPIC : {}".format(rcv_topic_name))
    if not rcv_topic_name in topic_list:
        print("New Topic")
        node_queue = Queue()
        threadinfo = ThreadInfo(rcv_topic_name, '127.0.0.1', 11312)
        # TODO must make process list (follow process)
        nw_process = Process(target=mediator_thread, args=(threadinfo, node_queue,))
        nw_process.start()
        topic_list[threadinfo.topic] = threadinfo
    # Register Subscriber
    rcv_position = ctrl_msg[:2]
    if rcv_position == "SUB":
        pass # TODO send node info

    demand_tpc = topic_list[rcv_topic_name]
    ret_msg = "RET:{}:{}".format(demand_tpc.ipaddr, demand_tpc.port)
    conn.send(ret_msg.encode())
    sock.close()



#    """
#    # Make queue
#    node_queue = Queue()
#    # Make thread
#    threadinfo = ThreadInfo('/debug', '127.0.0.1', 11311)
#    tf_process = Process(target=mediator_thread, args=(threadinfo, node_queue,))
#    tf_process.start()
#
#    # Send queue
#    nodeinfo = NodeInfo('localhost', 11312)
#    node_queue.put(nodeinfo)
#    nodeinfo = NodeInfo('127.0.0.1', 11313)
#    node_queue.put(nodeinfo)
#
#    tf_process.join()
#    """


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C -> END")
