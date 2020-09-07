# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 14:30:28 2020

@author: Kaushal Mistry
"""

import cv2
import numpy as np

Main_Options = np.zeros((200, 500, 3), np.uint8)
th = 3
cv2.rectangle(Main_Options, (0+th, 0+th),  (0+500-th, 0+100-th), (255,255,255), -1)
cv2.putText(Main_Options, "Select Detection Method", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

images = {0:'a', 1:'b', 2:'c'}

def draw_icon(image_index, image_select):
    if image_index == 0:
        x = 0
        y = 100
    elif image_index == 1:
        x = 100
        y = 100
    else:
        x = 200
        y = 100
    width = 100
    height = 100
    
    th = 3 # thickness

    # Text settings
    text = images[image_index]
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 5
    font_th = 4
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

while True:
    cv2.imshow("Elocutor Home", Main_Options)
    
    for i in range(3):
        if i == icon_index:
            light = True
        else:
            light = False
        draw_icon(i, light)
    
    frames = (frames + 1) % 15
    if frames == 5:
        icon_index = (icon_index + 1) % 3
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()

# import tkinter as tk
# top = tk.Tk()
# top.mainloop()