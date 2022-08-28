import tkinter as tk
from tkinter import font as tkFont
import platform
import time

ProjectNames = set()
ProjectButtons = []
workingProject = ""

startTime = 0
endTime = 0

def addNewItem(m):
    l = tk.Label(m, text="Item Name ")
    entry = tk.Entry(m)
    b = tk.Button(m, text='Confirm New Item', height = 5, width=15, command=lambda: confirmNewItem(entry, [l, entry, b]))
    entry.bind("<Return>", lambda event: confirmNewItem(entry, [l, entry, b]))
    l.pack()
    entry.pack()
    b.pack()

def confirmNewItem(entry, destroyList: list):
    newItemName = entry.get()
    if newItemName != "":
        ProjectNames.add(newItemName)
        new_button = tk.Button(m, text=newItemName, height = 5, width=15, command= lambda: startWorking(new_button))
        new_button.pack()
        ProjectButtons.append(new_button)

    for item in destroyList:
        item.destroy()

def updateWorkingTime():
    global startTime
    StopButton.configure(text=str(int(time.time()-startTime))+" s\n Stop")
    StopButton.after(1000, updateWorkingTime)


def startWorking(button):
    global startTime
    workingProject = button['text']
    print("start working on: ", workingProject)
    startTime = time.time()
    print("start time: ", startTime)
    NewItemButton.pack_forget()
    for button in ProjectButtons:
        button.pack_forget()
    StopButton.pack()
    StopButton.after(1000, updateWorkingTime)

def stopWorking():
    global startTime
    print("stop working ", workingProject)
    endTime = time.time()
    print("start time: ", startTime)
    print("end time: ", endTime, ", working time: ", endTime-startTime)
    StopButton.pack_forget()
    for button in ProjectButtons:
        button.pack()
    NewItemButton.pack(side=tk.BOTTOM)


m = tk.Tk()
m.title('Time Tracker')

NewItemButton = tk.Button(m, text='Add New Item', height = 10, width=15, fg='black', bg='grey', font=tkFont.Font(size=20), command=lambda: addNewItem(m))
NewItemButton.pack(side=tk.BOTTOM)
StopButton = tk.Button(m, text='stop', height = 6, width=10, fg='red', font=tkFont.Font(size=30), command=lambda: stopWorking())
m.wm_attributes("-topmost", 1)
m.mainloop()


