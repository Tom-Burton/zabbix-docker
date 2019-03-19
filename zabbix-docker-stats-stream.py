#!/usr/bin/python

#################################################################
#
# zabbix-docker-stats.py
#
#   A program that produces information for Zabbix to
#   process Docker container statistics.
#
# Version: 1.0
#
# Author: Richard Sedlak
#
#################################################################

import sys
import os
import time
import re
import subprocess

def B(b):
    return int(float(b))

def KB(b):
    return int(float(b) * 1024)

def MiB(b):
    return int(float(b) * 1000 * 1000)

def GiB(b):
    return int(float(b) * 1000 * 1000 * 1000)

def TB(b):
    return int(float(b) * 1024 * 1024 * 1024 * 1024)

def PCT(b):
    return float(b)

size_options = {
    'k':KB,
    'K':KB,
    'm':MiB,
    'M':MiB,
    'g':GiB,
    'G':GiB,
    't':TB,
    'T':TB,
    'b':B,
    'B':B,
    '%':PCT
}

def recalc(data):
     pat = re.compile(r'([0-9.]+)([a-zA-Z%])')
     mo = pat.match(data)
     if mo:
         number, unit = mo.group(1,2)
         value = size_options[unit](number)
     else:
         value = False
     return value

def pcpu(data):
     return recalc(data[1])

def umem(data):
     return recalc(data[2])

def lmem(data):
     return recalc(data[4])

def pmem(data):
     return recalc(data[5])

def inet(data):
     return recalc(data[7])

def onet(data):
     return recalc(data[9])

options = {
    'pcpu':pcpu,
    'umem':umem,
    'lmem':lmem,
    'pmem':pmem,
    'inet':inet,
    'onet':onet
}

def local_run_command(cmd,file):
    cmd = cmd + " > " + file
    a = subprocess.Popen(cmd, shell=True)
    time.sleep(2)
    subprocess.Popen.kill(a)
    with open(file, 'r') as f:
            lines = f.read().splitlines()
            strings = lines[-1]
    return strings.split()

container=sys.argv[1]
key=sys.argv[2]

cmd="docker stats " + container
strings = local_run_command(cmd,"/tmp/zabbix-docker-stats-"+container+".out")

print options[key](strings)
os.system('pkill -f \"docker stats\"')
