#!/bin/sh

. ~/newsnowmap_env/bin/activate

cd ~/newsnowmap

./src/download_snowfall_images.py >> ./log/cron.log 2>&1
./src/images_to_volume.py >> ./log/cron.log 2>&1
