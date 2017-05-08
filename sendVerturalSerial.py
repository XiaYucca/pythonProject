#!/usr/bin/env python
#coding=utf-8

import pty
import os
import time
import array
import random

def mkpty():
    #make pair of pseudo tty
    master, slave = pty.openpty()
    slaveName = os.ttyname(slave)

    print '\nslave device names:', slaveName
    return master

if __name__ == "__main__":
    master = mkpty()
    buf = array.array('B', [0] * 7)
    buf[0] = 0x00
    buf[1] = 0x02
    buf[2] = 0x8a
    buf[3] = 0x2d
    buf[4] = 0xc5
    buf[5] = 0x3f
    buf[6] = 0x00

    while True:
        if buf[1] < 40:
            buf[1] = buf[1] + 1
        else:
            buf[1] = 1
            buf[0] = buf[0] + 1

        if buf[0] == 255:
            buf[0] = 0

#        buf[5] = random.randint(40,50)
        buf[2] = random.randint(0,250)
        buf[6] = ( buf[0]+buf[1]+buf[2]+buf[3]+buf[4]+buf[5]) %256
        os.write(master,  buf)
#        print buf
        time.sleep(0.02)        