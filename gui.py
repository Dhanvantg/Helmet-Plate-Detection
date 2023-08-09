from PIL import Image, ImageTk


from tkinter import Tk, Label, Canvas, NW, Button, PhotoImage,ttk, Text, Frame
from tkinter import filedialog
import cv2


root = Tk()
root.title("HELMET DETECTOR")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
(root.geometry("%dx%d" % (w, h)))


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
    initial_y = h//4

    player = VideoPlayer(root, video_path, initial_x, initial_y)

    images = ["image1.png", "image2.png", "image3.png"]
    for i in images:
        plate = Image.open(i)
        plate = plate.resize((w // 2, h // 4))
        plate.save(i)
    current_image_index = 0
    image = PhotoImage(file=images[current_image_index])
    image_label = Label(root, image=image)
    image_label.place(x=w//2, y=0)


    images_new = ["image.png", "img1.png", "img2.png"]
    for i in images_new:
        plate1 = Image.open(i)
        plate1 = plate1.resize((w // 2, h // 4))
        plate1.save(i)
    img = PhotoImage(file=images_new[current_image_index])
    border_color = Frame(root, background="red")
    img_label = Label(root, image=img,border_color,)
    img_label.place(x=w//2, y=h//4)


    button = Button(root, text="back",command=back)
    button.place(x=w*3//4 - 100, y=h*3//4+50, width=100, height=30)
    button1 = Button(root, text="next", command=next)
    button1.place(x=w*3//4 + 100, y=h*3//4+50, width=100, height=30)

    '''plate = Image.open('image.png')
    plate = plate.resize((w // 2, h // 4))
    plate.save('image.png')
    image2 = PhotoImage(file="image.png")
    image_lab = Label(root, image=image2)
    image_lab.place(x=w//2, y=0)'''


    text_box = Text(root, height=5, width=40, bg="light cyan")
    text_new= ["KL01 BR 8055","ABCD012","DL4C AF 4943"]

    text_box.insert("1.0", text_new[current_image_index])
    text_box.place(x=w*5//8+100, y=h*5//8)

    root.mainloop()


