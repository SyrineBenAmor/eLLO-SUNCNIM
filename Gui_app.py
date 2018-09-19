import tkinter as tk
from tkinter import *
import tkinter.font
import main

import sys

sys.path.append('gather_photos/')
import gatherData

win = tk.Tk()
myFont = tkinter.font.Font(family = 'Helvatica',size = 18, weight='bold')
sentence1 = StringVar()
sentence2 = StringVar()
sentence3 = StringVar()
sentence4 = StringVar()

def runMain():
    main.main()
    
def exitProgram():
    
    print("exit button pressed")
    win.quit()
def GatherData():
    
    gatherData.main(15,54,16,54)

win.title("DETECTOR")
win.geometry('800x480')

exitButton = Button(win, text = "Exit", font = myFont, command = exitProgram, bg ='gray',height= 2, width = 6)
exitButton.pack(side = BOTTOM)
DataButton = Button(win,text="Gather data", font= myFont , command=GatherData,bg = 'blue' ,height = 2, width=10)
DataButton.pack()
MainButton = Button(win,text="Pin crack in map", font= myFont , command=runMain,bg = 'red' ,height = 3, width=16)
MainButton.pack()
StartHourEntry = Entry(win,textvariable= sentence1).pack()
StartMinuteEntry = Entry(win,textvariable= sentence2).pack()
FinishHourEntry = Entry(win,textvariable= sentence3).pack()
FinishMinuteEntry = Entry(win,textvariable= sentence4).pack()
StartHourLabel = Label(win,text = "1-Start Hour cleaning").pack()
StartMinuteLabel = Label(win,text = "2-Start Minute cleaning").pack()
FinishHourLabel = Label(win,text = "3-Finish Hour cleaning").pack()
FinishMinuteLabel = Label(win,text = "4-Finish Minute cleaning").pack()

mainloop()
