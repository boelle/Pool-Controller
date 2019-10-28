# Pool Monitor #

The Pool Monitor allows you measure the air and water temperature (both in and outlet in case of heating the water) while also controlling 2 pumps.

Using the web interface you can :
* Turn the pump on
* Turn the pump off
* "Boost" the pump which turns it on for 1 hour
* Put the system into "Auto" which turns the pump on and off based on a customisable schedule
* Edit the schedule
* Let it be controlled by the sun, so pump comes on when sun hits a solar heating system

## Equipment Required ##

* Raspberry Pi Zero W
* microSD card
* 5V power supply
* 3 DS18B20 temperature sensors (waterproof with cable)
* 4.7Kohm resistor
* Relay board to control the pump
* 3-wire (mains) Extension cable (you want the earth/ground wire don't you?)
* Weather proof garden electrical box
* Pool with water

## Optional Services Used ##
The following services can be used with this project if required :

* Duckdns to provide a stable URL by which you can connect to the web interface from the Internet

## Installation & Setup ##

This project has been documented in more detail on [https://www.raspberrypi-spy.co.uk/](https://www.raspberrypi-spy.co.uk/2017/07/pool-temperature-monitoring-and-pump-control-with-the-pi-zero-w/)

## Bootstrap ##
To render the web interface this project uses Bootstap. This includes a JS file and CSS file taken from v4.1.1. More details about Bootstrap can be found on their site : https://getbootstrap.com/
