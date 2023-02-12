import cv2
import mediapipe as mp
import numpy as np


class HandDetector():

    def __init__(self, mode=False, maxHands=2, complexity=1, detectionConf=0.5, trackingConf=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionConf = detectionConf
        self.trackingConf = trackingConf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.complexity, self.detectionConf, self.trackingConf)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        self.lmList = []
        self.areas = []

        if self.results.multi_hand_landmarks is not None:
            for hand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    self.lmList.append([id, cx, cy])

            # detects the largesthand hand
            if len(self.lmList) == 21:
                areatekel = abs((0.5)*(self.lmList[0][1]*(self.lmList[5][2]-self.lmList[17][2])+self.lmList[5][1]*(
                    self.lmList[17][2]-self.lmList[0][2])+self.lmList[17][1]*(self.lmList[0][2]-self.lmList[5][2])))
                # print(areatekel)
                if areatekel <= 220 or areatekel >= 1560:
                    draw = False
                    self.lmList = []
                if draw == True:
                    self.mpDraw.draw_landmarks(
                        frame, hand, self.mpHands.HAND_CONNECTIONS)

            if len(self.lmList) == 42:
                area1 = abs((0.5)*(self.lmList[0][1]*(self.lmList[5][2]-self.lmList[17][2])+self.lmList[5][1]*(
                    self.lmList[17][2]-self.lmList[0][2])+self.lmList[17][1]*(self.lmList[0][2]-self.lmList[5][2])))
                area2 = abs((0.5)*(self.lmList[21][1]*(self.lmList[26][2]-self.lmList[38][2])+self.lmList[26][1]*(
                    self.lmList[38][2]-self.lmList[21][2])+self.lmList[38][1]*(self.lmList[21][2]-self.lmList[26][2])))
                self.areas.append(area1)
                self.areas.append(area2)
                largesthand = np.argmax(self.areas)
                largestarea = np.max(self.areas)
                if largestarea <= 220 or largestarea >= 1560:
                    draw = False
                    self.lmList = []

                hand1 = self.lmList[0:21]
                hand2 = self.lmList[21:42]

                if largesthand == 0:
                    self.lmList = hand1
                else:
                    self.lmList = hand2

                if draw == True:
                    # draws second hand's landmarks as the default one
                    dizi1 = [0, 1, 2, 3, 4]
                    dizi2 = [0, 5, 6, 7, 8]
                    dizi3 = [9, 10, 11, 12]
                    dizi4 = [13, 14, 15, 16]
                    dizi5 = [0, 17, 18, 19, 20]
                    dizi6 = [5, 9, 13, 17]

                    k = 0
                    for point1 in dizi1:
                        if k != 4:
                            cv2.line(frame, (self.lmList[point1][1], self.lmList[point1][2]), (
                                self.lmList[dizi1[k+1]][1], self.lmList[dizi1[k+1]][2]), (224, 224, 224), 2)
                        k += 1
                    k = 0
                    for point2 in dizi2:
                        if k != 4:
                            cv2.line(frame, (self.lmList[point2][1], self.lmList[point2][2]), (
                                self.lmList[dizi2[k+1]][1], self.lmList[dizi2[k+1]][2]), (224, 224, 224), 2)
                        k += 1
                    k = 0
                    for point3 in dizi3:
                        if k != 3:
                            cv2.line(frame, (self.lmList[point3][1], self.lmList[point3][2]), (
                                self.lmList[dizi3[k+1]][1], self.lmList[dizi3[k+1]][2]), (224, 224, 224), 2)
                        k += 1
                    k = 0
                    for point4 in dizi4:
                        if k != 3:
                            cv2.line(frame, (self.lmList[point4][1], self.lmList[point4][2]), (
                                self.lmList[dizi4[k+1]][1], self.lmList[dizi4[k+1]][2]), (224, 224, 224), 2)
                        k += 1
                    k = 0
                    for point5 in dizi5:
                        if k != 4:
                            cv2.line(frame, (self.lmList[point5][1], self.lmList[point5][2]), (
                                self.lmList[dizi5[k+1]][1], self.lmList[dizi5[k+1]][2]), (224, 224, 224), 2)
                        k += 1
                    k = 0
                    for point6 in dizi6:
                        if k != 3:
                            cv2.line(frame, (self.lmList[point6][1], self.lmList[point6][2]), (
                                self.lmList[dizi6[k+1]][1], self.lmList[dizi6[k+1]][2]), (224, 224, 224), 2)
                        k += 1
                    k = 0
                    for lms in self.lmList:
                        cv2.circle(frame, (lms[1], lms[2]),
                                   3, (224, 224, 224), 2)
                        cv2.circle(frame, (lms[1], lms[2]), 2, (0, 0, 255), 2)

    def calculate_distance(self, point1, point2):
        point9x, point9y = point1[1], point1[2]
        point4x, point4y = point2[1], point2[2]
        distance = np.sqrt((np.abs(point9x-point4x)*np.abs(point9x-point4x)) +
                           (np.abs(point9y-point4y)*np.abs(point9y-point4y)))
        return distance

    def fingersUp(self):
        self.tipIds = [4, 8, 12, 16, 20]
        fingers = []

        if len(self.lmList) != 0:
            # 4 ve 9 arasi mesafe
            dist = self.calculate_distance(
                self.lmList[self.tipIds[0]], self.lmList[9])
            # 5 ve 6 arası mesafe referans degeri
            referance_dist = self.calculate_distance(
                self.lmList[5], self.lmList[6])

            offset = referance_dist*25/100  # hata payi

            # basparmak
            if dist < referance_dist+offset:
                fingers.append(0)
            else:
                fingers.append(1)

            # 4 fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # trick
            if ((fingers[0] == 1) & (fingers[1] == 0) & (fingers[2] == 0) & (fingers[3] == 0) & (fingers[4] == 0)):
                fingers[0] = 0

        return fingers
