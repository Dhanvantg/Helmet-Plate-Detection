from PIL import Image, ImageTk


from tkinter import Tk, Label, Canvas, NW, Button, PhotoImage,ttk
from tkinter import filedialog
import cv2

root = Tk()
root.title("HELMET DETECTOR")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

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




if __name__ == "__main__":


    video_path = "bs.mp4"
    initial_x = 0
    initial_y = 0

    player = VideoPlayer(root, video_path, initial_x, initial_y)

    person = Image.open('image.png')
    person = person.resize((w//2, h//2))
    person.save('image.png')
    image = PhotoImage(file = 'image.png')
    image_label = Label(root, image=image)
    image_label.place(x=0, y=h//2)

    button = Button(root, text="back")
    button.place(x=w*3//4 - 100, y=h*3//4 - 30, width=100, height=30)
    button1 = Button(root, text="next")
    button1.place(x=w*3//4 + 100, y=h*3//4 - 30, width=100, height=30)

    plate = Image.open('image2.png')
    plate = plate.resize((w // 2, h // 4))
    plate.save('image2.png')
    image2 = PhotoImage(file="image2.png")
    image_lab = Label(root, image=image2)
    image_lab.place(x=w//2, y=0)

    button3 = Button(root, text="back")
    button3.place(x=w*3//4 - 100, y=h*3//4 + 30, width=100, height=30)
    button4 = Button(root, text="next")
    button4.place(x=w*3//4 + 100, y=h*3//4 + 30, width=100, height=30)

    

    root.mainloop()


