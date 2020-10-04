# -*- coding: utf-8 -*-


# import cv2
# import numpy as np

# Main_Options = np.zeros((200, 500, 3), np.uint8)
# th = 3
# cv2.rectangle(Main_Options, (0+th, 0+th),  (0+500-th, 0+100-th), (255,255,255), -1)
# cv2.putText(Main_Options, "Select Detection Method", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

# images = {0:'a', 1:'b', 2:'c'}

# def draw_icon(image_index, image_select):
#     if image_index == 0:
#         x = 0
#         y = 100
#     elif image_index == 1:
#         x = 100
#         y = 100
#     else:
#         x = 200
#         y = 100
#     width = 100
#     height = 100
    
#     th = 3 # thickness

#     # Text settings
#     text = images[image_index]
#     font_letter = cv2.FONT_HERSHEY_PLAIN
#     font_scale = 5
#     font_th = 4
#     text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
#     width_text, height_text = text_size[0], text_size[1]
#     text_x = int((width - width_text) / 2) + x
#     text_y = int((height + height_text) / 2) + y
    
#     if image_select is True:
#         cv2.rectangle(Main_Options, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
#         cv2.putText(Main_Options, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
#     else:
#         cv2.rectangle(Main_Options, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
#         cv2.putText(Main_Options, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)
    
    
# icon_index = 0
# frames = 0
# selected = 0

# while True:
#     cv2.imshow("Elocutor Home", Main_Options)
    
#     for i in range(3):
#         if i == icon_index:
#             light = True
#         else:
#             light = False
#         draw_icon(i, light)
    
#     frames = (frames + 1) % 50
#     if frames == 49:
#         icon_index = (icon_index + 1) % 3
    
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
# cv2.destroyAllWindows()

from tkinter import * 
from tkinter.ttk import *
import os
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk()

root.title("Elocutor Home")
root.iconbitmap("images/accessibility.png")
root.geometry("600x400")
uniform_color="#3b6dc7"



"""class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        
        load = Image.open("images/elocutor.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=115, y=0)


l1=Window(root)
#l1.configure(background='#23b4c4')
l1.pack()"""

root.configure(background=uniform_color)

"""l1 = Label(root, text = " Elocutor ",background='darkblue',foreground="white")
l1.config(font=("Arial Rounded MT Bold", 40))
l1.pack()"""
photo5 = PhotoImage(file = r"images/elocuter2.png")
photoimage5 = photo5.subsample(1, 1)
l5=Label(root,image = photoimage5,background=uniform_color)
l5.pack()
l2 = Label(root, text = "Select Detection Method",background=uniform_color,foreground="white")
l2.config(font=('Arial Rounded MT Bold', 20))
l2.pack()
l3 = Label(root, text = "--------------------------------------------------------------------------------------------------------------------------------------------------\n",background=uniform_color,foreground="white")
l3.pack()
#ttk.Style().configure('green/black.TButton', foreground='black', background='blue')
#,style='green/black.TButton'
style = Style() 
style.configure('TButton', font = ('Arial', 15, 'bold'), borderwidth = '16', foreground ="black", background = uniform_color) 
  
# Changes will be reflected 
# by the movement of mouse. 






def button1_click():
    os.system('../Keyboard/cheek_test_ver_03.py')
    root.destroy


photo = PhotoImage(file = r"images/cheek.png") 
photoimage = photo.subsample(3, 3)
l4=Label(root,image = photoimage,background=uniform_color).place(x=30, y=250)
b1 = Button(root, text = 'Cheek', command = button1_click,style="TButton").place(x=10, y=340)

photo1 = PhotoImage(file = r"images/eye3.png") 
photoimage1 = photo1.subsample(3, 3)
l5=Label(root,image = photoimage1,background=uniform_color).place(x=180, y=250)
b2 = Button(root, text = 'Eye').place(x=160, y=340)

photo2 = PhotoImage(file = r"images/eyebrows3.png") 
photoimage2 = photo2.subsample(3, 3)
l6=Label(root,image = photoimage2,background=uniform_color).place(x=330, y=250)
b3 = Button(root, text = 'Eyebrows').place(x=310, y=340)

photo3 = PhotoImage(file = r"images/exit3.png") 
photoimage3 = photo3.subsample(3, 3)
l7=Label(root,image = photoimage3,background=uniform_color).place(x=480, y=250)
b4 = Button(root, text = 'Exit',command=root.destroy).place(x=460, y=340)

"""l4.pack(side=LEFT,padx=10,fill=X)
l5.pack(side=LEFT,padx=15)
l6.pack(side=LEFT,padx=15)
l7.pack(side=LEFT,padx=10)


l0=Label(root,text="\n")

l0.pack(side=LEFT)

#b4.pack(side=LEFT,padx=2)

b3.pack(side=LEFT,padx=1)


b1.pack(side=LEFT,padx=2)

b2.pack(side=LEFT,padx=1)"""


root.mainloop()
