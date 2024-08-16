# Import dependancies
import cv2
 
maxScaleUp = 100
scaleFactor = 1
windowName = "Resize Image"
trackbarValue = "Scale"
 
# read the image
image = cv2.imread("test.jpg")
 
# Create a window to display results and  set the flag to Autosize
cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
 
def drawCircle(action, x, y , flags, *userdata):
  # Referencing global variables 
  global top_left_corner, bottom_right_corner
  # Mark the top left corner when left mouse button is pressed
  if action == cv2.EVENT_LBUTTONDOWN:
    top_left_corner = [(trackbarValue, trackbarValue)]
    # When left mouse button is released, mark bottom right corner
  elif action == cv2.EVENT_LBUTTONUP:
    bottom_right_corner = [(trackbarValue, trackbarValue)]    
    # Draw the rectangle
    cv2.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0,255,0),2, 8)
    # highgui function called when mouse events occur
    cv2.setMouseCallback("Window", drawCircle) 
    cv2.imshow("Window",image)

# Callback functions
def scaleImage(*args):
    # Get the scale factor from the trackbar 
    scaleFactor = 1+ args[0]/100.0

    # Resize the image
    scaledImage = cv2.resize(image, None, fx=scaleFactor, fy = scaleFactor, interpolation = cv2.INTER_LINEAR)
    cv2.imshow(windowName, scaledImage)
 
# Create trackbar and associate a callback function
cv2.createTrackbar(trackbarValue, windowName, scaleFactor, maxScaleUp, scaleImage)



# Display the image
cv2.imshow(windowName, image)
c = cv2.waitKey(0)
cv2.destroyAllWindows()