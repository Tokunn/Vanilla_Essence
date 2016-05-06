#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vanilla Essence Main Program
H28 May 4
"""

import socket
from contextlib import closing

import medthre


def main():
    """ main function """

    print("[DEBUG] [main] Starting Vanilla Essence ...")

    topic_list = {}

    #debug_queue = Queue()
    #debug_threadinfo = ThreadInfo('/debug', '127.0.0.1', 11312) # TODO Ctrl topic port
    #debug_process = Process(target=mediator_thread, args=(debug_threadinfo, debug_queue,))
    #debug_process.start()
    #topic_list[debug_threadinfo.topic] = debug_threadinfo # Register topic thread info

    # Make /debug Topic Thread
    topic_list['/debug'] = medthre.MediatorThread('/debug')
    topic_list['/debug'].start()

    # TCP listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 11311
    bufsize = 4096

    sock.bind(('127.0.0.1', port))
    sock.listen(10)

    # Main Loop
    while True:
        # Recive ControlData
        print("[DEBUG] [main] Waiting TCP connection on {} ...".format(port))
        conn, address = sock.accept()

        ctrl_msg = conn.recv(bufsize).decode()

        # Return Thread Information
        rcv_topic_name = ctrl_msg[4:-1]
        print("[DEBUG] [main] RCV REQUEST : {}".format(rcv_topic_name))
        if not rcv_topic_name in topic_list:
            print("New Topic")
            topic_list[rcv_topic_name] = medthre.MediatorThread(rcv_topic_name)
            topic_list[rcv_topic_name].start()
            #node_queue = Queue()
            #threadinfo = ThreadInfo(rcv_topic_name, '127.0.0.1', 11312)
            ## TODO must make process list (follow process)
            #nw_process = Process(target=mediator_thread, args=(threadinfo, node_queue,))
            #nw_process.start()
            #topic_list[threadinfo.topic] = threadinfo
        # Register Subscriber
        rcv_nodetype = ctrl_msg[:3]
        if rcv_nodetype == "SUB":
            topic_list[rcv_topic_name].set_sub('127.0.0.1', 11312)

        #demand_tpc = topic_list[rcv_topic_name]
        ret_msg = "RET:{}:{}".format(topic_list[rcv_topic_name].ipaddr, topic_list[rcv_topic_name].port)
        conn.send(ret_msg.encode())
        #conn.close()
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
