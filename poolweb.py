#!/usr/bin/python3
#-----------------------------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#     Pool Monitor System
#          poolweb.py
#
# This is the web front-end script.
#
# It serves a status page and allows users to set the
# pump mode and edit the schedule. If Alexa lines are
# uncommented then the system can respond to a suitable
# Skill.
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
#-----------------------------------------------------------
import time
import datetime
import logging
import hashlib
import config as c
import poollib as p
from flask import Flask,flash,jsonify,redirect,request,render_template,url_for,session,escape

logFormat='%(asctime)s %(levelname)s:%(message)s'
logging.basicConfig(format=logFormat,filename='/home/pi/pool/logs/web.log',level=logging.DEBUG)
logging.info('Web start')

mySensorIDs=[]
myPumpMode=''
myPumpStatus=False
myPumpMode1=''
myPumpStatus1=False

@app.route('/')
def index():
    global mySensorIDs
    if 'username' in session:
      temp1,temp2,temp3=p.readTemps(mySensorIDs,c.TEMPUNIT)
      sunalt,sunangle=p.sun()
      myPumpMode,myPumpStatus,timestamp=p.getStatus()
      myPumpMode1,myPumpStatus1,timestamp1=p.getStatus1()
      timeStamp='{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
      data={'t1': temp1,
            't2': temp2,
            't3': temp3,
            'sunalt': sunalt,
            'sunangle': sunangle,
            'tu': c.TEMPUNIT,
            'pm': myPumpMode,
            'pm1': myPumpMode1,
            'ps': myPumpStatus,
            'ps1': myPumpStatus1,
            'ts': timeStamp,
            'user': escape(session['username'])
            }
      return render_template('index.html',data=data)
    else:
      return redirect(url_for('login'))

@app.route('/on/')
def on():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode='on'
    myPumpStatus=p.pumpUpdate(myPumpMode)
    return redirect(url_for('index'))

@app.route('/on1/')
def on1():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode1='on'
    myPumpStatus1=p.pumpUpdate1(myPumpMode1)
    return redirect(url_for('index'))

@app.route('/off/')
def off():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode='off'
    myPumpStatus=p.pumpUpdate(myPumpMode)
    return redirect(url_for('index'))

@app.route('/off1/')
def off1():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode1='off'
    myPumpStatus1=p.pumpUpdate1(myPumpMode1)
    return redirect(url_for('index'))

@app.route('/auto/')
def auto():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode='auto'
    myPumpStatus=p.pumpUpdate(myPumpMode)
    return redirect(url_for('index'))

@app.route('/auto1/')
def auto1():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode1='auto'
    myPumpStatus1=p.pumpUpdate1(myPumpMode1)
    return redirect(url_for('index'))

@app.route('/solar/')
def solar():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode='solar'
    myPumpStatus=p.pumpUpdate(myPumpMode)
    return redirect(url_for('index'))

@app.route('/solar1/')
def solar1():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode1='solar'
    myPumpStatus1=p.pumpUpdate1(myPumpMode1)
    return redirect(url_for('index'))

@app.route('/boost/')
def boost():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode='boost'
    myPumpStatus=p.pumpUpdate(myPumpMode)
    return redirect(url_for('index'))

@app.route('/boost1/')
def boost1():
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    myPumpMode1='boost'
    myPumpStatus1=p.pumpUpdate1(myPumpMode1)
    return redirect(url_for('index'))

@app.route('/debug/')
def debug():
    temp1,temp2,temp3=p.readTemps(mySensorIDs,c.TEMPUNIT)
    sensorIDs=p.getSensorIDs()
    mode,status,booststart=p.getStatus()
    mode1,status1,booststart1=p.getStatus1()
    hours = p.getSchedule()
    hours1 = p.getSchedule1()
    timeStamp='{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    
    if mode=="boost":
      boostremain=3600+booststart-time.time()
    else:
      boostremain=0  

    if mode1=="boost":
      boostremain1=3600+booststart1-time.time()
    else:
      boostremain1=0
    
    data={'id1': sensorIDs[0],
          'id2': sensorIDs[1],
          'id3': sensorIDs[2],
          't1' : temp1,
          't2' : temp2,
          't3' : temp3,
          'tu' : c.TEMPUNIT,
          'pm' : mode,
          'pm1' : mode1,
          'ps' : status,
          'ps1' : status1,
          'hrs': hours,
          'hrs1': hours1,
          'ts' : timeStamp,
          'bt' : booststart,
          'bt1' : booststart1,
          'br' : boostremain,
          'br1' : boostremain1
         }
    return render_template('debug.html',data=data)

@app.route('/schedule/', methods=['GET','POST'])
def schedule():
    if request.method == 'POST':
        myHours = request.form.getlist("hours")
        p.saveSchedule(myHours)
        flash('Schedule saved','info')
    else:
      myHours=p.getSchedule()
    return render_template('schedule.html',hours=myHours)

@app.route('/schedule1/', methods=['GET','POST'])
def schedule1():
    if request.method == 'POST':
        myHours1 = request.form.getlist("hours1")
        p.saveSchedule1(myHours1)
        flash('Schedule saved','info')
    else:
      myHours1=p.getSchedule1()
    return render_template('schedule1.html',hours1=myHours1)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from submitted form
        userName=escape(request.form['username'])
        passWord=escape(request.form['password'])
        # Convert password to hash and compare to stored hash
        passWordHash=hashlib.sha256(passWord.encode('utf-8')).hexdigest()
        if userName==c.USERNAME and passWordHash==c.USERHASH:
          session['username']='admin'
          return redirect(url_for('index'))
        else:
          time.sleep(2)
          session.pop('username', None)
          flash('Sorry. Better luck next time.','danger')
    else:
      flash('Please enter your details.','info')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove username from the session
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/status')
def status():
    # Return temps and pump mode in Json format to any
    # system that calls the /status URL. e.g. Home Assistant
    global mySensorIDs,myPumpStatus,myPumpMode,myPumpStatus1,myPumpMode1
    temp1,temp2,temp3=p.readTemps(mySensorIDs,c.TEMPUNIT)
    
    if myPumpStatus==True:
        myPumpStatus="On"
    else:
        myPumpStatus="Off"

    if myPumpStatus1==True:
        myPumpStatus1="On"
    else:
        myPumpStatus1="Off"
    
    return jsonify(solarin=temp1,airtemp=temp2,solarout=temp3,pumpmode=myPumpMode,pumpstatus=myPumpStatus,pumpmode1=myPumpMode1,pumpstatus1=myPumpStatus1)

if __name__ == '__main__':
    mySensorIDs=p.getSensorIDs()
    myPumpMode,myPumpStatus,timestamp=p.getStatus()

    # Default Flask port
    flaskPort=5000

    app.run(host='0.0.0.0', port=flaskPort, debug=False)
