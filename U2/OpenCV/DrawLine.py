# Import dependencies
import cv2

# Read Images
img = cv2.imread('sample.jpg')
# Display Image
cv2.imshow('Original Image',img)
cv2.waitKey(0)
# Print error message if image is null
if img is None:
    print('Could not read image')
# Draw line on image
imageLine = img.copy()
# Draw the image from point A to B
pointA = (200,80)
pointB = (450,80)
cv2.line(imageLine, pointA, pointB, (0, 255, 0), thickness=3, lineType=cv2.LINE_AA)

# define the center of circle
circle_center = (415,190)
# define the radius of the circle
radius =100
#  Draw a circle using the circle() Function
cv2.circle(imageLine, circle_center, radius, (0, 0, 255), thickness=3, lineType=cv2.LINE_AA) 

start_point =(300,115)
end_point =(475,225)
# draw the rectangle
cv2.rectangle(imageLine, start_point, end_point, (255, 0, 255), thickness= 3, lineType=cv2.LINE_8) 

# define the center point of ellipse
ellipse_center = (415,190)
# define the major and minor axes of the ellipse
axis1 = (100,50)
axis2 = (125,50)
# draw the ellipse
#Horizontal
cv2.ellipse(imageLine, ellipse_center, axis1, 90, 0, 360, (255, 255, 255), thickness=-1)
#Vertical
cv2.ellipse(imageLine, ellipse_center, axis2, 90, 0, 360, (0, 0, 0), thickness=-1)
# display the output

#let's write the text you want to put on the image
text = 'I am a Happy dog!'
#org: Where you want to put the text
org = (50,350)
# write the text on the input image
cv2.putText(imageLine, text, org, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.5, color = (250,225,100))
# display the output image with text over it

# Display the result
cv2.imshow('Image Line', imageLine)
cv2.waitKey(0)

cv2.destroyAllWindows()
