import cv2
import numpy as np

img = cv2.imread('car.jpg')

pts1 = np.float32([[0, 0], [0, 442], [612, 442], [612, 0]])
pts2 = np.float32([[0, 0], [400, 100], [0, 600], [400, 500], ])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
output = cv2.warpPerspective(img, matrix, (600, 600))

cv2.imshow("image", output)
cv2.waitKey(0)
cv2.destroyAllWindows()