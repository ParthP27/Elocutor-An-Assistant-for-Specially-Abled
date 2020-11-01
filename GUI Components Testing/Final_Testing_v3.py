


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
autoc.load()
import pyttsx3 #pip install pyttsx3

#-------------------------AUDIO CONTROL CENTER-------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#------------------------------------- Main Window ------------------------------------------------
root = tk.Tk()
root.title("Elocutor")
root.iconbitmap(r"wheelchair_person.ico")
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

frame_selector = 0
'''
    0 : Option Frame (Apps, Keyboard, Words, etc.)
    1 : App Selection Frame
    2 : Keyboard Frame
    3 : Frequent Words
    4 : Frequent Options
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
images = {0:'Notepad', 1:'Chrome', 2:'This PC', 3:'Calculator', 4:'You Tube', 5:'Setting', 6:'Exit'}
icon_count = len(images.keys())

# Frame Selector Frame (Options Wali Frame BABU BHAIYA)
options = {0:'Applications', 1:'Keyboard', 2:'Words', 3:'Freq. Controls'}
selected_option = 0

# Selection Criteria
app_frames = 0
key_frames = 0
blinking_frames = 0
frames_to_blink = 20
simulation_time = 20


#Colors used
selection_color = (204, 202, 196) 
Overall_Color = (13, 12, 13)#(32, 32, 32)#(47, 52, 55)#(26, 26, 26)
Overall_Color_Hash =  "#0d0c0d" #"#202020"   #"#1a1a1a"
Text_Color_Hash = "#eaeaea"
Text_Color = (234, 234, 234)

# Variables used in function to Open App
icon_index = 0
selected = 0
app = -1
app_opened = False
opened_apps = []

# Frequent Options for easier use
freq_count = 0

freq_options = {
                0 : {
                        0:('Save', ('ctrlleft', 's')), 1:('Enter', 'enter'), 2:('Up ^', 'up'), 3:('Down', 'down'),
                        4:('Left <-', 'left'), 5:('Right ->', 'right'), 6:('Speak', "call"), 7:('Exit', 'exit')
                    }, 
                1 : {
                        0:('New Tab', ('ctrlleft', 't')), 1:('Enter', 'enter'), 2:('Tab', 'tab'), 3:('Up ^', 'up'), 
                        4:('Left <-', 'left'), 5:('Right ->', 'right'), 6:('Down', 'down'), 7:('Exit', 'exit')
                    },
                2 : {
                        0:('Tab', 'tab'), 1:('Enter', 'enter'), 2:('Up ^', 'up'), 3:('Down', 'down'),
                        4:('Left <-', 'left'), 5:('Right ->', 'right'), 6:('Backspace', 'backspace'), 7:('Exit', 'exit')
                    },
                3 : {
                        0:('+', '+'), 1:('-', '-'), 2:('*', '*'), 3:('/', '/'),
                        4:('.', '.'), 5:('=', 'enter'), 6:('Tab', 'tab'), 7:('Exit', 'exit')
                    },
              
                4:  {
                        0:('Tab -> 6', 'tab 6'), 1:('Enter', 'enter'), 2:('Tab', 'tab'), 3:('Up ^', 'up'), 
                        4:('Left <-', 'left'), 5:('Right ->', 'right'), 6:('Down', 'down'), 7:('Exit', 'exit')
                    },
                
                5:  {
                    },
                
                6:  {
                    }
               }
'''
    Apps Number is given to switch between
        0 : Notepad
        1 : Chrome
        2 : This PC
        3 : Calculator

