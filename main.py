import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
from PIL import Image, ImageTk
import time

from os.path import exists

ProjectNames = set()
ProjectButtons = []
workingProject = ""

BIG_BUTTTON_HEIGHT = 10
MID_BUTTON_HEIGHT = 5
SMALL_BUTTTON_HEIGHT = 3


startTime = 0
endTime = 0
tracking = False

dragging = False

def drag(event):
    global dragging
    print("drag")
    x = m.winfo_pointerx() - m.offsetx
    y = m.winfo_pointery() - m.offsety
    m.geometry('+{x}+{y}'.format(x=x,y=y))
    dragging = True

def click(event):
    global dragging
    print("click")
    m.offsetx = event.x
    m.offsety = event.y
    dragging = False

def release(f = 0):
    global dragging
    if dragging:
        dragging = False
    elif f != 0:
        f()

def addNewProjectButton(name):
    new_button = tk.Button(m, text=name, height = MID_BUTTON_HEIGHT, width=15, font=tkFont.Font(size=20), command= lambda: startWorking(new_button))
    new_button.pack()
    ProjectButtons.append(new_button)

def timeFormatter(s):
    hours = 0
    minutes = 0
    seconds = 0
    res = ""
    if s > 3600:
        hours = s//3600
        s = s % 3600
        res += str(hours) + " h " 
    if s > 60:
        minutes = s//60
        s = s % 60
        res += str(minutes) + " m " 
    seconds = int(s)
    return res + str(seconds) + " s "

def addNewItem():
    l = tk.Label(m, text="Item Name ")
    entry = tk.Entry(m)
    b = tk.Button(m, text='Confirm New Item', height = SMALL_BUTTTON_HEIGHT, width=15, command=lambda: confirmNewItem(entry, [l, entry, b]))
    entry.bind("<Return>", lambda event: confirmNewItem(entry, [l, entry, b]))
    l.pack()
    entry.pack()
    b.pack()

def confirmNewItem(entry, destroyList: list):
    newItemName = entry.get()
    if newItemName != "" and newItemName not in ProjectNames:
        ProjectNames.add(newItemName)
        addNewProjectButton(newItemName)
        ##To save in file
        with open('OTT_projects.txt','a') as f:
            f.write(newItemName+"\n")

    for item in destroyList:
        item.destroy()

def updateWorkingTime():
    global startTime
    global tracking
    print("update time")
    CountingLabel.configure(text=timeFormatter(time.time()-startTime))
    if tracking:
        CountingLabel.after(1000, updateWorkingTime)


def startWorking(button):
    global startTime
    global tracking
    workingProject = button['text']
    print("start working on: ", workingProject)
    startTime = time.time()
    tracking = True
    print("start time: ", startTime)
    NewItemButton.pack_forget()
    for button in ProjectButtons:
        button.pack_forget()
    StopButton.pack()
    CountingLabel.pack()
    CountingLabel.after(1000, updateWorkingTime)
    m.attributes("-alpha", 0.5)

def stopWorking():
    global startTime
    global tracking
    print("stop working ", workingProject)
    endTime = time.time()
    tracking = False
    print("start time: ", startTime)
    print("end time: ", endTime, ", working time: ", endTime-startTime)
    StopButton.pack_forget()
    CountingLabel.pack_forget()
    for button in ProjectButtons:
        button.pack()
    NewItemButton.pack(side=tk.BOTTOM)
    m.attributes("-alpha", 1)


m = tk.Tk()
m.title('Time Tracker')

if exists('OTT_projects.txt'):
    with open('OTT_projects.txt','r') as f:
        lines = [i.strip() for i in f.readlines()]
        ProjectNames = set(lines)
        for name in ProjectNames:
            addNewProjectButton(name)
    print("projects: ", ProjectNames)

NewItemButton = tk.Button(m, text='Add New Item', height = SMALL_BUTTTON_HEIGHT, width=15, fg='black', bg='grey', font=tkFont.Font(size=20))
NewItemButton.bind("<ButtonRelease>", lambda event: release(addNewItem))
NewItemButton.pack(side=tk.BOTTOM)

photo = PhotoImage(file='stop.png')
photo = photo.subsample(8,8)

StopButton = tk.Button(m, image = photo)
StopButton.bind("<ButtonRelease>", lambda event: release(stopWorking))
CountingLabel = tk.Label(m, text="")

m.bind('<Button-1>', click)
m.bind('<B1-Motion>', drag)
m.overrideredirect(True)
m.wm_attributes("-topmost", 1)

m.mainloop()


