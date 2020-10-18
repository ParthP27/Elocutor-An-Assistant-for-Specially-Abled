# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 11:08:43 2020

@author: Kaushal Mistry

"""

#---------------------------------------- Modules -------------------------------------------------
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import dlib
from math import hypot
import time
import pyautogui as pag
# import autocomplete
# import next_word_prediction


#------------------------------------- Main Window ------------------------------------------------
root = tk.Tk()
root.title("Elocutor")
root.config(bg='gray')
root.resizable(width=False, height=False)

# Screen Sizes
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Resize Window
screen_width_updated = screen_width//2
root.geometry(f'{screen_width_updated}x{screen_height}+{screen_width_updated}+0')


#--------------------------------------- Control Center ----------------------------------------
# Dimensions for all frames and widgets
full_width = screen_width // 2
keyboard_height = screen_height // 3
title_height = screen_height // 15 - 15
app_height = screen_height * 0.6 - 55
app_width = full_width // 3
remaining_width = full_width * 2 // 3
user_height = app_height // 2
user_width = app_width
apps_icon_width = app_width // 2
apps_icon_height = app_width // 4

# Icon Names and Images
images = {0:'Notepad', 1:'Chrome', 2:'This PC', 3:'Calculator', 4:'Setting', 5:'Exit'}
icon_count = len(images.keys())

# Selection Criteria
app_frames = 0
key_frames = 0
blinking_frames = 0
frames_to_blink = 20

# Variables used in function to Open App
icon_index = 0
selected = 0
app = -1
app_opened = False

#Setting Keyboard size
resolutions = [[1920,1080],[1440,900],[1366,768]]
index_res = 0
for i in resolutions:
    if i[0] == screen_width and i[1] == screen_height:
        index_res = resolutions.index(i)
        
Keyboard_gap = 30 - (5*index_res)
Keyboard_width = (resolutions[index_res][0]//2 - Keyboard_gap) // 16     #57-(24*index_res)
Keyboard_height = (resolutions[index_res][1]//3 - 2*Keyboard_gap) // 6 #55-(10*index_res)
Keyboard_th = int(3-(0.5*index_res))

# Keyboard Counters and Setting
letter_index = 0
frames_active_letter = 19
flag_for_change = 0
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
select_keyboard_menu = True
keyboard_selection_frames = 0
mode = 0
side = 0

# Line wise Selection Keyboard
line_selected = 0
select_line_menu = False
cheek_move_counter = 0
last_selected_line = 0



# -------------- ALL FRAMES -----------------
title_frame = tk.Frame(root, bg='dark blue', width = full_width, height = title_height)
apps_frame = tk.Frame(root, bg='yellow', width = app_width, height = app_height)
user_frame = tk.Frame(root, bg='orange', width = user_width, height = user_height)
extra_frame1 = tk.Frame(root, bg='blue', width = user_width, height = user_height)
middle_frame4 = tk.Frame(root, bg='red', width = remaining_width, height = user_height)
keyboard_frame = tk.Frame(root, bg='black', width = full_width, height = keyboard_height)

# ------------- Layout of all frames -----------
title_frame.place(x = 0,y = 0)
apps_frame.place(x = 0, y = title_height)
extra_frame1.place(x = app_width, y = title_height)
user_frame.place(x = app_width * 2, y = title_height)
middle_frame4.place(x = app_width, y = title_height+user_height)
keyboard_frame.place(x = 0, y = title_height+app_height)


#-------------------------- Labels in that frame to show real time videos and simulations -------------------------
# title_label = tk.Label(title_frame, text = "Welcome to Elocutor")
title_label = tk.Label(title_frame, text = "Welcome to Elocutor", background = "#3b6dc7", foreground = "white", font=("Helvetica", 20), width = full_width // 15)
title_label.pack()

app_label = tk.Label(apps_frame)
app_label.pack()

user_label = tk.Label(user_frame)
user_label.pack()

keyboard_label = tk.Label(keyboard_frame)
keyboard_label.pack()


#---------------------------- Whole Code and Logic for app selection and User video stream--------------------------

# Landmarks Detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")

# User Video
cap = cv2.VideoCapture(0)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

# Change User Frame to fit the frame
def rescale_frame(frame, percent=75):
    width = int(user_width)
    height = int(user_height)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


#----------------------------- Application Icons Selection Menu ---------------------------------

Main_Options = np.zeros((len(images.keys())*apps_icon_height, apps_icon_width, 3), np.uint8)

icons = []

for i in images.values():
    ele=cv2.imread("Icons/"+i+".png")
    ele=cv2.resize(ele, (apps_icon_width, apps_icon_height))
    icons.append(ele)

# Vertical Conversion
img_concate_Verti = np.concatenate(icons,axis=0)

# Function that draws Icons on the screen

def draw_icon(image_index, image_select):
    x=0
    y=image_index*apps_icon_height
    width = apps_icon_width
    height = apps_icon_height
    
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
        
        
# Function That Opens an App
def OpenApp():
    global app
    global app_opened
    if app == 0:
        pag.press('win',interval=0.25)
        time.sleep(0.1)
        pag.press('n')
        pag.typewrite('otepad')
    elif app == 1:
        pag.press('win',interval=0.25)
        time.sleep(0.1)
        pag.press('c')
        pag.typewrite('hrome')      
    elif app == 2:
        pag.press('win',interval=0.25)
        time.sleep(0.1)
        pag.press('t')
        pag.typewrite('his PC')
    elif app == 3:
        pag.press('win',interval=0.25)
        time.sleep(0.1)
        pag.press('c')
        pag.typewrite('alculator')
    elif app == 5:
        root.destroy()
    
    if app != 5:
        time.sleep(1)
        pag.press('enter')
        time.sleep(2)
        pag.hotkey('win', 'left')
    app_opened = True
    
# ------------------------------- END : Application Selection ----------------------------------------
    
# ------------------------------------------------- Keyboard Section -------------------------------------------
keyboard = np.zeros((Keyboard_height*6+Keyboard_gap*2, Keyboard_width*16+Keyboard_gap, 3), np.uint8)

keys_set_1 = {0:' ',1:'f1',2:'f2',3:'f3',4:'f4',5:'f5',6:'f6',7:" ",8: " ",
              9:'0', 10:'1', 11:'2',12: '3',13: '4',14: '5',15: '6',16: " ",
              17: "tab", 18: "q", 19: "w", 20: "e", 21: "r",22: "t",23: " ",24: " ",
              25: "capslock", 26: "a", 27: "s", 28: "d",29: "f",30: "g",31: " ",32: " ",
              33: "shiftleft",34: "z",35: "x",36: "c",37: "v",38: " ",39: " ",40: " ",
              41: "ctrlleft",42: "fn",43: "winleft",44: "altleft",45: "space",46:" ",47:"esc"}
              
keys_set_2 = {0:'f7',1:'f8',2:'f9',3:'f10',4:'f11',5:'f12',6:'del',7: " ",8: " ",
              9:'7', 10:'8', 11:'9',12: '0',13: '-',14: '=',15: 'backspace',16: " ",
              17: "y", 18: "u", 19: "i", 20: "o", 21: "p",22: "[",23: "]",24:"|",
              25: "h", 26: "j", 27: "k",28: "l",29: ";",30: "'",31: "enter",32: " ",
              33: "b",34: "n",35: "m",36: ",",37: ".",38: "/",39: "shiftright",40: " ",
              41:"altright",42: "ctrlright",43:"up",44:"down",45:"left",46:"right",47:" "}


# Function For Keys on Keyboard
def draw_letters(letter_index, text, letter_light,keyset,selection):  
    if selection == 2:
        if keyset == keys_set_1:
            x = (letter_index%8) * Keyboard_width
            y = Keyboard_gap*2 + (letter_index//8) * Keyboard_height
        else:
            x = Keyboard_width*8 + Keyboard_gap + (letter_index%8) * Keyboard_width
            y = Keyboard_gap*2 + (letter_index//8) * Keyboard_height

        #text scaling
        if("ctrl" in text or "caps" in text):
            text=text[:4]
        elif("alt" in text or "win" in text):
            text=text[:3]
        elif("shift" in text):
            text=text[:5]
        elif("back" in text):
            text="<-"
            

        # Text settings
        if(len(text)>1 and len(text)<4):
            font_scale = 0.8-(0.1*index_res)
            font_th = 1
            
        elif(len(text)>3):
            font_scale = 0.6-(0.1*index_res)
            font_th = 1
          
        else:
            font_scale = 1
            font_th = 1
        font_letter = cv2.FONT_HERSHEY_COMPLEX

        text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
        width_text, height_text = text_size[0], text_size[1]
        text_x = int((Keyboard_width - width_text) / 2) + x
        text_y = int((Keyboard_height + height_text) / 2) + y

        if letter_light is True:
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), (255, 255, 255), -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
        else:
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), (51, 51, 51), -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)
    else:
        
        y = 2
        if text == "L":
            x = 2
        else:
            x = Keyboard_width * 15 + Keyboard_gap - 2
        if letter_light is True:
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), (255, 255, 255), -1)
        else:
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), (51, 51, 51), -1)


# ---------------------------------------END : Keyboard Part --------------------------------------------------
# ------------------------------------- Main Function Which Deals with everything ------------------------------
def show_frame():
    global icon_index
    global frames
    global selected
    global app_frames
    global key_frames
    global blinking_frames
    global frames_to_blink
    global app
    global app_opened
    global letter_index
    global frames_active_letter
    global flag_for_change
    global text
    global keyboard_selected
    global last_keyboard_selected
    global select_keyboard_menu
    global keyboard_selection_frames
    global mode
    global side
    global line_selected
    global select_line_menu
    global cheek_move_counter
    global last_selected_line
    
    
    _, frame = cap.read()    
    frame = rescale_frame(frame, percent=50)
    rows, cols, _ = frame.shape
    frame[rows - 30: rows, 0: cols] = (255, 255, 255)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    # Keyboard Stuff
    if select_keyboard_menu is True:
        if side==0:
                draw_letters(1, "L", True,keys_set_1,0)
                draw_letters(1, "R", False,keys_set_1,1)
        else:
                draw_letters(1, "L", False,keys_set_1,0)
                draw_letters(1, "R", True,keys_set_1,1)
            
        for i in range(48):
                draw_letters(i, keys_set_1[i], False,keys_set_1,2)
        for i in range(48):
                draw_letters(i, keys_set_2[i], False,keys_set_2,2)
    
       
            
    # Keyboard selected
    if keyboard_selected == "left":
        keys_set = keys_set_1
    else:
        keys_set = keys_set_2
    active_letter = keys_set[last_selected_line*8+letter_index]
    
       
    # Face Detection
    faces = detector(gray)
    
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(gray, (x,y), (x1,y1), (0,255,255), 3)
        
        landmarks = predictor(gray,face)
        
        nose_point = (landmarks.part(33).x, landmarks.part(33).y)
        chin_point = (landmarks.part(8).x, landmarks.part(8).y)
        
        
        cv2.line(gray, nose_point, chin_point, (255,0,0), 2)
        
        lip_point_left = (landmarks.part(48).x, landmarks.part(48).y)
        lip_point_right = (landmarks.part(54).x, landmarks.part(54).y)
        
        cv2.line(gray, lip_point_left, lip_point_right, (255,0,0), 2)
        
        ver_line_length = hypot((nose_point[0] - chin_point[0]), (nose_point[1] - chin_point[1]))
        hor_line_length = hypot((lip_point_left[0] - lip_point_right[0]), (lip_point_left[1] - lip_point_right[1]))
        
        ratio = ver_line_length / hor_line_length
        
        font = cv2.FONT_HERSHEY_COMPLEX
        
        if ratio < 1.10:    # Face change detectd
            cv2.putText(gray, "Selected",(5,20), font, 0.8, (0, 0, 0))
            blinking_frames += 1
        
            if blinking_frames == frames_to_blink: # Change for enough time is detected
                
                blinking_frames = 0 # Reset count
                
                # App Selection Stuff
                if app == -1 and not app_opened: # Opens App if not already opened
                    app = icon_index
                
                # Keyboard Simulation Stuff
                elif select_keyboard_menu is True:
                    if side == 0:
                        keyboard_selected = "left"
                    else:
                        keyboard_selected = "right"
                        
                    select_keyboard_menu = False
                    flag_for_change = 1
                    key_frames = 0                    
                    keyboard_selection_frames = 0
                    select_line_menu = True
                
                
                elif select_line_menu is True:
                    last_selected_line = line_selected
                    select_line_menu = False
                
                else:
                    pag.press(active_letter)
                    select_keyboard_menu = True
                    line_selected = 0
                    letter_index = 0
        
        
    
    # Keyboard Drawing
    if app_opened:
        key_frames = (key_frames + 1) % 20
    if select_keyboard_menu is True:
        
        if key_frames == frames_active_letter:
            side = (side+1) % 2
            key_frames = 0
            
            if side==0:
                draw_letters(1, "L", True,keys_set_1,0)
                draw_letters(1, "R", False,keys_set_1,1)
            else:
                draw_letters(1, "L", False,keys_set_1,0)
                draw_letters(1, "R", True,keys_set_1,1)
            
            for i in range(48):
                draw_letters(i, keys_set_1[i], False,keys_set_1,2)
            for i in range(48):
                draw_letters(i, keys_set_2[i], False,keys_set_2,2)
    
    # for line selection
    if select_keyboard_menu is False and select_line_menu is True:
         if key_frames == frames_active_letter:
            line_selected+=1
            key_frames = 0
            if(line_selected==6):
                select_keyboard_menu=True
                line_selected=0
                
         if keys_set==keys_set_1:
             lcount=-1
             for i in range(6):
                 if(line_selected==i):
                     do_light=True
                 else:
                     do_light=False
                 for j in range(8):
                     
                    lcount+=1
                    draw_letters(lcount, keys_set_1[lcount], do_light,keys_set_1,2)
             for i in range(48):
                draw_letters(i, keys_set_2[i], False,keys_set_2,2)
         else:
             lcount=-1
             for i in range(6):
                 if(line_selected==i):
                     do_light=True
                 else:
                     do_light=False
                 for j in range(8):
                     
                    lcount+=1
                    draw_letters(lcount, keys_set_2[lcount], do_light,keys_set_2,2)
                    #print(lcount)
             for i in range(48):
                draw_letters(i, keys_set_1[i], False,keys_set_1,2)
        
    # Display letters on the keyboard
    if select_keyboard_menu is False and select_line_menu is False:
        if flag_for_change == 1:
            flag_for_change = 0
            if key_frames == 15:
                letter_index += 1
                key_frames = 0
        else:
            if key_frames == frames_active_letter:
                letter_index += 1
                key_frames = 0
        
        if letter_index == 8:
            select_keyboard_menu=True
            letter_index = 0
            
  
        if keys_set == keys_set_1:
            lcount = 8 * last_selected_line            
            
            for j in range(8):
               if j == letter_index:
                   light = True
               else:
                   light = False
               
               draw_letters(lcount, keys_set_1[lcount], light, keys_set_1, 2)
               lcount += 1
               
            for i in range(48):
               draw_letters(i, keys_set_2[i], False, keys_set_2, 2)
        
        else:               
            lcount = 8 * last_selected_line           
            
            for j in range(8):
               if j == letter_index:
                   light = True
               else:
                   light = False
               
               draw_letters(lcount, keys_set_2[lcount], light, keys_set_2, 2)
               lcount += 1
            for i in range(48):
               draw_letters(i, keys_set_1[i], False, keys_set_1, 2)   
               
               
    # App Related content
    if app != -1 and not app_opened:    
        OpenApp()
        
    for i in range(icon_count):
        if app == -1:
            if i == icon_index:
                light = True
            else:
                light = False
        else:
            light = False
        draw_icon(i, light)
    
    app_frames = (app_frames + 1) % 15
    if app_frames == 14:
        icon_index = (icon_index + 1) % (icon_count)
    
    
    
    # Loading Meter
    percentage_blinking = blinking_frames / frames_to_blink
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(gray, (0, rows - 30), (loading_x, rows), (51, 51, 51), -1)
    
    
    general = np.concatenate((img_concate_Verti,Main_Options), axis = 1)
    
    
    # App Selection
    apps = Image.fromarray(general, 'RGB')
    apps_tk = ImageTk.PhotoImage(image=apps)
    app_label.apps_tk = apps_tk
    app_label.configure(image=apps_tk)
    
    
    # Keyboard
    Key_Board = Image.fromarray(keyboard, 'RGB')
    Key_Board_tk = ImageTk.PhotoImage(image = Key_Board)
    keyboard_label.Key_Board_tk = Key_Board_tk
    keyboard_label.configure(image = Key_Board_tk)
    
    if app_opened is False:
        app_label.after(10, show_frame)
    else:
        keyboard_label.after(10, show_frame)
    
    # User
    user = Image.fromarray(gray)
    user_tk = ImageTk.PhotoImage(image=user)
    user_label.user_tk = user_tk
    user_label.configure(image=user_tk)


show_frame()
root.mainloop()
cap.release()