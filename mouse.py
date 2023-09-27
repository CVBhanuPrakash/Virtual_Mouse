# We need to install python 3.8 because some libraries are not working well in latest versions of python

# pip install opencv-python
# pip install mediapipe
# pip install autopy
# pip install pynput
# pip install numpy
# pip install ffpyplayer


# If fore finger and litter finger both are up          ==  scroll up
# If fore finger, little finger and thumb are up        == scroll down
# Thumb and index finger both are up                    == volume down
# If thumb is down and rest all fingers are up          == volume up
# If fore finger, middle finger and ring finger are up(3 fingers)  == open website
# If fore finger & middle finger both are up            == click

import cv2
import numpy as np
import time
import autopy
import mediapipe as mp
import math
import webbrowser
from pynput.keyboard import Key, Controller

# from ffpyplayer.player import MediaPlayer
keyboard = Controller()

# Variables Declaration
pTime = 0  # Used to calculate frame rate
width = 640  # Width of Camera
height = 480  # Height of Camera
frameR = 100  # Frame Rate
smoothening = 8  # Smoothening Factor
prev_x, prev_y = 0, 0  # Previous coordinates
curr_x, curr_y = 0, 0  # Current coordinates
cap = cv2.VideoCapture(0)  # Getting video feed from the webcam
cap.set(3, width)  # Adjusting size
cap.set(4, height)

# Variables used for storing the time of fingers showed
secthree = 0
secfour = 0
secfive = 0
secpagedown = 0
secpageup = 0
fingzero = 0


# Hand Tracking Part

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=False, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    # Function to find the hands in a frame
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    # Function to find position of hands
    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox

    # Function to find witch finger is up
    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    # function to find the distance between two fingers
    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


# Virtual Mouse Part


detector = handDetector(maxHands=1)  # Detecting one hand at max in order to avoid confusion
screen_width, screen_height = autopy.screen.size()  # Getting the screen size
while True:
    success, img = cap.read()
    img = detector.findHands(img)  # Finding the hand
    lmlist, bbox = detector.findPosition(img)  # Getting position of hand

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()  # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255),
                      2)  # Creating boundary box
        if fingers[1] == 1 and fingers[2] == 0:  # If fore finger is up and middle finger is down
            x3 = np.interp(x1, (frameR, width - frameR), (0, screen_width))
            y3 = np.interp(y1, (frameR, height - frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x) / smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            autopy.mouse.move(screen_width - curr_x, curr_y)  # Moving the cursor
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[
            4] == 0:  # If fore finger & middle finger both are up
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:  # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()  # Perform Click

        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0 and fingers[
            0] == 0:  # If fore finger, middle finger and ring finger are up
            if secthree >= 100:
                secthree = 0
            if secthree == 0:
                webbrowser.open_new_tab("https://bhanu.social")
            secthree = secthree + 1

        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[
            0] == 0:  # If thumb is down and rest all fingers are up
            if secfour >= 30:
                secfour = 0
            if secfour == 0:
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
            secfour = secfour + 1

        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[
            0] == 1:  # Thumb and index finger both are up
            if secfive >= 30:
                secfive = 0
            if secfive == 0:
                keyboard.press(Key.media_volume_down)
                keyboard.release(Key.media_volume_down)
            secfive = secfive + 1

        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1 and fingers[
            0] == 1:  # If fore finger, little finger and thumb are up
            if secpagedown >= 10:
                secpagedown = 0
            if secpagedown == 0:
                keyboard.press(Key.down)
                keyboard.release(Key.down)
            secpagedown = secpagedown + 1

        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1 and fingers[
            0] == 0:  # If fore finger and litter finger both are up
            if secpageup >= 10:
                secpageup = 0
            if secpageup == 0:
                keyboard.press(Key.up)
                keyboard.release(Key.up)
            secpageup = secpageup + 1

            if fingzero >= 10:
                break
        else:
            fingzero = 0

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)