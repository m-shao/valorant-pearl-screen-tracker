from tkinter import Tk, Canvas, PhotoImage, NW
import cv2
from PIL import Image, ImageTk


img = cv2.imread('car.jpg')

root = Tk()

root.attributes('-transparentcolor','#f0f0f0')

# Canvas
canvas = Canvas(root, width=1000, height=1000)
canvas.pack()

im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)

# Image
# image = PhotoImage(imgtk)

# Positioning the Image inside the canvas
canvas.create_image(0, 0, anchor=NW, image=imgtk)

# Starts the GUI
root.mainloop()