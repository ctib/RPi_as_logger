#Monitoring of Building and System Performance
### Using the raspberry-pi as logging and monitoring interface through plot.ly

### 1. Used components
The whole system components are presented on http://www.spacs.info.
There, the distribution of the sensors is shown as well as the electric and cold air supply system.
####Sensors:
- 14x DHT22 temperature and humidity sensors
- 3x TMP006 contactless sureface temperature sensors
- 1x DS1302 real time clock
- 1x youless energy monitor
- 1x netatmo weather station
- 1x Steca Tarom 4545

####Processing equipment
- Arduino Mega 2560
- 2x raspberry-pi with raspbian
- plot.ly

### 2. Surface temperatures
one raspberry-pi is used to monitor the surface temperature of the vaulted ceiling. The used scripts are in the folder /SurfaceTemperatures
The core is a python script which is reading the TMP006 contactless temperature sensors. The readings are averaged over a minute and send to plot.ly afterwards. The resulting plot is embedded to spacs.info.
The data is backed up in a file and uploaded once per hour to dropbox.

### 3. Air temperature
A second raspberry-pi is used to send the minutely averaged values of the room air temperatures and humidity to plot.ly. The readings of the DHT22 sensors are taken by an Arduino Mega 2560 and transferred via USB serial communication. The data is logged within a file and backed up to dropbox.com once an hour.

### 4. Electric system readings
The second raspberry-pi is also used to get the minutely readings from the Steca Tarom 4545. They are connected through an UART serial communication over USB. Incoming data is logged in a file. This data is as well backed up to dropbox once an hour.
