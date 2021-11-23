#!/usr/bin/env python

import cv2
import numpy as np
from datetime import datetime, timedelta
import os

os.chdir('/home/boto/newsnowmap')

# get new snow #
snow_colors = cv2.imread('./images/colors.png')[0, :, :].tolist()
# TODO: change volumes
color_to_volume = [0.3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 50, 65, 80, 95, 110]
# color_to_volume = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 50, 65, 80, 95, 110, 125]
# color_to_volume = [0.3, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 12.5, 17.5, 22.5, 27.5, 32.5, 42.5, 57.5, 72.5, 87.5, 102.5, 117.5]
dead_colors = [[0,0,0], [2,2,2], [216,216,216], [230,230,230], [239,239,0]]

def crop_img(img): # only Slovakia
    return img[115:368, 240:730, :]

def img_to_matrix(img):
    s1 = img.shape[0]
    s2 = img.shape[1]

    def get_pixels(img):
        for l in range(s1):
            for w in range(s2):
                yield l, w

    snowfall = np.zeros((1, s1, s2))
    for l, w in get_pixels(img):
        pixel = img[l, w, :].tolist()
        if pixel in dead_colors:
            continue
        else:
            try:
                snowfall[0, l, w] = color_to_volume[snow_colors.index(pixel)]
            except ValueError:
                print('New color detected with RGB:', pixel)
                print(l, w)
    return snowfall

# add new snow #
# TODO: convert snow to rain if temperature is above 0 degree Celsius

with open('./data/downloaded', 'r') as f:
    first_downl = f.readline().strip()
    for line in f:
        pass
    last_downl = line.strip()

try:
    with open('./data/processed', 'r') as f:
        for line in f:
            pass
        last_process = line.strip()
except FileNotFoundError:
    first_downl = datetime.strptime(first_downl, '%Y%m%d.%H%M')
    last_process = datetime.strftime(first_downl - timedelta(hours=1), '%Y%m%d.%H%M')

last_img_dt = datetime.strptime(last_process, '%Y%m%d.%H%M')
max_img_dt = datetime.strptime(last_downl, '%Y%m%d.%H%M')

while max_img_dt > last_img_dt:
    new_img_dt = last_img_dt + timedelta(hours=1)
    new_dt = datetime.strftime(new_img_dt, '%Y%m%d.%H%M')
    new_d = datetime.strftime(new_img_dt, '%Y%m%d')
    img = cv2.imread('./images/pcp.1h.'+new_dt+'.0.png')
    img = crop_img(img)
    new_snow = img_to_matrix(img)
    try:
        with open('./data/snowfalls'+new_d+'.npy', 'rb') as f:
            snow_falls = np.load(f, allow_pickle=True)
            snow_falls = np.append(snow_falls, new_snow, axis=0)
        with open('./data/snowfalls'+new_d+'.npy', 'wb') as f:
            np.save(f, snow_falls)
    except FileNotFoundError:
        with open('./data/snowfalls'+new_d+'.npy', 'wb') as f:
            np.save(f, new_snow)
    last_img_dt = new_img_dt

with open('./data/processed', 'a') as f:
    f.write(new_dt+'\n')

print('Processing done!', datetime.utcnow(), 'UTC')
