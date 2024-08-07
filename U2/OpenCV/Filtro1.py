import cv2
import numpy as np
 
image = cv2.imread('sample.jpg')
 
# Print error message if image is null
if image is None:
    print('Could not read image')
 
# Apply identity kernel
kernel1 = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])

kernel1 = np.array([[1/9, 1/9, 1/9],
                    [1/9, 1/9, 1/9],
                    [1/9, 1/9, 1/9]])
 
identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)

print(identity.shape)

cv2.imshow('Original', image)
cv2.imshow('Identity', identity)
     
cv2.waitKey()
cv2.imwrite('identity.jpg', identity)
cv2.destroyAllWindows()
 
# Apply blurring kernel
kernel2 = np.ones((5, 5), np.float32) / 25
img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)
 
cv2.imshow('Original', image)
cv2.imshow('Kernel Blur', img)
     
cv2.waitKey()
cv2.imwrite('blur_kernel.jpg', img)
cv2.destroyAllWindows()

"""
Apply sharpening using kernel
"""
kernel3 = np.array([[0, -1,  0],
                   [-1,  5, -1],
                    [0, -1,  0]])
sharp_img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel3)
 
cv2.imshow('Original', image)
cv2.imshow('Sharpened', sharp_img)
     
cv2.waitKey()
cv2.imwrite('sharp_image.jpg', sharp_img)