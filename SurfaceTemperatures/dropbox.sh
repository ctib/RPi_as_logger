#! /bin/bash

cd /your/logging/directory
newest_file_surf=$(ls -tr|tail -n 1)

echo "$newest_file_surf"

/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /path/to/your/logging/directory/$newest_file_surf /$newest_file_surf