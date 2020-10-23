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
import autocomplete as autoc
# import next_word_prediction
# autoc.load()


#------------------------------------- Main Window ------------------------------------------------
root = tk.Tk()
root.title("Elocutor")
root.iconbitmap(r"E:\Project\Elocutor\GUI Components Testing\images\icons8-siri-256.ico")
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

frame_selector = 1
'''
    0 : Option Frame (Apps, Keyboard, Words, etc.)
    1 : App Selection Frame
    2 : Keyboard Frame
    3 : Frequent Words
    4 : Extra Frame
'''

full_width = screen_width // 2
keyboard_height = screen_height // 3
title_height = screen_height // 15 - 15
app_height = screen_height * 0.6 - 55
app_width = full_width // 4
remaining_width = full_width * 3 // 4
user_height = app_height // 2
user_width = remaining_width // 2
apps_icon_width = app_width // 2
apps_icon_height = app_width // 3
frame_selection_width = remaining_width // 3
words_frame_width = remaining_width * 2 // 3

# Icon Names and Images
images = {0:'Notepad', 1:'Chrome', 2:'This PC', 3:'Calculator', 4:'Setting', 5:'Exit'}
icon_count = len(images.keys())

# Frame Selector Frame (Options Wali Frame BABU BHAIYA)
options = {0:'Applications', 1:'Keyboard', 2:'Words'}
selected_option = 0

# Selection Criteria
app_frames = 0
key_frames = 0
blinking_frames = 0
frames_to_blink = 20
simulation_time = 20

# Variables used in function to Open App
icon_index = 0
selected = 0
app = -1
app_opened = False
opened_apps = []

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
active_letter = ""
letter_index = 0
frames_active_letter = 20
flag_for_change = 0
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
extra_frame1 = tk.Frame(root, bg='black', width = user_width, height = user_height)
selection_frame = tk.Frame(root, bg='green', width = frame_selection_width, height = user_height)
words_frame = tk.Frame(root, bg='red', width = words_frame_width, height = user_height)
keyboard_frame = tk.Frame(root, bg='black', width = full_width, height = keyboard_height)

# ------------- Layout of all frames -----------
title_frame.place(x = 0,y = 0)
apps_frame.place(x = 0, y = title_height)
extra_frame1.place(x = app_width, y = title_height)
user_frame.place(x = app_width + user_width, y = title_height)
selection_frame.place(x = app_width, y = title_height+user_height)
words_frame.place(x = app_width + frame_selection_width, y = title_height+user_height)
keyboard_frame.place(x = 0, y = title_height+app_height)

# Word Prediction Module Variables

current_valid_word = ""
text = ""
predicted_words = []
new_word_added = False
word_count = 0
valid_keys = ['caps', 'shift', 'ctrl']



#-------------------------- Labels in that frame to show real time videos and simulations -------------------------

