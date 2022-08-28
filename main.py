import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
from PIL import Image, ImageTk
import time
from datetime import datetime

from os.path import exists
import csv

ProjectNames = set()
ProjectButtons = []
TrackRecord = {}
workingProject = ""

BIG_BUTTTON_HEIGHT = 10
MID_BUTTON_HEIGHT = 5
SMALL_BUTTTON_HEIGHT = 3


startTime = 0
tracking = False


dragging = False

def drag(event):
    global dragging
    x = m.winfo_pointerx() - m.offsetx
    y = m.winfo_pointery() - m.offsety
    m.geometry('+{x}+{y}'.format(x=x,y=y))
    dragging = True

def click(event):
    global dragging
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
        with open('OTT_projects.txt','a') as f:
            f.write(newItemName+"\n")

    for item in destroyList:
        item.destroy()

def updateWorkingTime():
    global startTime
    global tracking
    t = datetime.now()-startTime
    CountingLabel.configure(text="{:02}:{:02}:{:02}".format(t.seconds//3600, t.seconds%3600//60, t.seconds%60))
    if tracking:
        CountingLabel.after(1000, updateWorkingTime)


def startWorking(button):
    global startTime
    global tracking
    global workingProject
    workingProject = button['text']
    startTime= datetime.now()
    tracking = True
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
    global workingProject
    endTime = datetime.now() 
    tracking = False

    if workingProject in TrackRecord:
        TrackRecord[workingProject].append((str(startTime), str(endTime), (endTime-startTime).seconds))
    else:
        TrackRecord[workingProject] = [(str(startTime), str(endTime), (endTime-startTime).seconds)]
    # print(TrackRecord)

    log_file = '{}-{}.log'.format(startTime.year, startTime.month)
    with open(log_file, 'a') as f:
        f.write(workingProject + ", "+ str(startTime) + ", " + str(endTime) + ", " + str((endTime-startTime).seconds)+"\n")


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


log_file = '{}-{}.log'.format(datetime.now().year, datetime.now().month)
if exists(log_file):
    with open(log_file, 'r') as f:
        r = csv.reader(f, delimiter=',')
        for row in r:
            if row[0] in TrackRecord:
                TrackRecord[row[0]].append((row[1], row[2], int(row[3])))
            else:
                TrackRecord[row[0]] = [(row[1], row[2], int(row[3]))]

# print(TrackRecord)


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


