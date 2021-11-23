import matplotlib
matplotlib.use('Agg')
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


def total_snow(start, end):
    start_d = datetime.strftime(start, '%Y%m%d')
    start_h = int(datetime.strftime(start, '%H'))
    end_d = datetime.strftime(end, '%Y%m%d')
    end_h = int(datetime.strftime(end, '%H'))

    actual = start
    if start_d == end_d: # if start and end is the same day
        with open('./data/snowfalls'+start_d+'.npy', 'rb') as f:
            snow_falls = np.load(f, allow_pickle=True)
        total_snow = np.sum(snow_falls[start_h:end_h+1], axis=0)
    else: # if start day < end day
        # part of first day #
        with open('./data/snowfalls'+start_d+'.npy', 'rb') as f:
            snow_falls = np.load(f, allow_pickle=True)
        total_snow = np.sum(snow_falls[start_h:], axis=0)

        # whole middle days #
        actual = actual + timedelta(days=1)
        while actual.date() < end.date():
            with open('./data/snowfalls'+datetime.strftime(actual, '%Y%m%d')+'.npy', 'rb') as f:
                snow_falls = np.load(f, allow_pickle=True)
            total_snow += np.sum(snow_falls, axis=0)
            actual = actual + timedelta(days=1)

        # part of last day #
        with open('./data/snowfalls'+datetime.strftime(actual, '%Y%m%d')+'.npy', 'rb') as f:
            snow_falls = np.load(f, allow_pickle=True)
        total_snow += np.sum(snow_falls[:end_h+1], axis=0)

    # handle outliers #
    max_snow = np.percentile(total_snow, 99.9)
    total_snow = np.clip(total_snow, 0, max_snow)

    return total_snow


def matrix_to_img(total_snow):

    # def generator #
    def get_pixels(img):
        for l in range(img.shape[0]):
            for w in range(img.shape[1]):
                yield l, w

    cmap = cm.jet
    norm = Normalize(vmin=np.min(total_snow), vmax=np.max(total_snow))
    img = np.zeros((total_snow.shape[0], total_snow.shape[1], 4))

    for l, w in get_pixels(img):
        if total_snow[l, w] == 0:
            continue
        img[l, w, :] = cmap(norm(total_snow[l, w]))

    # add frame #
    img[:, 0, 3] = 1
    img[:, -1, 3] = 1
    img[0, :, 3] = 1
    img[-1, :, 3] = 1

    return img


def save_img(img, name):
    fig = plt.figure(frameon=False)
    fig.set_size_inches(8, 5.5)

    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(img, aspect='auto')
    plt.savefig('./static/'+name, dpi=100)
    plt.close(fig)

def save_legend(total_snow, name):
    fig = plt.figure(figsize=(19, 1))
    ax1 = fig.add_axes([0.05, 0.5, 0.9, 0.4])
    cmap = cm.jet
    norm = Normalize(vmin=np.min(total_snow), vmax=np.max(total_snow))
    cb1 = matplotlib.colorbar.ColorbarBase(ax1, cmap=cmap,
                                           norm=norm,
                                           orientation='horizontal')
    cb1.set_label('cm')
    # ax1.xaxis.set_label_position('top')
    ax1.xaxis.tick_top()
    plt.savefig('./static/' + name + '_legend.png', bbox_inches='tight', transparent=True)

