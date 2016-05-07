#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TestingScript
Register Node to main
H28 May 6
"""

import sys
import socket
import time
from contextlib import closing
from multiprocessing import Process

STARTUP_TIME = time.time()

def uptime():
    """ uptime """
    return str(time.time() - STARTUP_TIME)[:8]

def test_print(strings):
    """ print """
    print("[{}] [TEST] {}".format(uptime(), strings))

def udp_send_thread(srv_host, srv_port):
    """ UDP Publisher Thread """
    print("")
    for i in range(50, -1, -1):
        print("\033[1m\033[1ACount : {}\033[0m ".format(i/10))
        time.sleep(0.05)
    print("\033[1A")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    test_print("Connect Thread Server")
    with closing(sock):
        for i in range(5):
            sock.sendto("test strings {}".format(i).encode(), (srv_host, srv_port))


def regist_node(msg):
    """ Regist Node and Get Topic Addr """
    host = "127.0.0.1"
    port = 11311
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_print("Connnect Main Server")
    with closing(sock):
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            sys.exit("\033[01m\033[91m[ERROR] Can't connect TCP Server\n \
            [ERROR] TCP Server is not open\033[0m")
        self_addr = sock.getsockname()
        test_print("OWN ADDR {}".format(self_addr))
        sock.send(msg.encode())
        recv_msg = sock.recv(4096).decode().split(':')
        # Example: recv_msg = ['RET', '/debug', '127.0.0.1', '56432']
        test_print(recv_msg)
    if recv_msg[0] == "RET":
        server_host = recv_msg[2]
        server_port = int(recv_msg[3])
        test_print("{}:{}".format(server_host, server_port))
        return server_host, server_port, self_addr
    else:
        sys.exit("ERROR RET VALUE: " + recv_msg[0])


def recive_udp(self_addr):
    """ UDP Subscriber """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    test_print("Listen UDP ...")
    with closing(sock):
        sock.bind(self_addr)
        while True:
            recv_msg = sock.recv(4096).decode()
            test_print(recv_msg)


def main():
    """ main """
    test_print("StartTesting ...")

    argv = sys.argv
    argc = len(argv)

    topic_name = "/debug"

    if argc > 1:
        for opt in argv:
            if opt == '-h':
                print("HELP  --- OPTION")
                print("-p UDP Publisher")
                print("-s UDP Subscriber")
                print("-t Topic Name")
                print("ex) ./regist_node.py -t -p -s /debug")
            elif opt == '-t':
                topic_name = argv[-1]
                test_print("Set Topic Name :{}".format(topic_name))
            elif opt == '-p':
                test_print("UDP Publisher")
                msg = "PUB:{}".format(topic_name)
                server_host, server_port, self_addr = regist_node(msg)
                process = Process(target=udp_send_thread, args=(server_host, server_port,))
                process.start()
            elif opt == '-s':
                test_print("UDP Subscriber")
                msg = "SUB:{}".format(topic_name)
                server_host, server_port, self_addr = regist_node(msg)
                recive_udp(self_addr)
    else:
        # TCP Connection
        msg = "SUB:/debug"
        server_host, server_port, self_addr = regist_node(msg)

        # Make UDP send thread
        process = Process(target=udp_send_thread, args=(server_host, server_port,))
        process.start()

        # Wait UDP
        recive_udp(self_addr)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C -> END")

