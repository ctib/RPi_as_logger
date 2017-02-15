#! /bin/bash

#file_Room=$(date +%Y%m%d_%H-%M-%S)-Room

#echo "$file_Room"

picocom -b 4800 -c -r -l /dev/ttyACM0

#echo "picocom arduino started"

#sleep 2
#cat /dev/ttyACM0 > /your/arduino/directory/$file_Room.txt &

#echo "capturing arduino started"