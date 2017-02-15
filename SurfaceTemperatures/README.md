# Monitoring process:
## 1. $sudo crontab -e
The RPi reboots every night at midnight.

## 2. TerminalTempReader.sh
A autostart file (*.desktop) was created in /etc/xdg/autostart with $gnome-desktop-item --create-new. 
This launches the *TerminalTempReader.sh* shell script which launches *TempReader.py*.

## 3. TempReader.py
*The main tutorial to create the python script has been: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/*
*The connected surface temperature sensors are TMP006 http://www.ti.com/lit/ds/symlink/tmp006.pdf which are connected via SDA and SCL to the RPi.*
- *config.json* file is loaded. It contains the login credentials to plot.ly and the streaming tokens (created on plot.ly under settings).
- streaming  is initialised and the plot is set-up. The number of maximum points is set to 1440 as the data is uploaded once a minute and a daily graph shall be displayed.
*hint: in the end, the filopt is set to "extend" so the graph is not resetted with any new API call.*
- during  the *while-loop* a file is created (or opened) from my logging folder, containing the current date
- the initial values are directly written (count of measurement and time)
- the second *while-loop* takes a measurement of each temperature sensor and adds them up for averaging
- after one minute has passed, the loop is left and the average values are created
*hint: as it seems the variation of the measurement is pretty high. Even with one minute average the temperatures are fluctuating by  +-0.5K. Maybe an average over 5min would work better.*
- the *try-loop* this needed so the program is not aborted if the connection fails

## 4. dropbox.sh
*The tutorial to connect to dropbox with raspbian is located here: http://raspi.tv/2013/how-to-use-dropbox-with-raspberry-pi*
It is neccessary to create a dropbox developer API.
This scrip uploads the newest file in my logging folder to my dropbox as a backup.