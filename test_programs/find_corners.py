import cv2
import numpy as np


image = cv2.imread('test_images/screen.png')
# image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 4, 0.3, 10)
corners = np.int0(corners)

for ind, corner in enumerate(corners):
    x, y = corner.ravel()
    corners[ind] = [x, y]
    cv2.circle(image, (x, y), 5, (255, 0, 0), -1)

print(corners)

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
