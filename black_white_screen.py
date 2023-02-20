import cv2
import numpy as np
import time
from time import time
from test_programs.new_wincap import wincap

def convert_BW(image):

    # convert image to grayscale
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # convert image to black and white

    thresh, image_black = cv2.threshold(image_grayscale, 48, 255, cv2.THRESH_BINARY)

    # download images
    # cv2.imwrite('yes.png', image_black)
    # cv2.imwrite('image_black.png', image_black)

    return image_black

def remove_background(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Filter using contour area and remove small noise
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    #find the largest "block" and remove the rest
    cnts = list(cnts)
    cnts.sort(key=lambda x: cv2.contourArea(x))
    largest = cv2.contourArea(cnts[-1])

    for c in cnts:
        area = cv2.contourArea(c)
        if area == largest:
            continue
        cv2.drawContours(thresh, [c], -1, (0, 0, 0), -1)

    # Morph close and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    close = 255 - cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    return close


def find_corners(image):
    corners = cv2.goodFeaturesToTrack(image, 4, 0.3, 10)
    corners = np.int0(corners)

    # color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    raveled_corners = []

    for ind, corner in enumerate(corners):
        x, y = corner.ravel()
        raveled_corners.append([x, y])

    return raveled_corners


def main():
    # get BW image
    # image_file = "4.png"

    loop_time = time()
    while (True):
        #take screenshot of window(change accordingly)
        screenshot = wincap("VALORANT_")

        #convert image using functions
        image = convert_BW(screenshot)
        image = remove_background(image)

        #print FPS
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        #display image
        cv2.imshow('Computer Vision', image)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            print("hi")
            break

#run code
if __name__ == "__main__":
    main()

