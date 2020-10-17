

import cv2
import numpy as np
import dlib
from math import hypot
import time
#import time
import pyautogui as pg
import tkinter as tk




cap = cv2.VideoCapture(0)
#board = np.zeros((100, 600), np.uint8)
#board[:] = 255

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #../Face_Landmarks/
font = cv2.FONT_HERSHEY_COMPLEX
font1 = cv2.FONT_HERSHEY_PLAIN



#Getting the screen resolution

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
#print(screen_width,screen_height)

#Setting Keyboard size
resolutions=[[1920,1080],[1440,900],[1366,768]]
index_res=0
for i in resolutions:
    if(i[0]==screen_width and i[1]==screen_height):
        index_res=resolutions.index(i)

        
# thickness
#if(index_res==0):

#Magic Portion (Control Centre)
gap=30-(5*index_res)    
width = (resolutions[index_res][0]//2-gap)//16 #57-(24*index_res)
height = (resolutions[index_res][1]//3-2*gap)//6 #55-(10*index_res)
th = int(3-(0.5*index_res))


# Keyboard settings
keyboard = np.zeros((height*6+gap*2, width*16+gap, 3), np.uint8)
"""keys_set = {0:'esc',1:'f1',2:'f2',3:'f3',4:'f4',5:'f5',6:'f6',7:" ",8: " ",9:'f7',10:'f8',11:'f9',12:'f10',13:'f11',14:'f12',15:'del',16: " ",17: " ",
              18:'0', 19:'1', 20:'2',21: '3',22: '4',23: '5',24: '6',25: " ",26:'7', 27:'8', 28:'9',29: '0',30: '-',31: '=',32: 'backspace',33: " ",
              34: "tab", 35: "q", 36: "w", 37: "e", 38: "r",39: "t",40: " ",41: " ",42: "y", 43: "u", 44: "i", 45: "o", 46: "p",47: "[",48: "]",49:"|",
              50: "capslock", 51: "a", 52: "s", 53: "d",54: "f",55: "g",56: " ",57: " ",58: "h", 59: "j", 60: "k",61: "l",62: ";",63: "'",64: "enter",65: " ",
              66: "shiftleft",67: "z",68: "x",69: "c",70: "v",71: " ",72: " ",73: " ",74: "b",75: "n",76: "m",77: ",",78: ".",79: "/",80: "shiftright",81: " ",
              82: "ctrlleft",83: "fn",84: "winleft",85: "altleft",86: "space",87:"altright",88: "ctrlright",89:"up",90:"down",91:"left",92:"right"}"""


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

              
              
              
              
              

def draw_letters(letter_index, text, letter_light,keyset,selection):
  
    if selection==2:
    # Keys
        if keyset==keys_set_1:
            x=(letter_index%8)*width
            y=gap*2+(letter_index//8)*height
        else:
            x=width*8+gap+(letter_index%8)*width
            y=gap*2+(letter_index//8)*height

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
        text_x = int((width - width_text) / 2) + x
        text_y = int((height + height_text) / 2) + y

        if letter_light is True:
            cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
        else:
            cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)
    else:
        
        y=2
        if text=="L":
            x=2
        else:
            x=width*15+gap-2
        #print(x,y,width,height,th)  
        if letter_light is True:
            cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        else:
            cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
        

        

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    #hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    #ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye
          
# Counters
frames = 0
letter_index = 0
blinking_frames = 0
frames_to_blink = 9
frames_active_letter = 20
flag_for_change=0

# Text and keyboard settings
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
select_keyboard_menu = True
keyboard_selection_frames = 0
mode=0
side=0

#Lines wise 

line_selected=0
select_line_menu=False
cheek_move_counter=0
last_selected_line=0

while True:
    _, frame = cap.read()
    # rows, cols, _ = frame.shape
    rows, cols, _ = frame.shape
    keyboard[:] = (26, 26, 26)
    frames += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame[rows - 50: rows, 0: cols] = (255, 255, 255)
    
       
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

    
    # Face detection
    faces = detector(gray)
    for face in faces:
        
        landmarks = predictor(gray, face)

        left_eye, right_eye = eyes_contour_points(landmarks)

            # Detect blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

            # Eyes color
        cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
        cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)        # print(ratio)
        #print(ratio)
        if select_keyboard_menu is True:
            
            if blinking_ratio > 5:
                cv2.putText(frame,"Selected",(5,100), font, 2, (0, 0, 0))
                # text += keys_set[letter_index]
                keyboard_selection_frames += 1
                
                if keyboard_selection_frames == 10:
                    if side==0:
                       keyboard_selected="left"
                       
                    else:
                        keyboard_selected="right"
                    select_keyboard_menu = False
                    flag_for_change=1
                        #right_sound.play()
                        # Set frames count to 0 when keyboard selected
                    frames = 0
                    
                    keyboard_selection_frames = 0
                    select_line_menu=True
                    #blinking_frames = 0
            
        
        elif(blinking_ratio > 5 and select_line_menu is True):
            #flag_for_change=0
            cv2.putText(frame,"Selected",(5,100), font, 2, (0, 0, 0))
            # text += keys_set[letter_index]
            blinking_frames += 1
        
            if blinking_frames == frames_to_blink:
                last_selected_line=line_selected
                blinking_frames = 0
                select_line_menu = False
        else:
            if blinking_ratio > 5:
                cheek_move_counter+=1
                if cheek_move_counter == frames_to_blink:
                    pg.press(active_letter)
                    cheek_move_counter = 0
                    select_keyboard_menu = True
                    line_selected=0
                    letter_index=0
            
      # for keyboard
        if select_keyboard_menu is True:
            
            if frames == frames_active_letter:
                side=(side+1)%2
                frames = 0
                #print(side)
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
             if frames == frames_active_letter:
                line_selected+=1
                frames = 0
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
            if(flag_for_change==1):
                flag_for_change=0
                if frames == 15:
                    letter_index += 1
                    frames = 0
            else:
                if frames == frames_active_letter:
                    letter_index += 1
                    frames = 0
            
            if letter_index == 8:
                select_keyboard_menu=True
                letter_index = 0
                
      
            if(keys_set==keys_set_1):
                
                     lcount=8*last_selected_line
                 
                     
                     for j in range(8):
                        if j == letter_index:
                            light = True
                        else:
                            light = False
                        #print(lcount)
                        draw_letters(lcount, keys_set_1[lcount], light,keys_set_1,2)
                        lcount+=1
                        
                     for i in range(48):
                        draw_letters(i, keys_set_2[i], False,keys_set_2,2)
            else:
               
                     lcount=8*last_selected_line
                 
                     
                     for j in range(8):
                        if j == letter_index:
                            light = True
                        else:
                            light = False
                        
                        draw_letters(lcount, keys_set_2[lcount], light,keys_set_2,2)
                        lcount+=1
                     for i in range(48):
                        draw_letters(i, keys_set_1[i], False,keys_set_1,2)

    if select_keyboard_menu is True: 
        percentage_blinking = keyboard_selection_frames / frames_to_blink
    elif select_line_menu is True:
        percentage_blinking = blinking_frames / frames_to_blink
    else:
        percentage_blinking = cheek_move_counter / frames_to_blink
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)
    
        
    #cv2.putText(board,text, (0, 50), font1, 1, 0, 1)
    
    cv2.imshow("Elocutor", frame)
    cv2.imshow("Virtual keyboard", keyboard)
    #cv2.imshow("Board", board)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
