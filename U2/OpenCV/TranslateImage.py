import cv2 
import numpy as np
 
# read the image 
image = cv2.imread('image-15.png')
# get the width and height of the image
height, width = image.shape[:2]

# get tx and ty values for translation
# you can specify any value of your choice
# tx, ty = width / 4, height / 4
# tx, ty = 0, height / 2
# tx, ty = 0, -1 *(height / 2)
tx, ty = width, -1 *(height / 2)
 
# create the translation matrix using tx and ty, it is a NumPy array 
translation_matrix = np.array([
    [1, 0, tx],
    [0, 1, ty]
], dtype=np.float32)

# apply the translation to the image
translated_image = cv2.warpAffine(src=image, M=translation_matrix, dsize=(width, height))

# display the original and the Translated images
cv2.imshow('Original image', image)
cv2.imshow('Translated image', translated_image)
cv2.waitKey(0)
# save the translated image to disk
cv2.imwrite('translated_image.jpg', translated_image)