# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 11:12:43 2020

@author: Kaushal Mistry
"""

import cv2
import dlib
import numpy as np
from math import hypot
import pyglet
import time

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_SIMPLEX
sound = pyglet.media.load("E:\\Project\\gaze_controlled_keyboard\\sound.wav", streaming=False)
eyebrow_up = 30

def midpoint(p1, p2):
    return (p1.x + p2.x)//2, (p1.y + p2.y)//2

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x,y), (x1,y1), (0,255,255), 3)
        
        landmarks = predictor(gray,face)
        
        left_eyebrow_point = midpoint(landmarks.part(23), landmarks.part(24))
        left_eye_point = midpoint(landmarks.part(43), landmarks.part(44))
        
        right_eyebrow_point = midpoint(landmarks.part(19), landmarks.part(20))
        right_eye_point = midpoint(landmarks.part(37), landmarks.part(38))
        
        left_ver_line = cv2.line(frame, left_eyebrow_point, left_eye_point, (0,0,255), 2)
        # right_ver_line = cv2.line(frame, right_eyebrow_point, right_eye_point, (0,0,255), 2)
        
        left_ver_line_length = hypot((left_eyebrow_point[0] - left_eye_point[0]), (left_eyebrow_point[1] - left_eye_point[1]))
        right_ver_line_length = hypot((right_eyebrow_point[0] - right_eye_point[0]), (right_eyebrow_point[1] - right_eye_point[1]))
        # print(ver_line_length)
        
        left_eyebrow_1 = (landmarks.part(22).x, landmarks.part(22).y)
        left_eyebrow_2 = (landmarks.part(26).x, landmarks.part(26).y)
        
        left_hor_line = cv2.line(frame, left_eyebrow_1, left_eyebrow_2, (0,0,255), 2)
        
        hor_line_length = hypot((left_eyebrow_1[0] - left_eyebrow_2[0]), (left_eyebrow_1[1] - left_eyebrow_2[1]))
        
        ratio = hor_line_length / left_ver_line_length
        print(ratio)
        
        # if ver_line_length > 40:
        #     # if 
        #     # sound.play()
        #     print(ver_line_length)
        #     time.sleep(1)
    
    cv2.imshow("Elocutor", frame)

    key = cv2.waitKey(1)
    if key == 27: # press esc to exit
        break

cap.release()
cv2.destroyAllWindows()