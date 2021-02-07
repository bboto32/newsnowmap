#!/bin/sh

cd ~/snowfall

./src/download_snowfall_images.py >> ~/cron.log 2>&1
./src/images_to_volume.py >> ~/cron.log 2>&1
