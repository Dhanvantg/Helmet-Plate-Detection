import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np
import keras_ocr
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'false'

#cap = cv2.VideoCapture(r"asmall.mp4")
COLORS = [(0, 255, 0), (0, 0, 255)]

#fourcc = cv2.VideoWriter_fourcc(*"XVID")
#writer = cv2.VideoWriter('output.avi', fourcc, 5, (888, 500))


def detect_helmet(img, n, gap, model, pipeline, output_layers, net):
    if img is None:
        print('EMPTY')
        return
    #cv2.imshow('TEST', img)
    #time.sleep(5)
    img = imutils.resize(img, height=500)
    # img = cv2.imread('test.py.png')
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
            #print(boxes[i])
            x, y, w, h = boxes[i]
            color = [int(c) for c in COLORS[classIds[i]]]
            # green --> bike
            # red --> number plate
            if classIds[i] == 0:  # bike
                pass
                # helmet_roi = img[max(0, y):max(0, y) + max(0, h) // 4, max(0, x):max(0, x) + max(0, w)]
            else:  # Helmet Detection
                x_h = x
                y_h = y - 400
                w_h = w + 300
                h_h = h + 300
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 7)
                # h_r = img[max(0,(y-330)):max(0,(y-330 + h+100)) , max(0,(x-80)):max(0,(x-80 + w+130))]
                plate = img[y:y + h, x:x + w]
                cv2.imwrite('platemp.png', plate)
                if y_h > 0 and x_h > 0:
                    h_r1 = img[y_h:y_h + h_h, x_h:x_h + w_h]
                    #cv2.imshow('helmet', h_r)
                    # Helmet Detection
                    try:
                        h_r = cv2.resize(h_r1, (224, 224))
                        h_r = np.array(h_r, dtype='float32')
                        h_r = h_r.reshape(1, 224, 224, 3)
                        h_r = h_r / 255.0
                        c = int(model.predict(h_r)[0][0])
                    except:
                        c = None
                    if c == 0:
                        print("NO HELMET!")
                        images = [keras_ocr.tools.read('platemp.png')]
                        prediction_groups = pipeline.recognize(images)
                        print(prediction_groups)
                        cv2.imwrite('plate'+str(n)+'.png', plate)
                        cv2.imwrite('face' + str(n) + '.png', h_r1)
                        text = ''
                        for i in prediction_groups[0]:
                            text += i[0]
                        gap = False
                        cv2.imwrite('temp.png', img)
                        return 'face' + str(n) + '.png', 'plate'+str(n)+'.png', text, 'temp.png', n+1, gap
                    else:
                        gap = True
                    cv2.putText(img, ['helmet', 'no-helmet'][c], (x, y - 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),
                                2)
                    cv2.rectangle(img, (x_h, y_h), (x_h + w_h, y_h + h_h), (255, 0, 0), 10)
                cv2.imwrite('temp.png', img)
                return 'temp.png', n+1, gap
    cv2.imwrite('temp.png', img)


    #writer.write(img)
    #try:
        #cv2.imshow("Image", img)
    #except:
        #pass

    #if cv2.waitKey(1) == 27:
        #break

#writer.release()
#cap.release()
#cv2.waitKey(0)
#cv2.destroyAllWindows()
# https://machinelearningprojects.net/helmet-and-number-plate-detection-and-recognition/
# https://drive.google.com/file/d/1o3i0VhhTjImEAl260M3EoMU5WNpRM-s1/view?usp=sharing
# https://drive.google.com/file/d/1NztDuFsjdHgkMskSKn4Dj_O2jEGKnllo/view?usp=sharing
# https://drive.google.com/file/d/1RySiJvPIRsA-fio9_ViGzS8OZg1eymPg/view?usp=sharing