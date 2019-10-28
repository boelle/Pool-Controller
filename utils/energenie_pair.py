#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
# Script to pair Energenie PiMote with Energenie sockets
# Only need to do this once.
#
# This is heavily based on the script in the official
# ENER314 Raspberry Pi RF-Transmitter Board User Manual
#
# Author : Matt Hawkins
# Date   : 07/08/2017
#
# http://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Import modules

import RPi.GPIO as GPIO
import time
import sys


def getSocketID(args):
    if len(args) != 2:

    # Default to 1 if no command line argument

        socketID = 1
    else:

    # Get command line argument
    # Default to 1 if invalid

        try:
            socketID = int(args[1])
            if socketID > 5:
                socketID = 4
            if socketID < 1:
                socketID = 1
        except:
            socketID = 1

    return socketID


def sendSocketCode(
    D3,
    D2,
    D1,
    D0,
    ):

  # Set D0-D3

    GPIO.output(17, D0)
    GPIO.output(22, D1)
    GPIO.output(23, D2)
    GPIO.output(27, D3)

  # let it settle, encoder requires this

    time.sleep(0.1)

  # Enable the modulator

    GPIO.output(25, True)

  # keep enabled for a period

    time.sleep(0.25)

  # Disable the modulator

    GPIO.output(25, False)


# set the pins numbering mode

GPIO.setmode(GPIO.BCM)

# Select the GPIO pins used for the encoder D0-D3 data inputs

GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

# Select GPIO used to select ASK/FSK (default ASK)

GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

# Select GPIO used to enable/disable modulator (default disabled)

GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)

# Here are the codes required for each socket
# True = '1', False ='0'

print 'To put socket in learning mode press the green button'
print 'for 5 seconds or more until the red light flashes slowly'
print 'The socket is now listening for a control code to be sent.'
print 'It will accept the following codes D3:D2:D1:D0'
print '  1011 and 0011 all ON and OFF'
print '  1111 and 0111 socket 1'
print '  1110 and 0110 socket 2'
print '  1101 and 0101 socket 3'
print '  1100 and 0100 socket 4\n'

try:
    input('Press ENTER to continue\n')
except:
    pass

try:
    socketID = getSocketID(sys.argv)

    print '' + str(socketID)

    if socketID == 1:
        print 'Pair as socket 1'
        sendSocketCode(True, True, True, True)
    elif socketID == 2:
        print 'Pair as socket 2'
        sendSocketCode(True, True, True, False)
    elif socketID == 3:
        print 'Pair as socket 3'
        sendSocketCode(True, True, False, True)
    elif socketID == 4:
        print 'Pair as socket 4'
        sendSocketCode(True, True, False, False)
    else:

    # Test mode

        print 'Testing all 4 sockets'
        print 'Sockets all OFF'
        sendSocketCode(False, False, True, True)  # All OFF
        time.sleep(3)
        print 'Socket 1 ON'
        sendSocketCode(True, True, True, True)  # 1 ON
        time.sleep(2)
        print 'Socket 2 ON'
        sendSocketCode(True, True, True, False)  # 2 ON
        time.sleep(2)
        print 'Socket 3 ON'
        sendSocketCode(True, True, False, True)  # 3 ON
        time.sleep(2)
        print 'Socket 4 ON'
        sendSocketCode(True, True, False, False)  # 4 ON
        time.sleep(3)
        print 'Sockets all OFF'
        sendSocketCode(True, False, True, True)  # All OFF

    GPIO.cleanup()
except KeyboardInterrupt:

# Clean up the GPIOs for next time

    GPIO.cleanup()
