import cv2
import pathlib
cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
clf = cv2.CascadeClassifier(str(cascade_path))
def box(img):
    faces = clf.detectMultiScale(
        img,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    print(faces)
    if len(faces) > 0:
        return faces[0]