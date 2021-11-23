#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import shutil
from datetime import datetime, timedelta
import os
import pytz

os.chdir('/home/boto/newsnowmap')

utc_now = pytz.utc.localize(datetime.utcnow())
cet_now = utc_now.astimezone(pytz.timezone("Europe/Prague"))

try:
    with open('./data/downloaded', 'r') as f:
        for line in f:
            pass
        last = line.strip()
except FileNotFoundError:
    last = datetime.strftime(utc_now - timedelta(days=3), '%Y%m%d.%H00')

last_img_dt = pytz.timezone("UTC").localize(datetime.strptime(last, '%Y%m%d.%H%M'))
current_dt = utc_now

while current_dt > last_img_dt:
    new_img_dt = last_img_dt + timedelta(hours=1)
    new_dt = datetime.strftime(new_img_dt, '%Y%m%d.%H%M')
    img = requests.get('http://www.shmu.sk/data/dataradary/data.1hrain/pcp.1h.'+new_dt+'.0.png', stream=True)
    if img.status_code != 200:
        last_img_dt = new_img_dt
        continue
    else:
        img.raw.decode_content = True
        with open('./images/pcp.1h.'+new_dt+'.0.png','wb') as f:
            shutil.copyfileobj(img.raw, f)
        with open('./data/downloaded', 'a') as f:
            f.write(new_dt+'\n')
        last_img_dt = new_img_dt

print('Download done!', datetime.utcnow(), 'UTC')
