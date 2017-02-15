#! /bin/bash

cd /your/arduino/directory/
newest_file_room=$(ls -tr|tail -n 1)

#echo "$newest_file_room"

/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /your/arduino/directory/$newest_file_room /dropboxdirectory/$newest_file_room

cd /your/tarom/directory
newest_file_sys=$(ls -tr|tail -n 1)

#echo "$newest_file_sys"

/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /your/tarom/directory/$newest_file_sys /dropboxdirectory/$newest_file_sys
