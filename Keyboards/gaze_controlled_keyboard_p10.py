import cv2
import numpy as np
import dlib
from math import hypot
#import pyglet
import time
import pyautogui as pg
#from pynput.keyboard import Key, Controller
# Load sounds
#sound = pyglet.media.load("sound.wav", streaming=False)
#left_sound = pyglet.media.load("left.wav", streaming=False)
#right_sound = pyglet.media.load("right.wav", streaming=False)
#keyboard1=Controller()
cap = cv2.VideoCapture(0)
#board = np.zeros((300, 1400), np.uint8)
#board[:] = 255

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Keyboard settings
keyboard = np.zeros((600, 800, 3), np.uint8)
keys_set_1 = {0:'esc',1:'f1',2:'f2',3:'f3',4:'f4',5:'f5',6:'f6',7:" ",8: " ",
              9:'0', 10:'1', 11:'2',12: '3',13: '4',14: '5',15: '6',16: " ",
              17: "tab", 18: "q", 19: "w", 20: "e", 21: "r",22: "t",23: " ",24: " ",
              25: "capslock", 26: "a", 27: "s", 28: "d",29: "f",30: "g",31: " ",32: " ",
              33: "shiftleft",34: "z",35: "x",36: "c",37: "v",38: " ",39: " ",40: " ",
              41: "ctrlleft",42: "fn",43: "winleft",44: "altleft",45: "space"
              }
keys_set_2 = {0:'f7',1:'f8',2:'f9',3:'f10',4:'f11',5:'f12',6:'del',7: " ",8: " ",
              9:'7', 10:'8', 11:'9',12: '0',13: '-',14: '=',15: 'backspace',16: " ",
              17: "y", 18: "u", 19: "i", 20: "o", 21: "p",22: "[",23: "]",24:"|",
              25: "h", 26: "j", 27: "k",28: "l",29: ";",30: "'",31: "enter",32: " ",
              33: "b",34: "n",35: "m",36: ",",37: ".",38: "/",39: "shiftright",40: " ",
              41:"altright",42: "ctrlright",43:"up",44:"down",45:"left",46:"right"}

def draw_letters(letter_index, text, letter_light):
    # Keys
    x=(letter_index%8)*100
    y=(letter_index//8)*100
            

    width = 100
    height = 100
    th = 3 # thickness

    # Text settings
    if(len(text)>1 and len(text)<4):
        font_scale = 2
        font_th = 1
    elif(len(text)>3):
        font_scale = 1
        font_th = 1
    else:
        font_scale = 5
        font_th = 2
    font_letter = cv2.FONT_HERSHEY_PLAIN

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

def draw_menu():
    rows, cols, _ = keyboard.shape
    th_lines = 4 # thickness lines
    cv2.line(keyboard, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
             (51, 51, 51), th_lines)
    cv2.putText(keyboard, "LEFT", (80, 300), font, 6, (255, 255, 255), 5)
    cv2.putText(keyboard, "RIGHT", (80 + int(cols/2), 300), font, 6, (255, 255, 255), 5)


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

def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
    # cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)
    #print("right_white",right_side_white)
    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

# Counters
frames = 0
letter_index = 0
blinking_frames = 0
frames_to_blink = 2
frames_active_letter = 7

# Text and keyboard settings
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
select_keyboard_menu = True
keyboard_selection_frames = 0

  
while True:
        _, frame = cap.read()
        #frame = cv2.resize(frame, None, fx=0.8, fy=0.8)
        rows, cols, _ = frame.shape
        keyboard[:] = (26, 26, 26)
        frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Draw a white space for loading bar
        frame[rows - 50: rows, 0: cols] = (255, 255, 255)


                    
        if select_keyboard_menu is True:
            draw_menu()

        # Keyboard selected
        if keyboard_selected == "left":
            keys_set = keys_set_1
        else:
            keys_set = keys_set_2
        active_letter = keys_set[letter_index]

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
            cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)


            if select_keyboard_menu is True:
                # Detecting gaze to select Left or Right keybaord
                gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
                gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
                #if(gaze_ratio_right_eye==5):
                        #print("right",gaze_ratio_right_eye)
                gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
                
                #if(gaze_ratio==5):
                        #print(gaze_ratio)
                if gaze_ratio <= 0.85:
                    #print("right",gaze_ratio)
                    keyboard_selected = "right"

                    keyboard_selection_frames += 1
                    # If Kept gaze on one side more than 15 frames, move to keyboard
                    if keyboard_selection_frames == 6:
                        select_keyboard_menu = False
                        #right_sound.play()
                        # Set frames count to 0 when keyboard selected
                        frames = 0
                        keyboard_selection_frames = 0
                    if keyboard_selected != last_keyboard_selected:
                        last_keyboard_selected = keyboard_selected
                        keyboard_selection_frames = 0
                elif gaze_ratio>1.1:
                    keyboard_selected = "left"
                    #print("left",gaze_ratio)
                    #if(gaze_ratio>3):
                        #print(gaze_ratio)
                    keyboard_selection_frames += 1
                    # If Kept gaze on one side more than 15 frames, move to keyboard
                    if keyboard_selection_frames == 6:
                        select_keyboard_menu = False
                        #left_sound.play()
                        # Set frames count to 0 when keyboard selected
                        frames = 0
                    if keyboard_selected != last_keyboard_selected:
                        last_keyboard_selected = keyboard_selected
                        keyboard_selection_frames = 0

            else:
                # Detect the blinking to select the key that is lighting up
                if blinking_ratio > 5:
                    #cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
                    blinking_frames += 1
                    frames -= 1

                    # Show green eyes when closed
                    cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                    cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

                    # Typing letter
                    if blinking_frames == frames_to_blink:
                        if active_letter != "<" and active_letter != "_":
                                #time.sleep(2)
                            if(active_letter == "/"):
                                pg.press("enter")
                            else:
                                
                                pg.press(active_letter)
                                #pg.release(active_letter)
                            #text += active_letter
                        if active_letter == "_":
                            text += " "
                        #sound.play()
                        select_keyboard_menu = True
                        # time.sleep(1)

                else:
                    blinking_frames = 0


        # Display letters on the keyboard
        if select_keyboard_menu is False:
            if frames == frames_active_letter:
                letter_index += 1
                frames = 0
            if letter_index == 47 and keys_set==keys_set_2:
                letter_index = 0
            if letter_index == 46 and keys_set==keys_set_1:
                letter_index = 0
            if(keys_set==keys_set_1):
                for i in range(46):
                    if i == letter_index:
                        light = True
                    else:
                        light = False
                    draw_letters(i, keys_set[i], light)
            else:
                for i in range(47):
                    if i == letter_index:
                        light = True
                    else:
                        light = False
                    draw_letters(i, keys_set[i], light)

        # Show the text we're writing on the board
        
        #cv2.putText(board, text, (80, 100), font, 9, 0, 3)

        # Blinking loading bar
        percentage_blinking = blinking_frames / frames_to_blink
        loading_x = int(cols * percentage_blinking)
        cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)


        cv2.imshow("Frame", frame)
        cv2.imshow("Virtual keyboard", keyboard)
        #cv2.imshow("Board", board)

        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()
