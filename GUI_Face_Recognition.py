from PIL import ImageTk, Image
from tkinter import *
import tkinter.messagebox
import tkinter.font
import tkinter.filedialog
from FeaturesExtractor import *

# Inisialisasi Variabel global awal
matchtemp = float(0)
matchrate = float(0)
filename = ''
i = 0
y = 1

def MatchUp():
    global filename
    global var
    global NumPhoto
    global matchtemp
    global y

    dataUji = filename

    # Path folder data referensi
    images_path = 'test/Data Referensi/'

    # Jika belum ada file .pck untuk data referensi, akan diextract terlebih dahulu
    extracted = os.path.isfile('./features_referensi.pck')
    if not(extracted):
        batch_extractor_referensi(images_path)

    ma = Matcher('features_referensi.pck')
    
    op = var.get()
    names, match = ma.match(dataUji, y, op)
    match_rate = float(0);
    sum = float(0);
    i = 0;
    for i in range(y):
        sum = sum + match[i]
        match_rate = sum / (i+1)
        changeDataRef(os.path.join(images_path, names[i]))
    EFinished.delete(0,'end')
    EQueue.delete(0,'end')
    EHasilAkhir.delete(0,'end')
    EMatchRate.delete(0,'end')
    EMatching.delete(0,'end')
    EFinished.insert(0,y)
    EQueue.insert(0,NumPhoto.get()-y)
    EMatching.insert(0,match[i])
    EMatchRate.insert(0,match_rate)
    EHasilAkhir.insert(0,'Mirip')

def NextImage():

    global y
    if (y < NumPhoto.get()) :
        y = y+1
        MatchUp()

def start():
    global y
    y = 1
    MatchUp()

# GANTI FOTO DALAM GUI
def changeDataUji(filename):
    global photo
    photo = ImageTk.PhotoImage(file=filename)
    LImage1 = Label(root, image=photo)
    LImage1.place(x=150, y=110, in_=root)

def changeDataRef(namafile):
    global photo1
    photo1 = ImageTk.PhotoImage(file=namafile)
    LImage2 = Label(root, image=photo1)
    LImage2.place(x=600, y=110, in_=root)

def helloCallBack():
    tkinter.messagebox.showinfo( "Hello Python", "Hello World")

def resetSetting():
    global y
    EFinished.delete(0,'end')
    EQueue.delete(0,'end')
    EHasilAkhir.delete(0,'end')
    EMatchRate.delete(0,'end')
    EMatching.delete(0,'end')
    scaleNumPhoto.set(1)
    y = 1
    pathlabel.config(text='')
    changeDataRef('EmptyPhoto.jpg')
    changeDataUji('EmptyPhoto.jpg')
    

def sel():
    selection = "Kamu memilih opsi perhitungan ke-" + str(var.get())
    label.config(text = selection)

def browsefunc():
    global filename
    filename = tkinter.filedialog.askopenfilename()
    changeDataUji(filename)
    imgName = filename.split("/")
    pathlabel.config(text=imgName[-1])

def callback():
    if tkinter.messagebox.askyesno('Verify', 'Do you want to really quit?'):
        quit()
    else:
        tkinter.messagebox.showinfo('No', 'Quit has been cancelled')

root = tkinter.Tk()
root.geometry('1024x768')
root.title("IF2123 - Aljabar Linear dan Geometri - Face Recognition")
#root.iconbitmap("C:/Users/micha/Documents/GitHub/algeosantuy/itb.ico")

# INISIALISASI FOTO AWAL
photo = ImageTk.PhotoImage(file="EmptyPhoto.jpg")
photo1 = ImageTk.PhotoImage(file="EmptyPhoto.jpg")


# Image Position in GUI
LImage1 = Label(root, image=photo)
LImage1.place(x=150, y=110, in_=root)

LImage2 = Label(root, image=photo1)
LImage2.place(x=600, y=110, in_=root)

# All Text and Labels In GUI
helv36 = tkinter.font.Font(family='Helvetica', size=36, weight='bold')
helv10 = tkinter.font.Font(family='Helvetica', size=10)
helv12 = tkinter.font.Font(family='Helvetica', size=12)
helv14 = tkinter.font.Font(family='Helvetica', size=14)
L2 = Label(root, text="Face Recognition")
L2['font'] = helv36
L2.place(x=10, y=30, in_=root)

