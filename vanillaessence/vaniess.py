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

    # Main Loop
    while True:
        # Recive ControlData
        print("[DEBUG] [main] Waiting TCP connection on {}:{} ...".format(main_ip, main_port))
        node_conn, node_addr = sock.accept()

        ctrl_msg = node_conn.recv(bufsize).decode()

        # Return Thread Information
        rcv_topic_name = ctrl_msg[4:]
        print("[DEBUG] [main] RCV REQUEST : {}".format(rcv_topic_name))
        if not rcv_topic_name in topic_list:
            print("New Topic")
            topic_list[rcv_topic_name] = medthre.MediatorThread(rcv_topic_name)
            topic_list[rcv_topic_name].start()
            # Register Subscriber
        rcv_nodetype = ctrl_msg[:3]
        if rcv_nodetype == "SUB":
            topic_list[rcv_topic_name].set_sub(node_addr)

        ret_msg = "RET:{}:{}".format(topic_list[rcv_topic_name].ipaddr, topic_list[rcv_topic_name].port)
        node_conn.send(ret_msg.encode())
        #conn.close()
    sock.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C -> END")
