# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 12:34:52 2020

@author: Kaushal Mistry
"""

import cv2
import numpy as np
import dlib
from math import hypot

cap = cv2.VideoCapture(0)
board = np.zeros((100, 600), np.uint8)
board[:] = 255

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_COMPLEX
font1 = cv2.FONT_HERSHEY_PLAIN

# Keyboard settings
keyboard = np.zeros((300, 500, 3), np.uint8)
keys_set = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",
              5: "A", 6: "S", 7: "D", 8: "F", 9: "G",
              10: "Z", 11: "X", 12: "C", 13: "V", 14: "<"}

def draw_letters(letter_index, text, letter_light):
    # Keys
    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 100
        y = 0
    elif letter_index == 2:
        x = 200
        y = 0
    elif letter_index == 3:
        x = 300
        y = 0
    elif letter_index == 4:
        x = 400
        y = 0
    elif letter_index == 5:
        x = 0
        y = 100
    elif letter_index == 6:
        x = 100
        y = 100
    elif letter_index == 7:
        x = 200
        y = 100
    elif letter_index == 8:
        x = 300
        y = 100
    elif letter_index == 9:
        x = 400
        y = 100
    elif letter_index == 10:
        x = 0
        y = 200
    elif letter_index == 11:
        x = 100
        y = 200
    elif letter_index == 12:
        x = 200
        y = 200
    elif letter_index == 13:
        x = 300
        y = 200
    elif letter_index == 14:
        x = 400
        y = 200

    width = 100
    height = 100
    th = 3 # thickness

    # Text settings
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 5
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y

    if letter_light is True:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
        cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)

            
# Counters
frames = 0
letter_index = 0
blinking_frames = 0
frames_to_blink = 4
frames_active_letter = 9

text = ""

while True:
    _, frame = cap.read()
    # rows, cols, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x,y), (x1,y1), (0,255,255), 3)
        
        landmarks = predictor(gray,face)
        
        nose_point = (landmarks.part(33).x, landmarks.part(33).y)
        chin_point = (landmarks.part(8).x, landmarks.part(8).y)
        
        ver_line = cv2.line(frame, nose_point, chin_point, (255,0,0), 2)
        
        lip_point_left = (landmarks.part(48).x, landmarks.part(48).y)
        lip_point_right = (landmarks.part(54).x, landmarks.part(54).y)
        
        hor_line = cv2.line(frame, lip_point_left, lip_point_right, (255,0,0), 2)
        
        ver_line_length = hypot((nose_point[0] - chin_point[0]), (nose_point[1] - chin_point[1]))
        hor_line_length = hypot((lip_point_left[0] - lip_point_right[0]), (lip_point_left[1] - lip_point_right[1]))
        
        # print(hor_line_length)
        ratio = ver_line_length / hor_line_length
        # print(ratio)
        if ratio < 1.18:
            cv2.putText(frame,"Selected",(5,100), font, 2, (0, 0, 0))
            # text += keys_set[letter_index]
            blinking_frames += 1
        
            if blinking_frames == frames_to_blink:
                if keys_set[letter_index] == '<':
                    text = text[:-1]
                else:
                    text += keys_set[letter_index]
                blinking_frames = 0
        else:
            blinking_frames = 0
            
    
    for i in range(15):
            if i == letter_index:
                light = True
            else:
                light = False
            draw_letters(i, keys_set[i], light)
    
    frames += 1
    
    if frames == 15:
        letter_index = (letter_index + 1) % 15
        frames = 0
        
    cv2.putText(board,text, (0, 50), font1, 1, 0, 1)
    
    cv2.imshow("Elocutor", frame)
    cv2.imshow("Virtual keyboard", keyboard)
    cv2.imshow("Board", board)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()