#! /bin/bash

file_Sys=$(date +%Y%m%d_%H-%M-%S)-Sys

#echo "$file_Sys"

stty -F /dev/ttyUSB0 4800

#picocom -b 4800 -c -r -l /dev/ttyUSB0

#sleep 5

cat /dev/ttyUSB0 > /your/tarom/directory/$file_Sys.txt

#echo "capturing started"

#echo "minicom started"