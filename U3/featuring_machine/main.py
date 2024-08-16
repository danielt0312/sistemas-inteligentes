import cv2
import numpy as np

# Load the images
img1 = cv2.imread('image1.png', 0)
img2 = cv2.imread('image2.png', 0)

# Detect keypoints and descriptors using ORB
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Initialize BFMatcher with Hamming distance
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors
matches = bf.match(des1, des2)

# Sort matches by distance (best matches first)
matches = sorted(matches, key=lambda x: x.distance)

# Draw matches with dark green color (BGR: (0, 100, 0))
img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None, matchColor=(0, 100, 0), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the matches
cv2.imshow("Window", img_matches)
cv2.waitKey(0)
cv2.destroyAllWindows()