import cv2
import numpy as np

im = cv2.imread('two-cubes.png')
print(im.shape)
bright = im[22:300,0:300]
dark = im[22:300,301:601]
print(bright.shape, dark.shape)
cv2.imshow('Original', im)
cv2.imshow('Clara', bright)
cv2.imshow('Oscura', dark)

b1,g1,r1 = cv2.split(bright)
b2,g2,r2 = cv2.split(dark)

vis1 = np.concatenate((b1, g1, r1), axis=1)
vis2 = np.concatenate((b2, g2, r2), axis=1)
vis3 = np.concatenate((vis1, vis2), axis=0)

cv2.imshow("Mosaico", vis3)

cv2.waitKey()