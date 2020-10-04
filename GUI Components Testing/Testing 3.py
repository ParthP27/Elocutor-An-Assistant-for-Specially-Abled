# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:28:59 2020

@author: Kaushal Mistry
"""


import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import dlib
from math import hypot
import time
import pyautogui

# Main Window
root = tk.Tk()
root.title("Elocutor")
root.config(bg='gray')
root.attributes('-fullscreen', True)

# Screen Sizes
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# ALL FRAMES 
title_frame = tk.Frame(root, bg='green', width=screen_width, height=50)
apps_frame = tk.Frame(root, bg='yellow', width=200, height = screen_height - 50)
middle_frame2 = tk.Frame(root, bg='blue', width=screen_width - 450, height=500)
user_frame = tk.Frame(root, bg='orange', width=250, height=250)
middle_frame4 = tk.Frame(root, bg='red', width=250, height=250)
keyboard_frame = tk.Frame(root,bg='black', width=screen_width - 200, height=screen_height - 550)

# Layout of all frames
title_frame.place(x=0,y=0)
apps_frame.place(x=0, y=50)
middle_frame2.place(x=200, y=50)
user_frame.place(x=screen_width-250, y=50)
middle_frame4.place(x=screen_width-250, y=300)
keyboard_frame.place(x=200, y=550)

# Labels in that frame to show real time videos and simulations
app_label = tk.Label(apps_frame)
app_label.pack()

user_label = tk.Label(user_frame)
user_label.pack()


# Whole Code and Logic for app selection and User video stream

#Landmarks Detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")

images = {0:'Notepad', 1:'Chrome', 2:'This PC', 3:'Calculator', 4:'Exit'}

cap = cv2.VideoCapture(0)
def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

# change_res(240, 240)
def rescale_frame(frame, percent=75):
    width = 250
    height = 250
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

Size=100 #Overall Sizes
Main_Options = np.zeros((len(images.keys())*Size, Size, 3), np.uint8)

icons=[]

for i in images.values():
    ele=cv2.imread("Icons/"+i+".png")
    ele=cv2.resize(ele, (Size, Size))
    icons.append(ele)
img_concate_Verti=np.concatenate(icons,axis=0)

def draw_icon(image_index, image_select):
    x=0
    y=image_index*Size
    width = Size
    height = Size
    
    th = 3 # thickness

    # Text settings
    text = images[image_index]
    font_letter = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    font_th = 1
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    
    if image_select is True:
        cv2.rectangle(Main_Options, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        cv2.putText(Main_Options, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(Main_Options, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
        cv2.putText(Main_Options, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)


icon_index = 0
frames = 0
selected = 0
frames = 0
blinking_frames = 0
frames_to_blink = 4
# frames_active_letter = 9
app = -1

def show_frame():
    global icon_index
    global frames
    global selected
    global frames
    global blinking_frames
    global frames_to_blink
    global app
    _, frame = cap.read()
    frame = rescale_frame(frame, percent=50)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # cv2.resize(gray, (250, 250))
    
    faces = detector(gray)
    
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(gray, (x,y), (x1,y1), (0,255,255), 3)
        
        landmarks = predictor(gray,face)
        
        nose_point = (landmarks.part(33).x, landmarks.part(33).y)
        chin_point = (landmarks.part(8).x, landmarks.part(8).y)
        
        ver_line = cv2.line(gray, nose_point, chin_point, (255,0,0), 2)
        
        lip_point_left = (landmarks.part(48).x, landmarks.part(48).y)
        lip_point_right = (landmarks.part(54).x, landmarks.part(54).y)
        
        hor_line = cv2.line(gray, lip_point_left, lip_point_right, (255,0,0), 2)
        
        ver_line_length = hypot((nose_point[0] - chin_point[0]), (nose_point[1] - chin_point[1]))
        hor_line_length = hypot((lip_point_left[0] - lip_point_right[0]), (lip_point_left[1] - lip_point_right[1]))
        
        ratio = ver_line_length / hor_line_length
        
        font = cv2.FONT_HERSHEY_COMPLEX
        
        if ratio < 1.10:
            cv2.putText(gray, "Selected",(5,100), font, 2, (0, 0, 0))
            blinking_frames += 1
        
            if blinking_frames == frames_to_blink:
                app = icon_index
                
                blinking_frames = 0
        else:
            blinking_frames = 0
    
    
    for i in range(5):
        if i == icon_index:
            light = True
        else:
            light = False
        draw_icon(i, light)
    
    frames = (frames + 1) % 15
    if frames == 14:
        icon_index = (icon_index + 1) % 5
    
    
    general=np.concatenate((img_concate_Verti,Main_Options),axis=1)
    
    apps = Image.fromarray(general, 'RGB')
    apps_tk = ImageTk.PhotoImage(image=apps)
    app_label.apps_tk = apps_tk
    app_label.configure(image=apps_tk)
    app_label.after(11, show_frame)
    
    user = Image.fromarray(gray)
    user_tk = ImageTk.PhotoImage(image=user)
    user_label.user_tk = user_tk
    user_label.configure(image=user_tk)
    # user_label.after(17, show_frame)
       


show_frame()
root.mainloop()
cap.release()