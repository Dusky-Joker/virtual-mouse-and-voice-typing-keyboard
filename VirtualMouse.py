import cv2
import numpy as np
import HandTrackingModule as htm
import mouse
import pyautogui
import time

pyautogui.FAILSAFE = False

wCam, hCam = 640, 360
smoothness = 2.5
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

wScr, hScr = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        cv2.rectangle(img, (50, 50), (wCam - 150, hCam - 150), [0, 0, 200], 1)

        fingers = detector.fingersUp()
        if fingers == [0, 1, 0, 0, 0]:
            x3 = np.interp(x1, (50, wCam-150), (0, wScr))
            y3 = np.interp(y1, (50, hCam-150), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothness
            clocY = plocY + (y3 - plocY) / smoothness

            pyautogui.moveTo(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1), 10, [0, 255, 255], cv2.FILLED)
            plocX, plocY = clocX, clocY

        if fingers == [0, 1, 1, 0, 0]:
            length, img, li = detector.findDistance(8, 12, img)
            if int(length) < 23:
                cv2.circle(img, (li[4], li[5]), 10, [0, 255, 0], cv2.FILLED)
                pyautogui.click()

        if fingers == [0, 1, 1, 1, 0]:
            length, img, li = detector.findDistance(8, 12, img)
            if int(length) < 23:
                cv2.circle(img, (li[4], li[5]), 10, [0, 255, 0], cv2.FILLED)
                pyautogui.rightClick()

        if fingers == [1, 1, 1, 0, 0]:
            length, img, li = detector.findDistance(8, 12, img)
            if int(length) < 23:
                cv2.circle(img, (li[4], li[5]), 10, [0, 255, 0], cv2.FILLED)
                pyautogui.doubleClick()

        if fingers == [1, 1, 0, 0, 1]:
            mouse.wheel(-1)

        if fingers == [0, 1, 0, 0, 1]:
            mouse.wheel(1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS: " + str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, [255, 0, 255], 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
