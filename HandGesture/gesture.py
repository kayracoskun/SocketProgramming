#!/usr/bin/env python3

import cv2
import time
import numpy as np
import gesture_module as gm
import hand_server


class Hand:

    def __init__(self):
        self.previousT = 0
        self.newT = 0
        self.counter = 0
        self.old_message = []

        self.detector = gm.HandDetector()
        self.socket = hand_server.Connect()

        self.vid = cv2.VideoCapture(0)
        self.mission()

    def mission(self):

        while True:
            ret, frame = self.vid.read()
            frame = cv2.flip(frame, 1)
            show_frame = frame

            # fps calculations
            self.newT = time.time()
            fps = np.round((1/(self.newT-self.previousT)), 2)
            self.previousT = self.newT

            # Limiting the frame where hands are being detected
            frame = frame[:, 100:540, :]
            cv2.line(show_frame, (100, 0), (100, 480),
                     (0, 0, 223), thickness=6)
            cv2.line(show_frame, (540, 0), (540, 480),
                     (0, 0, 223), thickness=6)
            self.detector.find_hands(frame, draw=True)
            fingers = self.detector.fingersUp()
            show_frame[:, 100:540, :] = frame

            # Finger filters
            if len(self.old_message) == 0:
                self.old_message = fingers
            elif fingers == self.old_message and self.counter != 5:
                self.counter += 1

            if self.counter == 5:
                data = str(sum(self.old_message))
                self.socket.send_command(data)
                self.old_message = []

            # Debug
            cv2.putText(frame, str(int(fps)), (20, 60),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 256, 0), 5)
            cv2.imshow("results", show_frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break


if __name__ == '__main__':
    main = Hand()
