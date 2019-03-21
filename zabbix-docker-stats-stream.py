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

def local_run_command(cmd,fname):
    cmd = cmd + " > " + fname
    a = subprocess.Popen(cmd, shell=True)
    time.sleep(1.5)
    with open(fname, 'r') as f:
            lines = f.read().splitlines()
            strings = lines[-1]
            filelength = 0
    while filelength <= 1:
            filelength = get_length(fname)
            continue
    subprocess.Popen.kill(a)
    return strings.split()


def get_length(fname):
    with open(fname) as f:
        i = 0    
        for i, l in enumerate(f):
            pass
    return i + 1

def kill_procs(container):
    killcmd = "pkill -f \"docker stats " +container+"\""
    os.system(killcmd)

container=sys.argv[1]
key=sys.argv[2]

cmd ="docker stats " + container
fname = "/tmp/zabbix-docker-stats-"+container+".out" 
strings = local_run_command(cmd,fname)
print options[key](strings)
os.system("rm " + fname)
kill_procs(container)
