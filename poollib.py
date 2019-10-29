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
#          poollib.py
#
# This is a supporting set of functions that are used
# by the main script (poolmain.py) and the web front-end (poolweb.py).
#
# It serves a status page and allows users to set the
# pump mode and edit the schedule.
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

import os
import time
import datetime
import pickle
import requests
import wiringpi
from pyephem_sunpath.sunpath import sunpos
from datetime import datetime

# wiringpi numbers

wiringpi.wiringPiSetup()
wiringpi.pinMode(0, 1)  # sets pin 0 to output (GPIO 17, Actual hardware pin number is 11) (Pump1)
wiringpi.pinMode(2, 1)  # sets pin 2 to output (GPIO 27, Actual hardware pin number is 13) (Pump2)


def sun():

    thetime = datetime.now()
    lat = 55.327013
    lon = 10.438298
    tz = 2
    (alt, azm) = sunpos(thetime, lat, lon, tz, dst=False)
    sunalt = round(alt, 2)
    sunangle = round(azm, 2)

    return (sunalt, sunangle)


def saveStatus(mode,status,booststart):
  try:
    pickle.dump( [mode,status,booststart], open( "/home/pi/pool/status.p", "wb" ) )
  except:
    print("Problem saving status")


def saveStatus1(mode1,status1,booststart1):
  try:
    pickle.dump( [mode1,status1,booststart1], open( "/home/pi/pool/status1.p", "wb" ) )
  except:
    print("Problem saving status")


def getStatus():
    mode,status,booststart=pickle.load(open('/home/pi/pool/status.p', 'rb'))
    return mode,status,booststart


def getStatus1():
    mode1,status1,booststart1=pickle.load(open('/home/pi/pool/status1.p', 'rb'))
    return mode1,status1,booststart1


def saveSchedule(hours):
    try:
        pickle.dump(hours, open('/home/pi/pool/schedule.p', 'wb'))
    except:
        print("Problem saving schedule")


def saveSchedule1(hours1):
    try:
        pickle.dump(hours1, open('/home/pi/pool/schedule1.p', 'wb'))
    except:
        print("Problem saving schedule1")


def getSchedule():
    hours = pickle.load(open('/home/pi/pool/schedule.p', 'rb'))
    return hours


def getSchedule1():
    hours1 = pickle.load(open('/home/pi/pool/schedule1.p', 'rb'))
    return hours1


def checkStatus():
    if not os.path.isfile('/home/pi/pool/status.p'):
        print("No status.p file found")
        saveStatus('off', False, 0)
    else:
        print("Existing status.p file found")


def checkStatus1():
    if not os.path.isfile('/home/pi/pool/status1.p'):
        print("No status1.p file found")
        saveStatus1('off', False, 0)
    else:
        print("Existing status1.p file found")


def checkSchedule():
    if not os.path.isfile('/home/pi/pool/schedule.p'):
        print("No schedule.p file found")
        saveSchedule(['7', '8'])
    else:
        print("Existing schedule.p file found")


def checkSchedule1():
    if not os.path.isfile('/home/pi/pool/schedule1.p'):
        print("No schedule1.p file found")
        saveSchedule1(['7', '8'])
    else:
        print("Existing schedule1.p file found")


def readTemps(sensorID, tempunit='C'):
    read1 = getTemp(sensorID[0]) / float(1000)
    read2 = getTemp(sensorID[1]) / float(1000)
    read3 = getTemp(sensorID[2]) / float(1000)

    if tempunit.upper() == 'F':

      # Convert to Fahrenheit if unit is F

        read1 = read1 * 1.8 + 32
        read2 = read2 * 1.8 + 32
        read3 = read3 * 1.8 + 32

    t1 = '{:.1f}'.format(read1)
    t2 = '{:.1f}'.format(read2)
    t3 = '{:.1f}'.format(read3)
    return (t1, t2, t3)


def getTemp(id):
    try:
        mytemp = ''
        filename = 'w1_slave'
        f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
        line = f.readline()  # read 1st line
        crc = line.rsplit(' ', 1)
        crc = crc[1].replace('\n', '')
        if crc == 'YES':
            line = f.readline()  # read 2nd line
            mytemp = line.rsplit('t=', 1)
        else:
            mytemp = 99999
        f.close()

        return int(mytemp[1])
    except:

        return 99999


