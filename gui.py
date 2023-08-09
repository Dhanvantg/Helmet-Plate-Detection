from PIL import Image, ImageTk
from tkinter import Tk, Label, Canvas, NW, Button, PhotoImage,ttk, Text, Frame, filedialog
import cv2
import keras_ocr
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import matplotlib.pyplot as plt
from detect import detect_helmet
from threading import *

root = Tk()
root.title("HELMET DETECTOR")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
(root.geometry("%dx%d" % (w, h)))

images = ["nil.png"]  # , "image2.png", "image3.png"]
images_new = ["nilp.png"]  # , "img1.png", "img2.png"]
text_new = [""]  # ,"ABCD012","DL4C AF 4943"]

net = cv2.dnn.readNet("yolov3-custom_7000.weights", "yolov3-custom.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

pipeline = keras_ocr.pipeline.Pipeline()

model = load_model('helmet-nonhelmet_cnn.h5')
print('model loaded!!!')

class VideoPlayer:
    def __init__(self, root, video_path,initial_x,initial_y):
        self.root = root
        self.video_path = video_path
        self.initial_x = initial_x
        self.initial_y = initial_y

        self.video_capture = cv2.VideoCapture(video_path)
        self.video_width = w//2

        self.video_height = h//2

        self.canvas = Canvas(root, width=self.video_width, height=self.video_height)
        self.canvas.pack()

        self.play_video()

    def play_video(self):
        ret, frame = self.video_capture.read()
        img = Image.fromarray(frame)
        img = img.resize((w//2, h//2))
        if ret:
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
            self.canvas.place(x=self.initial_x, y=self.initial_y)
            self.root.after(10, self.play_video)


def next():
    global current_image_index
    global image_label
    global img_label
    print(images_new)
    current_image_index = (current_image_index + 1) % len(images)
    image = PhotoImage(file=images[current_image_index])
    image_label.configure(image=image)
    image_label.image = image

    img = PhotoImage(file=images_new[current_image_index])
    img_label.configure(image=img)
    img_label.image = img

    text_box.delete("1.0", "end")
    text_box.insert("1.0", text_new[current_image_index])

def back():
    global current_image_index
    global image_label
    global img_label

    current_image_index = (current_image_index -1) % len(images)
    image = PhotoImage(file=images[current_image_index])
    image_label.configure(image=image)
    image_label.image = image

    img = PhotoImage(file=images_new[current_image_index])
    img_label.configure(image=img)
    img_label.image = img

    text_box.delete("1.0", "end")
    text_box.insert("1.0", text_new[current_image_index])

if __name__ == "__main__":
    video_path = "video.mp4"
    initial_x = 0
    initial_y = 0
    cap = cv2.VideoCapture('asmall.mp4')
    #player = VideoPlayer(root, video_path, initial_x, initial_y)
    n = 1
    gap = True
    def update():
        global n, gap
        #global image, image_label
        imag = PhotoImage(file='load.png')
        imag_label = Label(root, image=imag)
        imag_label.place(x=0, y=0)
        while True:
            ret, fr = cap.read()
            detection = detect_helmet(fr, n, gap, model, pipeline, output_layers, net)
            if detection is None:
                print('none')
                continue
            elif len(detection) == 3:
                img, n, gap = detection
            elif len(detection) == 6:
                face, plate, text, img, n, gap = detection
                images.append(face)
                images_new.append(plate)
                text_new.append(text)
                head = Image.open(face)
                head = head.resize((w // 2, h // 4))
                head.save(face)
                num = Image.open(plate)
                num = num.resize((w // 2, h // 4))
                num.save(plate)

            else:
                print('what')
                continue

            frm = Image.open(img)
            frm = frm.resize((w // 2, h // 2))
            frm.save(img)
            imag = PhotoImage(file=img)
            imag_label.configure(image=imag)
            imag_label.image = imag
            #_label = Label(root, image=frm)
            #frm_label.place(x=0, y=0)
        #root.after(50, update)

    for i in images:
        plate = Image.open(i)
        plate = plate.resize((w // 2, h // 4))
        plate.save(i)
    current_image_index = 0
    image = PhotoImage(file=images[current_image_index])
    image_label = Label(root, image=image)
    image_label.place(x=w//2, y=0)

    for i in images_new:
        plate1 = Image.open(i)
        plate1 = plate1.resize((w // 2, h // 4))
        plate1.save(i)
    img = PhotoImage(file=images_new[current_image_index])
    border_color = Frame(root, background="red")
    img_label = Label(root, image=img)
    img_label.place(x=w//2, y=h//4)


    button = Button(root, text="back",command=back)
    button.place(x=w//2 - 150, y=h*3//4+50, width=100, height=30)
    button1 = Button(root, text="next", command=next)
    button1.place(x=w//2 + 50, y=h*3//4+50, width=100, height=30)

    '''plate = Image.open('image.png')
    plate = plate.resize((w // 2, h // 4))
    plate.save('image.png')
    image2 = PhotoImage(file="image.png")
    image_lab = Label(root, image=image2)
    image_lab.place(x=w//2, y=0)'''


    text_box = Text(root, height=5, width=40, bg="light grey")

    text_box.insert("1.0", text_new[current_image_index])
    text_box.place(x=w//2-150, y=h*5//8)

    t1 = Thread(target=update)
    t1.start()
    root.mainloop()
    print('hi')


