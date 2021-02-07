#!/usr/bin/python3

import cv2
import numpy as np
from datetime import datetime, timedelta
import os

os.chdir('/home/boto/snowfall')

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

# init #
# start_dt = datetime.strptime('20210115.0000', '%Y%m%d.%H%M')
# end_dt = datetime.strptime('20210115.0300', '%Y%m%d.%H%M')
# t = np.arange(start_dt, end_dt, timedelta(hours=1)).astype(datetime)
# snow_falls = np.zeros((len(t), 253, 490))
#
# i = 0
# for time in t:
#     new_dt = datetime.strftime(time, '%Y%m%d.%H%M')
#     img = cv2.imread('./images/pcp.1h.'+new_dt+'.0.png')
#     img = crop_img(img)
#     new_snow = img_to_matrix(img)
#     snow_falls[i, :, :] = new_snow
#     i += 1
#
# with open('./data/snowfalls.npy', 'wb') as f:
#     np.save(f, snow_falls)
# with open('./data/snowfalls_date.npy', 'wb') as f:
#     np.save(f, t)
#

with open('./data/snowfalls.npy', 'rb') as f:
    snow_falls = np.load(f, allow_pickle=True)
with open('./data/snowfalls_date.npy', 'rb') as f:
    t = np.load(f, allow_pickle=True)
with open('./data/downloaded', 'r') as f:
    for line in f:
        pass
    last = line.strip()

last_img_dt = t[-1]
max_img_dt = datetime.strptime(last, '%Y%m%d.%H%M')

while max_img_dt > last_img_dt:
    new_img_dt = last_img_dt + timedelta(hours=1)
    new_dt = datetime.strftime(new_img_dt, '%Y%m%d.%H%M')
    img = cv2.imread('./images/pcp.1h.'+new_dt+'.0.png')
    img = crop_img(img)
    new_snow = img_to_matrix(img)
    snow_falls = np.append(snow_falls, new_snow, axis=0)
    t = np.append(t, new_img_dt)
    last_img_dt = new_img_dt

with open('./data/snowfalls.npy', 'wb') as f:
    np.save(f, snow_falls)
with open('./data/snowfalls_date.npy', 'wb') as f:
    np.save(f, t)

print('Processing done!', datetime.now())
