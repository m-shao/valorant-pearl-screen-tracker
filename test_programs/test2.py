import cv2
import numpy as np
import time
from time import time
import os
from new_wincap import wincap
from tkinter import Tk, Canvas, PhotoImage, NW
from PIL import Image, ImageTk

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
    corners = cv2.goodFeaturesToTrack(image, 4, 0.3, 50)
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
        screenshot = wincap("Medal")
        # image = cv2.imread('test_images/' + image_file, cv2.IMREAD_UNCHANGED)
        # image = cv2.imread(screenshot, cv2.IMREAD_UNCHANGED)
        image = convert_BW(screenshot)
        image = remove_background(image)

        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()
        corners = find_corners(image)

        img = cv2.imread('car.jpg')

        pts1 = np.float32([[0, 0], [0, 442], [612, 0], [612, 442]])

        corners_sorted = sorted(corners, key=lambda x: x[0])

        if len(corners_sorted) < 4:
            continue

        if corners_sorted[0][1] > corners_sorted[1][1]:
            corners_sorted.insert(0, corners_sorted.pop(1))
        if corners_sorted[2][1] > corners_sorted[3][1]:
            corners_sorted.insert(2, corners_sorted.pop(3))
        #
        # pip(corners_sorted)

        pts2 = np.float32(corners_sorted)
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        output = cv2.warpPerspective(img, matrix, (1900, 1060))

        root = Tk()

        root.attributes('-transparentcolor', '#f0f0f0')

        # Canvas
        canvas = Canvas(root, width=1900, height=1060)
        canvas.pack()

        im = Image.fromarray(output)
        imgtk = ImageTk.PhotoImage(image=im)

        # Image
        # image = PhotoImage(imgtk)

        # Positioning the Image inside the canvas
        canvas.create_image(0, 0, anchor=NW, image=imgtk)

        print("hi")
        # Starts the GUI
        root.mainloop()
        print("hi")

        # cv2.imshow("image", output)
        #
        # if cv2.waitKey(1) == ord('q'):
        #     cv2.destroyAllWindows()
        #     break

        #download image
        # cv2.imwrite('yes.png', image)
        #


        # show image
        # cv2.imshow('image.jpeg', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


main()