L3 = Label(root, text="IF2123 - Aljabar Linear dan Geometri")
L4 = Label(root, text="Created by : Gatau Nanti")
L5 = Label(root, text="13518056 - Michael Hans")
L6 = Label(root, text="13518088 - Ananda Yulizar Muhammad")
L7 = Label(root, text="13518112 - Muhammad Fauzan Al-Ghifari")
L3['font'] = helv10
L4['font'] = helv10
L5['font'] = helv10
L6['font'] = helv10
L7['font'] = helv10
L3.place(x=750, y=0, in_=root)
L4.place(x=750, y=20, in_=root)
L5.place(x=750, y=40, in_=root)
L6.place(x=750, y=60, in_=root)
L7.place(x=750, y=80, in_=root)

# Radio Button Metode Euclidian/Cosine
LRadio = Label(root, text="Metode Perhitungan")
LRadio['font'] = helv14
LRadio.place(x=130, y=430, in_=root)

var = IntVar()
R1 = Radiobutton(root, text="1. Jarak Euclidiean", variable=var, value=1,command=sel)
R1['font'] = helv12
R1.place(x=130, y=460, in_=root)

R2 = Radiobutton(root, text="2. Cosinus Similarity", variable=var, value=2,command=sel)
R2['font'] = helv12
R2.place(x=130, y=490, in_=root)

label = Label(root)
label['font'] = helv12
label.place(x=130, y=520, in_=root)

LName = Label(root, text="Nama Orang")
LName['font'] = helv14
LName.place(x=430, y=430, in_=root)

# EName = Entry(root, bd =2, width = 18)
# EName['font'] = helv12
# EName.place(x=430, y=460, in_=root)

browsebutton = Button(root, text="Browse", command=browsefunc)
browsebutton['font'] = helv14
browsebutton.place(x=430, y=460, in_=root)

pathlabel = Label(root)
pathlabel['font'] = helv14
pathlabel.place(x=430, y=490, in_=root)

LNumPhoto = Label(root, text="Jumlah foto")
LNumPhoto['font'] = helv14
LNumPhoto.place(x=430, y=520, in_=root)

NumPhoto = IntVar() 
scaleNumPhoto = Scale( root, variable = NumPhoto, orient=HORIZONTAL, from_=1, to_=10, length = 200)
scaleNumPhoto['font'] = helv12
scaleNumPhoto.place(x=430, y=550, in_=root)

# GUI Hasil Recognition
LResult = Label(root, text="Hasil Face Recognition")
LResult['font'] = helv14
LResult.place(x=700, y=430, in_=root)

Finished = Label(root, text="Finished")
Finished['font'] = helv12
Finished.place(x=700, y=460, in_=root)

EFinished = Entry(root, bd =2, width = 14)
EFinished['font'] = helv12
EFinished.place(x=800, y=460, in_=root)

Queue = Label(root, text="Queue")
Queue['font'] = helv12
Queue.place(x=700, y=490, in_=root)

EQueue = Entry(root, bd =2, width = 14)
EQueue['font'] = helv12
EQueue.place(x=800, y=490, in_=root)

Matching = Label(root, text="Match")
Matching['font'] = helv12
Matching.place(x=700, y=520, in_=root)

EMatching = Entry(root, bd =2, width = 14)
EMatching['font'] = helv12
EMatching.place(x=800, y=520, in_=root)

MatchRate = Label(root, text="Match Rate")
MatchRate['font'] = helv12
MatchRate.place(x=700, y=550, in_=root)

EMatchRate = Entry(root, bd =2, width = 14)
EMatchRate['font'] = helv12
EMatchRate.place(x=800, y=550, in_=root)

HasilAkhir = Label(root, text="Result")
HasilAkhir['font'] = helv12
HasilAkhir.place(x=700, y=580, in_=root)

EHasilAkhir = Entry(root, bd =2, width = 14)
EHasilAkhir['font'] = helv12
EHasilAkhir.place(x=800, y=580, in_=root)

MatchButton = tkinter.Button(root, height = 2, width = 10, bg='green yellow', text ="Match Up!", command = start)
MatchButton['font'] = helv12
MatchButton.place(x=480, y=250, in_=root)

ResetButton = tkinter.Button(root, height = 2, width = 10, bg='orange', text ="Reset", command = resetSetting)
ResetButton['font'] = helv12
ResetButton.place(x=480, y=180, in_=root)

QuitButton = tkinter.Button(root, height = 2, width = 10, bg='red', text ="Quit", command = callback)
QuitButton['font'] = helv12
QuitButton.place(x=480, y=320, in_=root)

NextButton = tkinter.Button(root, height = 2, width = 10, bg='blue', text ="Next", command = NextImage)
NextButton['font'] = helv12
NextButton.place(x=480, y=110, in_=root)

# Button(text='Quit', command=callback).pack(fill=X)
# Button(text='Answer', command=answer).pack(fill=X)

root.resizable(0,0)
root.mainloop()