import tkinter as tk
from tkinter import font as tkFont
import platform
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

def addNewProjectButton(name):
    new_button = tk.Button(m, text=name, height = MID_BUTTON_HEIGHT, width=15, font=tkFont.Font(size=20), command= lambda: startWorking(new_button))
    new_button.pack()
    ProjectButtons.append(new_button)

def addNewItem(m):
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
    StopButton.configure(text=str(int(time.time()-startTime))+" s\n Stop")
    if tracking:
        StopButton.after(1000, updateWorkingTime)


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
    StopButton.after(1000, updateWorkingTime)

def stopWorking():
    global startTime
    global tracking
    print("stop working ", workingProject)
    endTime = time.time()
    tracking = False
    print("start time: ", startTime)
    print("end time: ", endTime, ", working time: ", endTime-startTime)
    StopButton.pack_forget()
    for button in ProjectButtons:
        button.pack()
    NewItemButton.pack(side=tk.BOTTOM)


m = tk.Tk()
m.title('Time Tracker')

if exists('projects.txt'):
    with open('OTT_projects.txt','r') as f:
        lines = [i.strip() for i in f.readlines()]
        ProjectNames = set(lines)
        for name in ProjectNames:
            addNewProjectButton(name)
    print("projects: ", ProjectNames)

NewItemButton = tk.Button(m, text='Add New Item', height = SMALL_BUTTTON_HEIGHT, width=15, fg='black', bg='grey', font=tkFont.Font(size=20), command=lambda: addNewItem(m))
NewItemButton.pack(side=tk.BOTTOM)
StopButton = tk.Button(m, text='stop', height = MID_BUTTON_HEIGHT, width=10, fg='red', font=tkFont.Font(size=30), command=lambda: stopWorking())
m.wm_attributes("-topmost", 1)
m.mainloop()


