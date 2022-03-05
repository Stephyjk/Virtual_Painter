import cv2
import numpy as np
import os
import time
import HandTrackingModule as htm

folderPath = 'Painter'
myList = os.listdir(folderPath)

overlayList = []
eraserThickness = 100
brushThickness = 15

for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)

header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
xp, yp = 0, 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # fing hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            if y1 < 125:
                if 330 < x1 < 430:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                if 570 < x1 < 665:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                if 840 < x1 < 920:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                if 1130 < x1 < 1205:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),
                          drawColor, cv2.FILLED)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2. threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # setting the header image
    img[0:125, 0:1280] = header
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow('img', img)
    # cv2.imshow('imgCanvas', imgCanvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
