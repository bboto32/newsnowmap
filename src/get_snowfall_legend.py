import cv2

img = cv2.imread('./static/data.1hrain.png')

img_cr = img[12:30, 52:892, :]

n_color = 21
color_len = img_cr.shape[1] // n_color

img_sample = img_cr[8:9, 20::40, :]
colors_legend = [.1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 50, 65, 80, 95, 110]

cv2.imwrite('./static/colors.png', img_sample)

