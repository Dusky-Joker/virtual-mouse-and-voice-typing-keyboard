import cv2
import numpy as np
import HandTrackingModule as htm
import VoiceRecognitonModule as vrm
import mouse
import pyautogui
import time

pyautogui.FAILSAFE = False

wCam, hCam = 640, 360
smoothness = 2.5
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
drag, pressed = False, False
ssc = 1

wScr, hScr = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
voice = vrm.voiceDetector()
mode = "Mouse"

while True:
    while mode == "Mouse":
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if lmList:
            cv2.rectangle(img, (100, 50), (wCam - 200, hCam - 150), [0, 0, 200], 1)

            fingers = detector.fingersUp()
            if detector.handType() == "Right":
                if fingers == [0, 1, 0, 0, 0]:
                    x1, y1 = lmList[8][1:]
                    x2 = np.interp(x1, (100, wCam - 200), (0, wScr))
                    y2 = np.interp(y1, (50, hCam - 150), (0, hScr))

                    clocX = plocX + (x2 - plocX) / smoothness
                    clocY = plocY + (y2 - plocY) / smoothness

                    pyautogui.moveTo(wScr - clocX, clocY)
                    cv2.circle(img, (x1, y1), 10, [0, 255, 255], cv2.FILLED)
                    plocX, plocY = clocX, clocY

                elif fingers == [0, 1, 1, 0, 0]:
                    length, img, li = detector.findDistance(8, 12, img)
                    if int(length) < 23:
                        cv2.circle(img, (li[4], li[5]), 10, [0, 255, 0], cv2.FILLED)
                        pyautogui.click()

                elif fingers == [0, 1, 1, 1, 0]:
                    length, img, li = detector.findDistance(8, 12, img)
                    if int(length) < 23:
                        cv2.circle(img, (li[4], li[5]), 10, [0, 255, 0], cv2.FILLED)
                        pyautogui.rightClick()

                elif fingers == [0, 0, 0, 0, 0] and not drag:
                    pyautogui.mouseDown(button='left')
                    drag = True
                elif fingers == [1, 1, 1, 1, 1] and drag:
                    drag = False
                    pyautogui.mouseUp(button='left')

                elif fingers == [1, 1, 0, 0, 1]:
                    mouse.wheel(-1)

                elif fingers == [0, 1, 0, 0, 1]:
                    mouse.wheel(1)
                elif fingers == [1, 0, 0, 0, 1]:
                    mode = "Keyboard"
                    cv2.destroyAllWindows()
                    break

            else:
                if fingers == [1, 0, 0, 0, 1]:
                    pyautogui.screenshot("Screenshot{}.png".format(ssc))
                    ssc += 1
                    print("success")
                    cv2.waitKey(1000)

                elif fingers == [0, 1, 0, 0, 1] and not pressed:
                    pyautogui.keyDown('alt')
                    pressed = True

                elif fingers == [1, 1, 0, 0, 1] and pressed:
                    cv2.waitKey(500)
                    pyautogui.press('tab')

                elif fingers == [1, 1, 1, 1, 1]:
                    pyautogui.keyUp('alt')
                    pressed = False

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "FPS: " + str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, [255, 0, 255], 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    while mode == "Keyboard":
        text = voice.detectVoice()
        if text == True:
            exit(0)
        elif text == False:
            print("Error occurred, Shifting to Mouse mode...")
            mode = "Mouse"
            break
        if text.strip().lower() == "mouse" or text[-5:].strip().lower() == "mouse":
            mode = "Mouse"
            break
        pyautogui.typewrite(text)
