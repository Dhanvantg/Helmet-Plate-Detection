from PIL import Image, ImageTk
from tkinter import Tk, Label, Canvas, NW, Button, PhotoImage,ttk, Text, Frame, filedialog
import cv2
import keras_ocr
from tensorflow.keras.models import load_model
import numpy as np
import imutils
from detect import detect_helmet
from threading import *

root = Tk()
root.title("HELMET DETECTOR")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
(root.geometry("%dx%d" % (w, h)))

net = cv2.dnn.readNet("yolov3-custom_7000.weights", "yolov3-custom.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

pipeline = keras_ocr.pipeline.Pipeline()

model = load_model('helmet-nonhelmet_cnn.h5')
print('model loaded!!!')
imgf = ''

def select_file():
    global imgf, imag_label, images, images_new, text_new
    filetypes = (
        ('Image files', '*.jpg'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Select Image',
        initialdir='assets/',
        filetypes=filetypes)
    images = []
    images_new = []
    text_new = []
    imgf = filename
    print('updated', imgf)
    frm = Image.open(imgf)
    frm = frm.resize((w // 2, h // 2))
    frm.save('temp.png')
    imag = PhotoImage(file='temp.png')
    imag_label.configure(image=imag)
    imag_label.image = imag

if __name__ == "__main__":
    n = 1
    gap = True
    def update():
        global n, gap, imgf, imag_label, image_label, img_label
        imag = Image.open('select.png')
        imag = imag.resize((w // 2, h // 2))
        imag.save('select.png')
        imag = PhotoImage(file='select.png')
        imag_label = Label(root, image=imag, borderwidth=0)
        imag_label.place(x=0, y=0)
        while True:
            if imgf == '':
                continue
            fr = cv2.imread(imgf)
            detection = detect_helmet(fr, n, gap, model, pipeline, output_layers, net)
            if detection is None:
                img = 'temp.png'
                img1 = 'nilp.png'
                img2 = 'nilp.png'
                text_box.delete("1.0", 'end')
            elif len(detection) == 3:
                img, n, gap = detection
                img1 = 'nilp.png'
                img2 = 'nil.png'
                text_box.delete("1.0", 'end')
            elif len(detection) == 6:
                global face, text
                face, plate, text, img, n, gap = detection
                img1 = face
                img2 = plate
                text_box.insert("1.0", text)
            else:
                print('what')
                continue

            head = Image.open(img1)
            head = head.resize((h // 4, h // 4))
            head.save(img1)
            plt = Image.open(img2)
            plt = plt.resize((w // 2, h // 4))
            plt.save(img2)

            frm = Image.open(img)
            frm = frm.resize((w // 2, h // 2))
            frm.save(img)

            imag = PhotoImage(file=img)
            imag_label.configure(image=imag)
            imag_label.image = imag
            imgf = ''
            imag = PhotoImage(file=img1)
            image_label.configure(image=imag)
            image_label.image = imag
            imag = PhotoImage(file=img2)
            img_label.configure(image=imag)
            img_label.image = imag

    image = PhotoImage(file='nilp.png')
    image_label = Label(root, image=image, borderwidth=0)
    image_label.place(x=w//2 + h // 4, y=0)
    img = PhotoImage(file='nilp.png')
    img_label = Label(root, image=img, borderwidth=0)
    img_label.place(x=w//2, y=h//4)


    button = Button(root, text="Select Image",command=select_file)
    button.place(x=w//2 - 50, y=h*3//4+50, width=100, height=30)

    text_box = Text(root, height=5, width=40, bg="light grey")
    text_box.place(x=w//2-150, y=h*5//8)

    t1 = Thread(target=update)
    t1.start()
    root.configure(bg='#10375A')
    root.mainloop()
