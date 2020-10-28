## Detection Method Selection Menu

from tkinter import * 
from tkinter.ttk import *
from Main_Menu_Cheek import Menu_Cheek

root = Tk()
root.title("Elocutor Home")
root.iconbitmap("images/accessibility.png")
root.geometry("800x400")
l1 = Label(root, text = "\nWelcome!")
l1.config(font=("Courier", 44))
l1.pack()
l2 = Label(root, text = "\nSelect detection Method\n")
l2.config(font=('TimesNewRoman', 30))
l2.pack()

def button1_click():
    root.destroy()
    Menu_Cheek()
    
def button2_click():
    os.system('../Keyboard/cheek_test_ver_03.py')
    root.destroy

def button3_click():
    os.system('../Keyboard/cheek_test_ver_03.py')
    root.destroy

photo = PhotoImage(file = r"images/cheek.png") 
photoimage = photo.subsample(3, 3)
b1 = Button(root, text = 'Cheek detection', image = photoimage, compound = LEFT, command = button1_click)

photo1 = PhotoImage(file = r"images/eye.png") 
photoimage1 = photo1.subsample(3, 3)
b2 = Button(root, text = 'Eye detection', image = photoimage1, compound = LEFT)

photo2 = PhotoImage(file = r"images/eyebrows.png") 
photoimage2 = photo2.subsample(3, 3)
b3 = Button(root, text = 'Eyebrows detection', image = photoimage2, compound = LEFT)

photo3 = PhotoImage(file = r"images/exit.png") 
photoimage3 = photo3.subsample(3, 3)
b4 = Button(root, text = 'Exit', image = photoimage3, compound = LEFT, command=root.destroy)

b1.pack(side=LEFT,padx=20)
b2.pack(side=LEFT,padx=20)
b3.pack(side=LEFT,padx=20)
b4.pack(side=LEFT,padx=20)

root.mainloop()