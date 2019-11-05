from tkinter import *
import tkinter.filedialog
root = Tk()

def browsefunc():
    filename = tkinter.filedialog.askopenfilename()
    pathlabel.config(text=filename)

browsebutton = Button(root, text="Browse", command=browsefunc)
browsebutton.pack()

pathlabel = Label(root)
pathlabel.pack()

root.mainloop()