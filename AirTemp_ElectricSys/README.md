# Monitoring process:
## 1. $sudo crontab -e
-*$/sbin/shutdown -r now*: The RPi reboots every night at midnight.
-*$@reboot start_arduino.sh*: this script creates a file with the current date and launches picocom with a baudrate of 4800 and listens to serial port ttyACM0 (UART connection to Tarom 4545 charge controller via USB)

## 2. $ crontab -e
-*$@reboot measrue_arduino.sh && measure_tarom.sh*: Those scripts start stty and picocom to listen to ttyUSB0 and ttyACM0 and log their incoming communication (at a baudrate of 4800) to a file. The data is aquired through an arduino and the Steca Tarom 4545 charge controller. The arduino mega is connected to 14 DHT22 sensors and an RTC. It averages over one minute and sends the data to its serial connection. The Steca Tarom 4545 has an UART connection and is as well connected via USB to the RPi.
*Hint: both scripts are started multiple times in crontab and sudo crontab as it was hard to establish two serial connections and monitor them. Most of the times only one would have worked and monitored. As far as I understand, it is not possible to use stty and cat two times to monitor the serial connection. Hence, I used one time stty and one time picocom*

## 3. TerminalAir.sh
A autostart file (*.desktop) was created in /etc/xdg/autostart with $gnome-desktop-item --create-new.*
This launches the *TerminalAir.sh* shell script which launches *AirTempReader.py*.

## 4. TerminalPV.sh
A autostart file (*.desktop) was created in /etc/xdg/autostart with $gnome-desktop-item --create-new.*
This launches the *TerminalPV.sh* shell script which launches *PVReader.py*.

## 5. AirTempReader.py
*The main tutorial to create the python script has been: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/*
- the first while-loop is needed that the script doesn't fail any if the RPi cannot connect to the internet
- *config.json* file is loaded. It contains the login credentials to plot.ly and the streaming tokens (created on plot.ly under settings)
- streaming  is initialized and the plot is set-up. The number of maximum points is set to 1440 as the data is uploaded once a minute and a daily graph shall be displayed.
*hint: in the end, the filopt is set to "extend" so the graph is not reset with any new API call.*
- during  the *while-loop* the newest file in my log-folder for the monitoring of the connection to the arduino is opened.
- the last line (newest item) is read and each line is split at '; '
- the values 3 to 9 (temperature T_1 to T_7 of westward facing wall) are taken as float and send to plot.ly
- the *try-loop* this needed so the program is not aborted if the connection fails

## 6. PVReader
*equivalent to AirTempReader.py*
additionally within the *while-loop*:
- send http request to youless energy monitor. this monitors the electricity demand of the A/C, connected to the grid. It sends back the average power consumption of the last 30min.
- the loaded page is read by the script and split at every line break, every tab-stop and every empty space
- the second last element is the current electricity consumption which is send to plot.ly
*the youless energy monitor http request is documented here: http://wiki.td-er.nl/index.php?title=YouLess*


## 7. dropbox.sh
*The tutorial to connect to dropbox with raspbian is located here: http://raspi.tv/2013/how-to-use-dropbox-with-raspberry-pi*
It is neccessary to create a dropbox developer API.
This scrip uploads the newest file in my logging folder to my dropbox as a backup.