'''

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

#Flags for window changes(no need touch)
flag_for_freq_options=0
flag_for_word_predictor=0
flag_app_to_menu=0

# -------------- ALL FRAMES -----------------
title_frame = tk.Frame(root, bg = Overall_Color_Hash, width = full_width, height = title_height)
apps_frame = tk.Frame(root, bg = Overall_Color_Hash, width = app_width, height = app_height)
user_frame = tk.Frame(root, bg = Overall_Color_Hash, width = user_width, height = user_height)
freq_title_frame = tk.Frame(root, bg =  "#1a1919" , width = user_width-5, height = (user_height//5))
freq_option_frame = tk.Frame(root, bg = Overall_Color_Hash, width = user_width, height = user_height)
selection_frame = tk.Frame(root, bg = Overall_Color_Hash, width = frame_selection_width, height = (user_height*4//5))
words_frame = tk.Frame(root, bg = Overall_Color_Hash, width = words_frame_width, height = user_height)
keyboard_frame = tk.Frame(root, bg = Overall_Color_Hash, width = full_width, height = keyboard_height)

root.configure(bg = Overall_Color_Hash)
# ------------- Layout of all frames -----------
title_frame.place(x = 0,y = 0)
apps_frame.place(x = 0, y = title_height)
freq_title_frame.place(x = app_width+5, y = title_height)
freq_option_frame.place(x = app_width, y = title_height + (user_height//5))
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
#logo = tk.PhotoImage(file = "logos_pollos.png")
#logo = logoz.resize((250, 250), Image. ANTIALIAS)
#photoimage= logo.subsample(2, 2)
logo= cv2.imread("logos_pollos.png")
logo =   cv2.resize(logo, (0, 0), fx = 0.35, fy = 0.35)  

title_label = tk.Label(title_frame,background = Overall_Color_Hash)#, text = "Elocuter", background = "white", foreground = "black", font=("Helvetica", 25), width = full_width // 18)
title_label.place(x=full_width//2.5,y=-1)

logo = Image.fromarray(logo, 'RGB')
title_image_tk = ImageTk.PhotoImage(image=logo)
title_label.title_image_tk = title_image_tk
title_label.configure(image=title_image_tk)


app_label = tk.Label(apps_frame,background = "#757575")
app_label.pack()

user_label = tk.Label(user_frame,background = "#757575")
user_label.pack()

keyboard_label = tk.Label(keyboard_frame,background = "#757575")
keyboard_label.pack()

option_label = tk.Label(selection_frame,background = "#757575")
option_label.pack()

words_label = tk.Label(words_frame,background = "#757575")
words_label.pack()

freq_option_label = tk.Label(freq_option_frame,background = "#757575")
freq_option_label.pack()


freq_title_label = tk.Label(freq_title_frame, text = "'Patience Is Virtue'", background =  "#1a1919" ,foreground = Text_Color_Hash, font=("Helvetica", 15))
Author_title_label = tk.Label(freq_title_frame, text = "-William Langland", background =  "#1a1919" ,foreground = Text_Color_Hash, font=("Helvetica", 10))

freq_title_label.place(x = (user_width//5), y = 10)
Author_title_label.place(x = (user_width//2), y = 35)



#---------------------------- Whole Code and Logic for app selection and User video stream--------------------------

# Landmarks Detector
detector = dlib.get_frontal_face_detector()
#predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

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


    
#Experimental round corners
"""
def rounded_rectangle(src, top_left, bottom_right, radius=1, color=255, thickness=1, line_type=cv2.LINE_AA):

    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3

    p1 = top_left
    p2 = (bottom_right[1], top_left[1])
    p3 = (bottom_right[1], bottom_right[0])
    p4 = (top_left[0], bottom_right[0])

    height = abs(bottom_right[0] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/2))

    if thickness < 0:

        #big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1] + corner_radius)
        bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

        top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
        bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

        all_rects = [
        [top_left_main_rect, bottom_right_main_rect], 
        [top_left_rect_left, bottom_right_rect_left], 
        [top_left_rect_right, bottom_right_rect_right]]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
    cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
    cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
    cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color ,thickness, line_type)
    cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color , thickness, line_type)
    cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90,   color , thickness, line_type)
    cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90,  color , thickness, line_type)

    return src     """

#----------------------------- Option Wali Frame--------------------------------------------
#Option_Frame=cv2.imread("blur-white.jpg")  
#Option_Frame=cv2.resize(Option_Frame, (int(frame_selection_width),len(options.keys())*(int(user_height) // 4 - 15)+int(user_height) // 4 - 15))
#print((len(options.keys())*(int(user_height) // 4 - 15)+int(user_height) // 4 - 15, int(frame_selection_width)))
#Option_Frame=rounded_rectangle(src=Option_Frame, top_left=[0,0],thickness=2, bottom_right=[len(options.keys())*(int(user_height) // 4 - 15)+int(user_height) // 4 - 15+50,int(frame_selection_width)], radius= 0.3)
#print(Keyboard_height*6+Keyboard_gap*2)
Option_Frame = np.full((len(options.keys())*(int(user_height) // 4 - 15)+int(user_height) // 4 - 15, int(frame_selection_width)-5, 3),Overall_Color, np.uint8)
def draw_options(option_index, option_select):
    width = int(frame_selection_width) - 20
    height = int(user_height) // 4 - 15
    x = 10
    y = Keyboard_gap + (option_index * (height+2))
    
    th = 3 # thickness

    # Text settings 
    text = options[option_index]
    font_letter = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.8
    font_th = 1
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    
    if option_select is True:
        cv2.rectangle(Option_Frame, (x + th, y + th), (x + width - th, y + height - th),selection_color, -1)
        cv2.putText(Option_Frame, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(Option_Frame, (x + th, y + th), (x + width - th, y + height - th), Overall_Color, -1)
        cv2.putText(Option_Frame, text, (text_x, text_y), font_letter, font_scale, Text_Color, font_th)
        

     

#----------------------------- Frequently used options Frame--------------------------------------------
#Frequent_Options = np.zeros((int(user_height//5)*4, int(user_width), 3), np.uint8)
#Frequent_Options=rounded_rectangle(src=Frequent_Options, top_left=[0,0],thickness=2, bottom_right=[int(user_height // 5) * 4, int(user_width // 2)*2], radius= 1)
Frequent_Options = np.full((int(user_height//5)*4, int(user_width), 3),Overall_Color, np.uint8)

def draw_freq_options(freq_index, freq_select, blank):
    global opened_apps
    global freq_options
    global flag_for_freq_options
    global Frequent_Options
    width = int(user_width // 2)
    height = int(user_height // 5)
    
    if freq_index % 2 == 0:
        x = 0
    else:
        x = width
    y = height * (freq_index // 2)
    th = 3

    if blank:
        #cv2.rectangle(Frequent_Options, (x + th, y + th), (x + width - th, y + height - th), (0, 0, 0), -1)
        font_letter = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.7
        font_th = 0
        #cv2.rectangle(Frequent_Options, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        #(int(user_height // 5) * 4)//3, int(user_width // 2)
        #rec="Frequent Options"
        cv2.putText(Frequent_Options, "Frequent Options", (user_width // 5,(int(user_height//5)*4)//2), font_letter, font_scale, Text_Color, font_th)
        
    else:
        if(flag_for_freq_options==0):
            flag_for_freq_options+=1
            
            Frequent_Options = np.full((int(user_height//5)*4, int(user_width), 3),Overall_Color, np.uint8)
        # Text settings
        text = freq_options[opened_apps[0]][freq_index][0]
        font_letter = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.7
        font_th = 1
        text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
        width_text, height_text = text_size[0], text_size[1]
        text_x = int((width - width_text) / 2) + x
        text_y = int((height + height_text) / 2) + y
        #rec="Frequent Options"
        #cv2.putText(Frequent_Options, "Frequent Options", (user_width // 5,(int(user_height//5)*4)//2), font_letter, font_scale, (0, 0, 0), font_th)
        if freq_select is True:
            cv2.rectangle(Frequent_Options, (x + th, y + th), (x + width - th, y + height - th), selection_color, -1)
            cv2.putText(Frequent_Options, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
        else:
            cv2.rectangle(Frequent_Options, (x + th, y + th), (x + width - th, y + height - th), Overall_Color, -1)
            cv2.putText(Frequent_Options, text, (text_x, text_y), font_letter, font_scale, Text_Color, font_th)


#--------------------------------- Predicted Words Frame --------------------------
#words = np.zeros((int(user_height), int(words_frame_width), 3), np.uint8)
words = np.full((int(user_height), int(words_frame_width), 3),Overall_Color, np.uint8)

def draw_words(word_index, word_select, blank):
    global predicted_words
    global flag_for_word_predictor
    global words
    width = int(words_frame_width // 2)
    height = int(user_height // 5)
    if word_index % 2 == 0:
        x = 0
    else:
        x = width
    y = height * (word_index // 2)
    th = 3
    
    if blank:
        if(flag_for_word_predictor==0):
            flag_for_word_predictor=(flag_for_word_predictor+1)%2
            words = np.full((int(user_height), int(words_frame_width), 3),Overall_Color, np.uint8)
        #cv2.rectangle(words, (x + th, y + th), (x + width - th, y + height - th), (0, 0, 0), -1)
        font_letter = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.7
        font_th = 1
        cv2.putText(words, "Word Completion and Prediction", (int(words_frame_width)// 10,(int(user_height))//2), font_letter, font_scale, Text_Color, font_th)

    else:
        
        # Text settings
        if(flag_for_word_predictor==1):
            flag_for_word_predictor=(flag_for_word_predictor+1)%2
            words = np.full((int(user_height), int(words_frame_width), 3),Overall_Color, np.uint8)
        if word_index < len(predicted_words):
            text = predicted_words[word_index][0]
        else:
            text = ""
        font_letter = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.7
        font_th = 1
        text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
        width_text, height_text = text_size[0], text_size[1]
        text_x = int((width - width_text) / 2) + x
        text_y = int((height + height_text) / 2) + y
        
        if word_select is True:
            cv2.rectangle(words, (x + th, y + th), (x + width - th, y + height - th), selection_color, -1)
            cv2.putText(words, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
        else:
            cv2.rectangle(words, (x + th, y + th), (x + width - th, y + height - th), Overall_Color, -1)
            cv2.putText(words, text, (text_x, text_y), font_letter, font_scale, Text_Color, font_th)
    


#----------------------------- Application Icons Selection Menu ---------------------------------

Main_Options = np.full((len(images.keys())*apps_icon_height, apps_icon_width, 3),Overall_Color, np.uint8)

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
    
    if(len(text)>7):
        font_scale = 0.6
    else:
        font_scale = 0.7
    font_th = 1
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    
    if image_select is True:
        cv2.rectangle(Main_Options, (x + th, y + th), (x + width - th, y + height - th), selection_color, -1)
        cv2.putText(Main_Options, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(Main_Options, (x + th, y + th), (x + width - th, y + height - th), Overall_Color, -1)
        cv2.putText(Main_Options, text, (text_x, text_y), font_letter, font_scale, Text_Color, font_th)
        
        
# Function That Opens an App
def OpenApp():
    global app
    global app_opened
    global opened_apps
    # print(opened_apps)
    if app not in opened_apps:
        opened_apps.insert(0, app)
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
            pag.press('win',interval=0.25)
            time.sleep(0.1)
            pag.press('S')
            pag.typewrite('ettings')
        elif app == 4:
            pag.press('win',interval=0.25)
            time.sleep(0.1)
            pag.press('c')
            pag.typewrite('hrome')
            pag.press('enter')
            time.sleep(0.7)
            pag.typewrite('www.youtube.com/')
            pag.press("end")
            pag.press('backspace')
            
        elif app == 6:
            root.destroy()
        
        if app != 6:
            time.sleep(1)
            pag.press('enter')
            time.sleep(2)
            pag.hotkey('win', 'left')
            time.sleep(1)
            pag.click(x = (screen_width//2 - 50), y = (screen_height - 100))
    
    else:
        pag.keyDown('altleft')
        for i in range(opened_apps.index(app)):
            pag.press('tab')
        pag.keyUp('altleft')
        opened_apps.remove(app)
        opened_apps.insert(0, app)
        
    app_opened = True
    # print(opened_apps)
    
# ------------------------------- END : Application Selection ----------------------------------------
    
# ------------------------------------------------- Keyboard Section -------------------------------------------
keyboard = np.full((Keyboard_height*6+Keyboard_gap*2, Keyboard_width*16+Keyboard_gap, 3),Overall_Color, np.uint8)

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
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), selection_color, -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
        else:
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), Overall_Color, -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, Text_Color, font_th)
    else:
        
        y = 2
        if text == "L":
            x = 2
        else:
            x = Keyboard_width * 15 + Keyboard_gap - 2
        if letter_light is True:
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), selection_color, -1)
        else:
            cv2.rectangle(keyboard, (x + Keyboard_th, y + Keyboard_th), (x + Keyboard_width - Keyboard_th, y + Keyboard_height - Keyboard_th), (54, 53, 53), -1)


# ---------------------------------------END : Keyboard Part --------------------------------------------------

# ------------------------- Functions to draw blank frames without simulation ------
def blank_Apps():
    #flag_app_to_menu=0
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
        draw_words(1, False, True)
        
def put_freq_options():
    """if len(opened_apps) != 0:
        if(flag_for_freq_options==0):
            flag_for_freq_options+=1
            Frequent_Options = np.zeros((int(user_height//5)*4, int(user_width), 3), np.uint8)
        for i in range(len(freq_options[opened_apps[0]].items())):
            draw_freq_options(i, False, False)
    else:
        
        font_letter = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.7
        font_th = 0
        #cv2.rectangle(Frequent_Options, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        #(int(user_height // 5) * 4)//3, int(user_width // 2)
        rec="Frequent Options"
        cv2.putText(Frequent_Options, rec, (user_width // 5,(int(user_height//5)*4)//2), font_letter, font_scale, (255, 255, 255), font_th)
    """
    if len(opened_apps) != 0:
        for i in range(len(freq_options[opened_apps[0]].items())):
            draw_freq_options(i, False, False)
    
    else:
        #for i in range(8):
            draw_freq_options(1, False, True)
    

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
    global Frequent_Options
    global freq_count
    global opened_apps
    global freq_options
    
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
        put_freq_options()
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
        put_freq_options()
        global flag_app_to_menu
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
            if icon_index == (0):
                flag_app_to_menu+=1
            icon_index = (icon_index + 1) % (icon_count)
            
            if(flag_app_to_menu==2):
                    flag_app_to_menu=0
                    frame_selector = 0
            
    elif frame_selector == 2: # Keyboard Frame is selected
        blank_Apps()
        blank_Options()
        put_freq_options()
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
        if len(predicted_words) == 0:
            frame_selector = 0
        else:
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
        
    elif frame_selector == 4: # Frequent Options
        if len(opened_apps) == 0:
            frame_selector = 0
        else:           
            
            for i in range(len(freq_options[opened_apps[0]].items())):
                if i == freq_count:
                    tmp_light = True
                else:
                    tmp_light = False
                draw_freq_options(i, tmp_light, False)
                
            app_frames = (app_frames + 1) % (simulation_time + 1)
            if app_frames == simulation_time:
                freq_count = (freq_count + 1) % (len(freq_options[opened_apps[0]].items()))
            
                
    else:
        blank_Apps()
        blank_Keyboard()
        blank_Options()
        put_freq_options()
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
                        current_valid_word = ""
                        
                    elif selected_option == 1:
                        frame_selector = 2
                        
                    elif selected_option == 2:
                        frame_selector = 3
                    
                    elif selected_option == 3:
                        frame_selector = 4
                    
                # App Selection Stuff
                elif frame_selector == 1 and app == -1 and not app_opened: # Opens App if not already opened
                    app = icon_index
                    frame_selector = 0
                
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
                        frame_selector = 0
                        
                        if word_check1(active_letter):
                            current_valid_word += active_letter
                            
                            new_word_added = True
                            Predict_Words()
                        else:
                            current_valid_word = ""
                        
                        if word_check2(active_letter):
                            text += active_letter
##                        else:
##                            text = ""
                        
                        if not word_check1(active_letter) and word_check2(active_letter):
                            current_valid_word = ""
                
                # Predicted Word Selection
                elif frame_selector == 3:
                    tmp_word = predicted_words[word_count][0]
                    pag.typewrite(tmp_word[len(current_valid_word):])
                    pag.press('space')
                    text=text[:len(text)-len(current_valid_word)]
                    text+=tmp_word+" "
                    current_valid_word = ""
                    frame_selector = 0
                
                elif frame_selector == 4:
                    temp = freq_options[opened_apps[0]][freq_count][1]
                    if temp == 'exit':
                        frame_selector = 0
                    else:
                        if type(temp) is tuple:
                            pag.hotkey(temp[0], temp[1])
                        else:
                            if ( temp == "call" ):
                                speak(text)
                                
                            elif ( temp == "tab 6" ):
                                temp_split = temp.split()
                                
                                for ii in range (int(temp_split[1])): 
                                    pag.press(temp_split[0])
                            else:
                                pag.press(temp)


    
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
    
    Freq_Options = Image.fromarray(Frequent_Options, 'RGB')
    Freq_Options_tk = ImageTk.PhotoImage(image = Freq_Options)
    freq_option_label.Freq_Options_tk = Freq_Options_tk
    freq_option_label.configure(image = Freq_Options_tk)
    
    if frame_selector == 0:
        option_label.after(10, show_frame)
    elif frame_selector == 1:
        app_label.after(10, show_frame)
    elif frame_selector == 2:
        keyboard_label.after(10, show_frame)
    else:
        words_label.after(10, show_frame)

 
    # User
    user = Image.fromarray(gray)
    user_tk = ImageTk.PhotoImage(image=user)
    user_label.user_tk = user_tk
    user_label.configure(image=user_tk)




show_frame()
root.mainloop()
cap.release()
