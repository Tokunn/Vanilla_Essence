#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vanilla Essence Log Print Program
H28 May 7
"""

import time

STARTUP_TIME = time.time()

def uptime():
    """ Return STR uptime """
    return str(time.time() - STARTUP_TIME)[:10]

def getstartup_time():
    """ Return FLOAT Startup time """
    return STARTUP_TIME

def logdebug(strings):
    """ Print Debug """
    log = "\033[32m[DEBUG] [{}]: {}\033[0m".format(uptime(), strings)
    print(log)

def loginfo(strings):
    """ Print Info """
    log = "\033[01m[ INFO] [{}]: {}\033[0m".format(uptime(), strings)
    print(log)

def logwarn(strings):
    """ Print Warn """
    log = "\033[93m[ WARN] [{}]: {}\033[0m".format(uptime(), strings)
    print(log)

def logerr(strings):
    """ Print Err """
    log = "\033[01m\033[91m[  ERR] [{}]: {}\033[0m".format(uptime(), strings)
    print(log)
