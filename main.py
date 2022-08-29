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
ProjectLabels = []
TrackRecord = {}
workingProject = ""

BIG_BUTTTON_HEIGHT = 10
MID_BUTTON_HEIGHT = 3
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
    m.offsetx = m.winfo_pointerx() - m.winfo_rootx()
    m.offsety = m.winfo_pointery() - m.winfo_rooty()
    dragging = False

def release(f = 0):
    global dragging
    if dragging:
        dragging = False
    elif f != 0:
        f()

def getTodayTotal(name):
    if name in TrackRecord:
        return sum([i[2] for i in TrackRecord[name]])
    else:
        return 0


def addNewProjectButton(name):
    total = getTodayTotal(name)
    new_button = tk.Button(CentralArea, text=name, height = MID_BUTTON_HEIGHT, width=12, font=tkFont.Font(size=20), command= lambda: startWorking(new_button))
    new_button.grid(row = len(ProjectButtons)*2)
    l = tk.Label(CentralArea, text="Today Total: {:02}:{:02}:{:02}".format(total//3600, total%3600//60, total%60))
    l.grid(row = len(ProjectButtons)*2 + 1)
    ProjectButtons.append(new_button)
    ProjectLabels.append((name, l))


def addNewItem():
    l = tk.Label(CentralArea, text="Item Name ")
    entry = tk.Entry(CentralArea)
    b = tk.Button(CentralArea, text='Confirm New Item', height = SMALL_BUTTTON_HEIGHT, width=12, command=lambda: confirmNewItem(entry, [l, entry, b]))
    entry.bind("<Return>", lambda event: confirmNewItem(entry, [l, entry, b]))
    l.grid(row = len(ProjectButtons)*2)
    entry.grid(row = len(ProjectButtons)*2 + 1)
    b.grid(row = len(ProjectButtons)*2 + 2)

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
    CountingLabel.configure(text=workingProject+"\n{:02}:{:02}:{:02}".format(t.seconds//3600, t.seconds%3600//60, t.seconds%60))
    if tracking:
        CountingLabel.after(1000, updateWorkingTime)


def startWorking(button):
    global startTime
    global tracking
    global workingProject
    workingProject = button['text']
    startTime= datetime.now()
    tracking = True
    NewItemButton.grid_remove()
    ExitButton.grid_remove()
    BottomBar.pack_forget()
    for button in ProjectButtons:
        button.grid_remove()
    for label in ProjectLabels:
        label[1].grid_remove()
    StopButton.grid(row = 0)
    CountingLabel.grid(row = 1)
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


    StopButton.grid_remove()
    CountingLabel.grid_remove()
    for index in range(len(ProjectButtons)):
        ProjectButtons[index].grid()
        ProjectLabels[index][1].grid()
    for p in ProjectLabels:
        if p[0] == workingProject:
            total = getTodayTotal(p[0])
            p[1].configure(text = "Today Total: {:02}:{:02}:{:02}".format(total//3600, total%3600//60, total%60))

    BottomBar.pack()
    NewItemButton.grid()
    ExitButton.grid()
    m.attributes("-alpha", 1)


m = tk.Tk()
m.title('Time Tracker')
CentralArea = Frame()
CentralArea.pack(side = TOP)
BottomBar = Frame()
BottomBar.pack(side = BOTTOM)

log_file = '{}-{}.log'.format(datetime.now().year, datetime.now().month)
if exists(log_file):
    with open(log_file, 'r') as f:
        r = csv.reader(f, delimiter=',')
        for row in r:
            if row[0] in TrackRecord:
                TrackRecord[row[0]].append((row[1], row[2], int(row[3])))
            else:
                TrackRecord[row[0]] = [(row[1], row[2], int(row[3]))]

print(TrackRecord)

if exists('OTT_projects.txt'):
    with open('OTT_projects.txt','r') as f:
        lines = [i.strip() for i in f.readlines()]
        ProjectNames = set(lines)
        for name in ProjectNames:
            addNewProjectButton(name)
    print("projects: ", ProjectNames)




NewItemButton = tk.Button(BottomBar, text='New', height = SMALL_BUTTTON_HEIGHT, width=5, fg='black', bg='lightblue', font=tkFont.Font(size=20))
NewItemButton.grid(column=0, row = 0)
NewItemButton.bind("<ButtonRelease>", lambda event: release(addNewItem))
ExitButton = tk.Button(BottomBar, text='Exit', height = SMALL_BUTTTON_HEIGHT, width=5, fg='red', bg='black', font=tkFont.Font(size=20))
ExitButton.grid(column=1, row = 0)
ExitButton.bind("<ButtonRelease>", lambda event: release(lambda: exit()))

photo = PhotoImage(file='stop.png')
photo = photo.subsample(8,8)

StopButton = tk.Button(CentralArea, image = photo)
StopButton.bind("<ButtonRelease>", lambda event: release(stopWorking))
CountingLabel = tk.Label(CentralArea, text="")

m.bind('<Button-1>', click)
m.bind('<B1-Motion>', drag)

# m.bind('<FocusIn>', lambda _: m.attributes("-alpha", 1))
# m.bind('<FocusOut>', lambda _: m.attributes("-alpha", 0.5))

m.overrideredirect(True)
m.wm_attributes("-topmost", 1)

m.mainloop()
