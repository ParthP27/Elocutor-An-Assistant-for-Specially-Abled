# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:16:10 2020

@author: Kaushal Mistry
"""

import cv2

cap = cv2.VideoCapture(0)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

# change_res(250, 250)

def rescale_frame(frame, percent=75):
    width = 250
    height = 250
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

while True:
    _, frame = cap.read()
    frame = rescale_frame(frame, percent=50)
    frame2 = rescale_frame(frame, percent=75)
    # cv2.resize(frame, (250,250))
    # cv2.namedWindow(frame, cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(frame, (100,100))
    cv2.imshow("User",frame)
    cv2.imshow("1", frame2)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()