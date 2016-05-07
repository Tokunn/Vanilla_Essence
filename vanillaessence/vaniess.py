#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vanilla Essence Main Program
H28 May 4
"""

import socket
#from contextlib import closing

import medthre
from logprint import *


def main():
    """ main function """

    topic_list = {}

    # Make /debug Topic Thread
    topic_list['/debug'] = medthre.MediatorThread('/debug')
    topic_list['/debug'].start()

    # TCP listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_ip = '127.0.0.1'
    main_port = 11311
    bufsize = 4096

    sock.bind((main_ip, main_port))
    sock.listen(10)

    loginfo("[main] Waiting TCP connection on {}:{} ...".format(main_ip, main_port))
    # Main Loop
    while True:
        logdebug("[main] Loop Start")

        # Recive ControlData
        node_conn, node_addr = sock.accept()
        ctrl_msg = node_conn.recv(bufsize).decode()
        ctrl_msg = ctrl_msg.split(':')  # Example: ctrl_msg = ['SUB', '/debug']
        rcv_topic_name = ctrl_msg[1]
        rcv_nodetype = ctrl_msg[0]

        # Return Thread Information
        logdebug("[main] RCV REQUEST : {}".format(rcv_topic_name))
        if not rcv_topic_name in topic_list:
            logdebug("New Topic")
            topic_list[rcv_topic_name] = medthre.MediatorThread(rcv_topic_name)
            topic_list[rcv_topic_name].start()
        # Register Subscriber
        if rcv_nodetype == "SUB":
            topic_list[rcv_topic_name].set_sub(node_addr)

        tmp_thre = topic_list[rcv_topic_name]
        ret_msg = "RET:{}:{}:{}".format(tmp_thre.topic, tmp_thre.ipaddr, tmp_thre.port)
        node_conn.send(ret_msg.encode())
        #conn.close()
    sock.close()


if __name__ == '__main__':
    loginfo("***** Starting Vanilla Essence ... *****")
    loginfo("Start Up Time : {}".format(startup_time))
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C -> END")
