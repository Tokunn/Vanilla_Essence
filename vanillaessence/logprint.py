#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vanilla Essence Log Print Program
H28 May 7
"""

import time

startup_time = time.time()

def uptime():
    return str(time.time() - startup_time)[:8]

def logdebug(strings):
    log = "\033[32m[{}] [DEBUG] {}\033[0m".format(uptime(), strings)
    print(log)

def loginfo(strings):
    log = "\033[01m[{}] [INFO]  {}\033[0m".format(uptime(), strings)
    print(log)

def logwarn(strings):
    log = "\033[93m[{}] [WARN]  {}\033[0m".format(uptime(), strings)
    print(log)

def logerr(strings):
    log = "\033[91m[{}] [ERR]   {}\033[0m".format(uptime(), strings)
    print(log)
