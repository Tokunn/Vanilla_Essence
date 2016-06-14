#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
/nodelib/vaninode.py
Vanilla Essence Python Node Library
H28 May 8
"""

import os
import sys
from multiprocessing import Process, Value
import ctypes
import socket

PATH = os.path.join(os.path.dirname(__file__), '../vanillaessence/')
sys.path.append(PATH)
import logprint
import addr_conf


class VaniEssNode(object):
    """ Vanilla Essence Node Class """
    def __init__(self, topic):
        self.topic = topic
        self.msg = Value(ctypes.c_char_p, "".encode())
        self.process = Process(target=self.sub_process, args=(self.msg,))
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_host = ""
        self.server_port = 0
        self.already_regist_pub = False
        self.already_regist_sub = False

    def set_callback(self, function):
        """ set callback function """
        pass

    def regist_node(self, ctrl_msg):
        """ TCP Connection (Get Topic Addr) """
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_sock.connect((addr_conf.host, addr_conf.port))
        except ConnectionRefusedError:
            tcp_sock.close()
            logprint.logerr("[sub_process] Can't connect TCP Server")
            logprint.logerr("[sub_process] TCP Server is not open")
            sys.exit()
        tcp_sock.send(ctrl_msg.encode())
        recv_msg = tcp_sock.recv(4096).decode().split(':')
        self_addr = tcp_sock.getsockname()
        tcp_sock.close()
        logprint.logdebug("[sub_process] OWN ADDR {}".format(self_addr))
        if recv_msg[0] == "RET":
            self.server_host = recv_msg[2]
            self.server_port = int(recv_msg[3])
            logprint.logdebug("[sub_process] {} is waiting on {}:{}".format(
                self.topic, self.server_host, self.server_port))
            return self_addr

    def sub_process(self, p_msg):
        """ Subscriber Process """
        # Get Server Addr
        ctrl_msg = "SUB:{}".format(self.topic)
        self_addr = self.regist_node(ctrl_msg)

        # Recive UDP (Get Topic Message)
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logprint.logdebug("[sub_process] Listening UDP ...")
        udp_sock.bind(self_addr)
        try:
            while True:
                #self.msg.value = udp_sock.recv(4096)
                p_msg = udp_sock.recv(4096)
                logprint.logdebug("[sub_process] Recive UDP msg {}".format(
                    p_msg.decode()))
        except KeyboardInterrupt:
            pass

    def regist_subscriber(self):
        """ Register Subscriber """
        self.process.start()
        self.already_regist_sub = True

    def regist_publisher(self):
        """ Register Publisher """
        ctrl_msg = "PUB:{}".format(self.topic)
        self.regist_node(ctrl_msg)
        self.already_regist_pub = True

    def subscribe(self):
        """ Subscribe """
        return self.msg.value.decode()

    def publish(self, msg):
        """ Publish """
        if not self.already_regist_pub:
            logprint.logwarn("[publish] Call regist_publisher")
        self.udp_sock.sendto(msg.encode(), (self.server_host, self.server_port))
