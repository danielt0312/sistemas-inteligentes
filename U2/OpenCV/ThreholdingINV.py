# import opencv 
import cv2 

# Read image
src = cv2.imread("threshold.png", cv2.IMREAD_GRAYSCALE)
 
# Set threshold and maxValue
thresh = 0
maxValue = 255
 
# Basic threshold example
th, dst = cv2.threshold(src, thresh, maxValue, cv2.THRESH_BINARY)
th, dst2 = cv2.threshold(src, thresh, maxValue, cv2.THRESH_BINARY_INV)
th, dst3 = cv2.threshold(src, thresh, maxValue, cv2.THRESH_TRUNC)

src = cv2.imread("opencv-thresh-trunc.jpg")
cv2.imshow("Trunc", dst3)
cv2.imwrite("opencv-thresh-trunc.jpg", dst3)
cv2.imshow("Binary Inv", dst2)