# logo = tk.PhotoImage(file="images/icons8-siri-256.png")
# logo = logo.subsample(title_height, title_height)
title_label = tk.Label(title_frame, text = "Welcome to Elocutor", background = "#3b6dc7", foreground = "white", font=("Helvetica", 20), width = full_width // 15)
title_label.pack()

app_label = tk.Label(apps_frame)
app_label.pack()

user_label = tk.Label(user_frame)
user_label.pack()

keyboard_label = tk.Label(keyboard_frame)
keyboard_label.pack()

option_label = tk.Label(selection_frame)
option_label.pack()

words_label = tk.Label(words_frame)
words_label.pack()


#---------------------------- Whole Code and Logic for app selection and User video stream--------------------------

# Landmarks Detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")

# User Video
cap = cv2.VideoCapture(0)

# --------------------- Functions who rescales cv2 window
def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

# Change User Frame to fit the frame
def rescale_frame(frame, percent=75):
    width = int(user_width)
    height = int(user_height)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# ------------------------- Functions to draw blank frames without simulation ------
def blank_Apps():
    for i in range(icon_count):
        draw_icon(i, False)

def blank_Keyboard():
    draw_letters(1, "L", False, keys_set_1, 0)
    draw_letters(1, "R", False, keys_set_1, 1)
                
    for i in range(48):
        draw_letters(i, keys_set_1[i], False,keys_set_1,2)
    for i in range(48):
        draw_letters(i, keys_set_2[i], False,keys_set_2,2)

def blank_Options():
    for i in range(len(options.keys())):
        draw_options(i, False)

def blank_words():
    for i in range(10):
        draw_words(i, False, True)

def put_words():
    global predicted_words
    if len(predicted_words) > 0:
        for i in range(10):
            draw_words(i, False, False)
    else:
        blank_words()
    
        
def word_check1(letter):
    if len(letter) == 1 and letter.isalpha():
        return True
    else:
        return False
    
def word_check2(letter):
    if len(letter) == 1 and (letter.isalpha() or letter.isspace()):
        return True
    else:
        return False
    
def Predict_Words():
    global predicted_words
    global text
    global current_valid_word
    predicted_words = autoc.predict_currword(current_valid_word, 10)

def Predict_Next_Word():
    print()
    


#----------------------------- Option Wali Frame--------------------------------------------
Option_Frame = np.zeros((len(options.keys())*int(user_height), int(frame_selection_width), 3), np.uint8)
def draw_options(option_index, option_select):
    width = int(frame_selection_width) - 20
    height = int(user_height) // 3 - 30
    x = 10
    y = Keyboard_gap + (option_index * (height + 30))
    
    th = 3 # thickness

    # Text settings 
    text = options[option_index]
    font_letter = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.4
    font_th = 1
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    
    if option_select is True:
        cv2.rectangle(Option_Frame, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        cv2.putText(Option_Frame, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(Option_Frame, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
        cv2.putText(Option_Frame, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)


#--------------------------------- Predicted Words Frame --------------------------
words = np.zeros((int(user_height // 5) * 5, int(words_frame_width // 2)*2, 3), np.uint8)

def draw_words(word_index, word_select, blank):
    global predicted_words
    width = int(words_frame_width // 2)
    height = int(user_height // 5)
    if word_index % 2 == 0:
        x = 0
    else:
        x = width
    y = height * (word_index // 2)
    th = 3
    
    if blank:
        cv2.rectangle(words, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
        
    else:
        # Text settings
        if word_index < len(predicted_words):
            text = predicted_words[word_index][0]
        else:
            text = ""
        font_letter = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.6
        font_th = 1
        text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
        width_text, height_text = text_size[0], text_size[1]
        text_x = int((width - width_text) / 2) + x
        text_y = int((height + height_text) / 2) + y
        
        if word_select is True:
            cv2.rectangle(words, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
            cv2.putText(words, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
        else:
            cv2.rectangle(words, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
            cv2.putText(words, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)
    


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
    font_scale = 0.3
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
    global frame_selector
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
    global simulation_time
    global active_letter
    global selected_option
    global current_valid_word
    global new_word_added
    global word_count
    
    
    _, frame = cap.read()    
    frame = rescale_frame(frame, percent=50)
    rows, cols, _ = frame.shape
    frame[rows - 30: rows, 0: cols] = (255, 255, 255)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    # App Related content
    if app != -1 and not app_opened:  
        OpenApp()

    
    if frame_selector == 0:
        blank_Apps()
        blank_Keyboard()
        if current_valid_word != "":
            put_words()
        else:
            blank_words()
        
        for i in range(len(options.keys())):
            if i == selected_option:
                light = True
            else:
                light = False
            draw_options(i, light)
            
        app_frames = (app_frames + 1) % (simulation_time+1)
        if app_frames == simulation_time:
            selected_option = (selected_option + 1) % (len(options.keys()))
            
    elif frame_selector == 1: # APP Selection Frame is selected.
        blank_Keyboard()
        blank_Options()
        if current_valid_word != "":
            put_words()
        else:
            blank_words()
            
        for i in range(icon_count):
            if app == -1: # Future remove
                if i == icon_index:
                    light = True
                else:
                    light = False
            else:
                light = False
            draw_icon(i, light)
        
        app_frames = (app_frames + 1) % (simulation_time+1)
        if app_frames == simulation_time:
            icon_index = (icon_index + 1) % (icon_count)
            
    elif frame_selector == 2: # Keyboard Frame is selected
        blank_Apps()
        blank_Options()
        if current_valid_word != "":
            put_words()
        else:
            blank_words()
    
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
            
        
        # Keyboard Drawing
        # if app_opened:
        key_frames = (key_frames + 1) % (simulation_time+1)
            
        if select_keyboard_menu is True:
            if key_frames == simulation_time:
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
             if key_frames == simulation_time:
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
                if key_frames == simulation_time:
                    letter_index += 1
                    key_frames = 0
            else:
                if key_frames == simulation_time:
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
               
    
    elif frame_selector == 3: # Frequent Words 
        blank_Apps()
        blank_Keyboard()
        blank_Options()
            
        for i in range(10):
            if i == word_count:
                light = True
            else:
                light = False
            draw_words(i, light, False)
        
        app_frames = (app_frames + 1) % (simulation_time + 1)
        if app_frames == simulation_time:
            word_count = (word_count + 1) % (len(predicted_words))
    
    else:
        blank_Apps()
        blank_Keyboard()
        blank_Options()
        if current_valid_word != "":
            put_words()
        else:
            blank_words()
    
    
    
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
                
                # Window selector
                if frame_selector == 0:
                    if selected_option == 0:
                        frame_selector = 1
                        app = -1
                        app_opened = False
                        
                    elif selected_option == 1:
                        frame_selector = 2
                        
                    elif selected_option == 2:
                        frame_selector = 3
                    
                # App Selection Stuff
                elif frame_selector == 1 and app == -1 and not app_opened: # Opens App if not already opened
                    app = icon_index
                    frame_selector = 2
                
                # Keyboard Simulation Stuff
                elif frame_selector == 2:
                    if select_keyboard_menu is True:
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
                        
                        if word_check1(active_letter):
                            current_valid_word += active_letter
                            frame_selector = 0
                            new_word_added = True
                            Predict_Words()
                        else:
                            current_valid_word = ""
                        
                        if word_check2(active_letter):
                            text += active_letter
                        else:
                            text = ""
                        
                        if not word_check1(active_letter) and word_check2(active_letter):
                            current_valid_word = ""
                
                # Predicted Word Selection
                elif frame_selector == 3:
                    tmp_word = predicted_words[word_count][0]
                    pag.typewrite(tmp_word[len(current_valid_word):])
                    pag.press('space')
                    current_valid_word = ""
                    frame_selector = 2


    
    # Loading Meter
    percentage_blinking = blinking_frames / frames_to_blink
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(gray, (0, rows - 30), (loading_x, rows), (51, 51, 51), -1)
    
    
    general = np.concatenate((img_concate_Verti,Main_Options), axis = 1)

    # Options
    Option_Board = Image.fromarray(Option_Frame, 'RGB')
    Options_tk = ImageTk.PhotoImage(image = Option_Board)
    option_label.Options_tk = Options_tk
    option_label.configure(image = Options_tk)    
    
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
    
    # Predicted Words
    Pred_Words = Image.fromarray(words, 'RGB')
    Pred_Words_tk = ImageTk.PhotoImage(image = Pred_Words)
    words_label.Pred_Words_tk = Pred_Words_tk
    words_label.configure(image = Pred_Words_tk)
    
    if frame_selector == 0:
        option_label.after(10, show_frame)
    elif frame_selector == 1:
        app_label.after(10, show_frame)
    elif frame_selector == 2:
        keyboard_label.after(10, show_frame)
    elif frame_selector == 3:
        words_label.after(10, show_frame)    

 
    # User
    user = Image.fromarray(gray)
    user_tk = ImageTk.PhotoImage(image=user)
    user_label.user_tk = user_tk
    user_label.configure(image=user_tk)




show_frame()
root.mainloop()
cap.release()