def getSensorIDs():
    sensorIDs = []

    try:
        for item in os.walk('/sys/bus/w1/devices/'):
            dirs = item[1]
            for dir in dirs:
                if dir[:3] == '28-':
                    sensorIDs.append(dir)
    except:
        sensorIDs = ['28-01', '28-02']
    if len(sensorIDs) == 0:
        sensorIDs = ['1', '2', '3']
    return sensorIDs


def pumpUpdate(mode):
    sunalt,sunangle=sun()
    prevPumpMode,prevPumpStatus,booststart=getStatus()
    hours = getSchedule()

    if mode == 'on':
        wiringpi.digitalWrite(0, 1) # sets port 0 to ON
        status = True
    elif mode == 'off':
        wiringpi.digitalWrite(0, 0) # sets port 0 to OFF
        status = False
    elif mode == 'solar':
            if sunalt > 20 and sunangle > 90 and sunangle < 180:
                wiringpi.digitalWrite(0, 1) # sets port 0 to ON
                status = True
            else:
                wiringpi.digitalWrite(0, 0) # sets port 0 to OFF
                status = False
    elif mode == 'off':
        wiringpi.digitalWrite(0, 0) # sets port 0 to OFF
        status = False
    elif mode == 'boost':
        if prevPumpMode == 'boost' and time.time() - booststart>3600:
            wiringpi.digitalWrite(0, 0) # sets port 0 to OFF
            status = False
            mode = 'auto'
        else:
            wiringpi.digitalWrite(0, 1) # sets port 0 to ON
            status = True
    elif mode == 'auto':
        now = datetime.now()
        if str(now.hour) in hours:
            wiringpi.digitalWrite(0, 1) # sets port 0 to ON
            status = True
        else:
            wiringpi.digitalWrite(0, 0) # sets port 0 to OFF
            status = False
    else:
        wiringpi.digitalWrite(0, 0) # sets port 0 to OFF
        status = False

    print("Current pump status : "+str(status))
    print("Current pump mode : "+mode)

  # If there has been a change in state save status

    if status != prevPumpStatus or mode != prevPumpMode:
        booststart = time.time()
        saveStatus(mode, status, booststart)
    else:
        print("No change in status so don't save")

    return status


def pumpUpdate1(mode1):
    sunalt,sunangle=sun()
    prevPumpMode1,prevPumpStatus1,booststart1=getStatus1()
    hours1 = getSchedule1()

    if mode1 == 'on':
        wiringpi.digitalWrite(2, 1) # sets port 2 to ON
        status1 = True
    elif mode1 == 'off':
        wiringpi.digitalWrite(2, 0) # sets port 2 to OFF
        status1 = False
    elif mode1 == 'solar':
            if sunalt > 20 and sunangle > 90 and sunangle < 180:
                wiringpi.digitalWrite(2, 1) # sets port 2 to ON
                status1 = True
            else:
                wiringpi.digitalWrite(2, 0) # sets port 2 to OFF
                status1 = False
    elif mode1 == 'off':
        wiringpi.digitalWrite(2, 0) # sets port 2 to OFF
        status1 = False
    elif mode1 == 'boost':
        if prevPumpMode1 == 'boost' and time.time() - booststart1>3600:
            wiringpi.digitalWrite(2, 0) # sets port 2 to OFF
            status1 = False
            mode1 = 'auto'
        else:
            wiringpi.digitalWrite(2, 1) # sets port 2 to ON
            status1 = True
    elif mode1 == 'auto':
        now = datetime.now()
        if str(now.hour) in hours1:
            wiringpi.digitalWrite(2, 1) # sets port 2 to ON
            status1 = True
        else:
            wiringpi.digitalWrite(2, 0) # sets port 2 to OFF
            status1 = False
    else:
        wiringpi.digitalWrite(2, 0) # sets port 2 to OFF
        status1 = False

    print("Current pump1 status : "+str(status1))
    print("Current pump1 mode : "+mode1)

  # If there has been a change in state save status

    if status1 != prevPumpStatus1 or mode1 != prevPumpMode1:
        booststart1 = time.time()
        saveStatus1(mode1, status1, booststart1)
    else:
        print("No change in status1 so don't save")

    return status1
