def Menu_Cheek():
    import cv2
    import numpy as np
    import dlib
    from math import hypot
    import time
    import pyautogui
    import tkinter as tk
    from PIL import Image, ImageTk
    # from cheek_test_ver_03 import Cheek_Keyboard
    
    root = tk.Tk()
    root.title("Elocutor Home")
    root.config(background="#FFFFFF")
    root.attributes('-fullscreen', True)
    
    imageFrame = tk.Frame(root, width=600, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)
    
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("../Face_Landmarks/shape_predictor_68_face_landmarks.dat")
    cap = cv2.VideoCapture(0)
    images = {0:'Notepad', 1:'Chrome', 2:'This PC', 3:'Calculator', 4:'Exit'}
    
    
    
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
    
    while True:
        _, frame = cap.read()
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
            
            ratio = ver_line_length / hor_line_length
            
            if ratio < 1.10:
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
            
        cv2.imshow("User", frame)
        general=np.concatenate((img_concate_Verti,Main_Options),axis=1)
        cv2.imshow("Elocutor Home", general)
        #cv2.imshow("Icons", img_concate_Verti)
        if app != -1:
            break
        
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    
    if app == 0:
        pyautogui.press('win',interval=0.25)
        time.sleep(0.1)
        pyautogui.press('n')
        pyautogui.typewrite('otepad')
        time.sleep(1)
        pyautogui.press('enter')
    elif app == 1:
        pyautogui.press('win',interval=0.25)
        time.sleep(0.1)
        pyautogui.press('c')
        pyautogui.typewrite('hrome')
        time.sleep(1)
        pyautogui.press('enter')
    elif app == 2:
        pyautogui.press('win',interval=0.25)
        time.sleep(0.1)
        pyautogui.press('t')
        pyautogui.typewrite('his PC')
        time.sleep(1)
        pyautogui.press('enter')
    elif app == 3:
        pyautogui.press('win',interval=0.25)
        time.sleep(0.1)
        pyautogui.press('c')
        pyautogui.typewrite('alculator')
        time.sleep(1)
        pyautogui.press('enter')
        
        
    # Cheek_Keyboard()

Menu_Cheek()

# import numpy as np
# import cv2
# import tkinter as tk
# # import image
# from PIL import Image, ImageTk

# #Set up GUI
# window = tk.Tk()  #Makes main window
# window.wm_title("Elocutor")
# window.config(background="#FFFFFF")
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
# # window.geometry("%dx%d+0+0" % (screen_width, screen_height))
# window.attributes('-fullscreen', True)

# # print(screen_height, screen_width)

# #Graphics window
# imageFrame = tk.Frame(window, width=600, height=500)
# imageFrame.grid(row=0, column=0, padx=10, pady=2)

# #Capture video frames
# lmain = tk.Label(imageFrame)
# lmain.grid(row=0, column=0)
# cap = cv2.VideoCapture(0)
# def show_frame():
#     _, frame = cap.read()
#     cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#     img = Image.fromarray(cv2image)
#     imgtk = ImageTk.PhotoImage(image=img)
#     lmain.imgtk = imgtk
#     lmain.configure(image=imgtk)
#     lmain.after(10, show_frame)


# #Slider window (slider controls stage position)
# sliderFrame = tk.Frame(window, width=600, height=100)
# sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

# show_frame()  #Display 2
# window.mainloop()  #Starts GUI
# cap.release()
