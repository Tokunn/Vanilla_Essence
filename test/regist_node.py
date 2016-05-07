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

host = "127.0.0.1"
port = 11311

msg = "SUB:/debug"

startup_time = time.time()

def uptime():
    return str(time.time() - startup_time)[:8]

def test_print(strings):
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


def regist_node():
    """ Regist Node and Get Topic Addr """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_print("Connnect Main Server")
    with closing(sock):
        sock.connect((host, port))
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
    test_print("StartTesting ...")

    argv = sys.argv
    argc = len(argv)


    # TCP Connection
    server_host, server_port, self_addr = regist_node()

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

