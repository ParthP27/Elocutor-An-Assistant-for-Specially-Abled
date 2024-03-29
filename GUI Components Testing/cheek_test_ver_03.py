def Cheek_Keyboard():
    import cv2
    import numpy as np
    import dlib
    from math import hypot
    import time
    import pyautogui as pg
    cap = cv2.VideoCapture(0)
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")
    font = cv2.FONT_HERSHEY_COMPLEX
    font1 = cv2.FONT_HERSHEY_PLAIN
    
    # Keyboard settings
    keyboard = np.zeros((550, 1250, 3), np.uint8)
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
        # thickness
        width = 75
        height = 75
        th = 3
        if selection==2:
        # Keys
            if keyset==keys_set_1:
                x=(letter_index%8)*75
                y=100+(letter_index//8)*75
            else:
                x=625+(letter_index%8)*75
                y=100+(letter_index//8)*75
    
           
    
            # Text settings
            if(len(text)>1 and len(text)<4):
                font_scale = 1
                font_th = 1
            elif(len(text)>3):
                font_scale = 0.5
                font_th = 1
            else:
                font_scale = 2
                font_th = 2
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
            
            y=10
            if text=="L":
                x=10
            else:
                x=1150
            if letter_light is True:
                cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
            else:
                cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
            
    
    
              
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
            #print(ratio)
            if select_keyboard_menu is True:
                
                if ratio < 1.10:
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
                
            
            elif(ratio < 1.10 and select_line_menu is True):
                #flag_for_change=0
                cv2.putText(frame,"Selected",(5,100), font, 2, (0, 0, 0))
                # text += keys_set[letter_index]
                blinking_frames += 1
            
                if blinking_frames == frames_to_blink:
                    last_selected_line=line_selected
                    blinking_frames = 0
                    select_line_menu = False
            else:
                if ratio < 1.10:
                    cheek_move_counter+=1
                    if cheek_move_counter == frames_to_blink:
                        pg.press(active_letter)
                        cheek_move_counter = 0
                        select_keyboard_menu = True
                
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
        
        key = cv2.waitKey(1)
        if key == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()