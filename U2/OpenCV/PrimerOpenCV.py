# import the cv2 library
import cv2
 
# The function cv2.imread() is used to read an image.
img_grayscale = cv2.imread('input.jpg',0)
 
# The function cv2.imshow() is used to display an image in a window.
cv2.imshow('graycsale image',img_grayscale)
 
# waitKey() waits for a key press to close the window and 0 specifies indefinite loop
cv2.waitKey(0)
 
# cv2.destroyAllWindows() simply destroys all the windows we created.
cv2.destroyAllWindows()
 
# The function cv2.imwrite() is used to write an image.
cv2.imwrite('grayscale.jpg',img_grayscale)


# img_grayscaleA = cv2.imread('input.jpg')
# img_grayscaleB = cv2.imread('input.jpg', 0)
# img_grayscaleC = cv2.imread('grayscale2.jpg', 0)

# print (img_grayscaleA.shape)
# print (img_grayscaleB.shape)
# print (img_grayscaleC.shape)

# img_grayscaleA[:, :] = (128, 128, 0)
# img_grayscaleC[:, :] = (255, 255, 0)

# cv2.imshow('grayscale image1', img_grayscaleA)
# cv2.imshow('grayscale image2', img_grayscaleC)

# cv2.waitKey(0)

# cv2.destroyAllWindows()