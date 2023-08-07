import cv2
import numpy as np
from PIL import Image
import imutils
from tensorflow.keras.models import load_model
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'false'

net = cv2.dnn.readNet("yolov3-custom_7000.weights", "yolov3-custom.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

model = load_model('helmet-nonhelmet_cnn.h5')
print('model loaded!!!')
cap = cv2.VideoCapture(r"1.mp4")
COLORS = [(0, 255, 0), (0, 0, 255)]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

fourcc = cv2.VideoWriter_fourcc(*"XVID")
writer = cv2.VideoWriter('output.avi', fourcc, 5, (888, 500))


def helmet_or_nohelmet(helmet_roi):
    try:
        helmet_roi = cv2.resize(helmet_roi, (224, 224))
        helmet_roi = np.array(helmet_roi, dtype='float32')
        helmet_roi = helmet_roi.reshape(1, 224, 224, 3)
        helmet_roi = helmet_roi / 255.0
        return int(model.predict(helmet_roi)[0][0])
    except:
        pass


ret = True

while True:

    ret, img = cap.read()
    if img is None:
        print('EMPTY')
        continue
    #cv2.imshow('TEST', img)
    #time.sleep(5)
    img = imutils.resize(img, height=500)
    # img = cv2.imread('test.png')
    height, width = img.shape[:2]

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    confidences = []
    boxes = []
    classIds = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                classIds.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            print(boxes[i])
            x, y, w, h = boxes[i]
            color = [int(c) for c in COLORS[classIds[i]]]
            # green --> bike
            # red --> number plate
            if classIds[i] == 0:  # bike
                helmet_roi = img[max(0, y):max(0, y) + max(0, h) // 4, max(0, x):max(0, x) + max(0, w)]
            else:  # number plate
                x_h = x - 60
                y_h = y - 350
                w_h = w + 100
                h_h = h + 100
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 7)
                # h_r = img[max(0,(y-330)):max(0,(y-330 + h+100)) , max(0,(x-80)):max(0,(x-80 + w+130))]
                plate = img[y:y + h, x:x + w]
                #cv2.imshow('BOZ', h_n)
                if y_h > 0 and x_h > 0:
                    h_r = img[y_h:y_h + h_h, x_h:x_h + w_h]
                    c = helmet_or_nohelmet(h_r)
                    if c == 0:
                        text = pytesseract.image_to_string(plate)
                        print(text)
                        cv2.imwrite(text+'.png', plate)
                    cv2.putText(img, ['helmet', 'no-helmet'][c], (x, y - 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),
                                2)
                    cv2.rectangle(img, (x_h, y_h), (x_h + w_h, y_h + h_h), (255, 0, 0), 10)

    writer.write(img)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break

writer.release()
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
# https://machinelearningprojects.net/helmet-and-number-plate-detection-and-recognition/
# https://drive.google.com/file/d/1o3i0VhhTjImEAl260M3EoMU5WNpRM-s1/view?usp=sharing