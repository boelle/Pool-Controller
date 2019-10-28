#!/usr/bin/python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#     Pool Monitor System
#          poolmain.py
#
# This is the main script.
#
# It provides a loop and checks a schedule to determine
# if the pump should be on or off when in "auto" mode.
#
# Author : Matt Hawkins
# Date   : 06/08/2018
#
# Additional details of this project here:
# http://bit.ly/pizeropool
#
# Visit my Raspberry Pi Blog for other awesome content:
# https://www.raspberrypi-spy.co.uk/
#
# -----------------------------------------------------------

import time
import logging
import config as c
import poollib as p
import sys, string
import http.client

logFormat = '%(asctime)s %(levelname)s:%(message)s'
logging.basicConfig(format=logFormat,
                    filename='/home/pi/pool/logs/main.log',
                    level=logging.DEBUG)
logging.info('Main start')

# Check current saved status and create pickle files
# if they don't already exist

p.checkStatus()
p.checkSchedule()
p.checkStatus1()
p.checkSchedule1()

# Get the IDs of the DS18B20 temp sensors

mySensorIDs = p.getSensorIDs()

# Set number of seconds to wait between loops

loopDelay = c.LOOPDELAY

# Set number of loops to wait before sending data to Thingspeak

loopSendData = c.LOOPSENDDATA

loopCounter = 0

# emoncms details

domain = 'takeaguess'
emoncmspath = 'emoncms'
apikey = 'takeaguess'
nodeid = 10000

if __name__ == '__main__':

    while True:

    # Read current schedule, pump status and mode
    # as it may have been changed by web interface since last loop

        myHours = p.getSchedule()
        (myPumpMode, myPumpStatus, booststart) = p.getStatus()
        myHours1 = p.getSchedule1()
        (myPumpMode1, myPumpStatus1, booststart1) = p.getStatus1()

    # Deal with pump based on current mode

        myPumpStatus = p.pumpUpdate(myPumpMode)
        myPumpStatus1 = p.pumpUpdate1(myPumpMode1)

    # Read temperatures in C or F and send to
    # emoncms every 5 loops

        loopCounter += 1
        if loopCounter == loopSendData:
            sunalt,sunangle=p.sun()
            (temp1, temp2, temp3) = p.readTemps(mySensorIDs, c.TEMPUNIT)
            seq = (temp1, temp2, temp3, sunalt, sunangle, myPumpStatus, myPumpStatus1)
            str_join = ','.join(str(x) for x in seq)
            conn = http.client.HTTPConnection(domain)

            conarg1 = (
                '/',
                emoncmspath,
                '/input/post?node=',
                str(nodeid),
                '&csv=',
                str_join,
                '&apikey=',
                apikey,
                )
            conarg = ''.join(str(x) for x in conarg1)

            conn.request('GET', conarg)

            response = conn.getresponse()
            loopCounter = 0

    # Wait before doing it all again

        time.sleep(loopDelay)
