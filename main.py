import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
from datetime import datetime
from os.path import exists
import csv


class DataControl():
    def __init__(self):
        self.projectNames = set()
        self.archivedProjectNames = set()
        self.trackRecord = {}
        self.workingProject = ""

        if exists('OTT_projects.txt'):
            with open('OTT_projects.txt','r') as f:
                lines = [i.strip() for i in f.readlines()]
                for l in lines:
                    if l[:2] == "--":
                        self.archivedProjectNames.add(l[2:])
                    else:
                        self.projectNames.add(l)
            print("projects: ", self.projectNames)
            print("archived projects: ", self.archivedProjectNames)


        log_file = '{}-{}.log'.format(datetime.now().year, datetime.now().month)
        if exists(log_file):
            with open(log_file, 'r') as f:
                r = csv.reader(f, delimiter=',')
                for row in r:
                    if row[0] in self.trackRecord:
                        self.trackRecord[row[0]].append((row[1], row[2], int(row[3])))
                    else:
                        self.trackRecord[row[0]] = [(row[1], row[2], int(row[3]))]
        print(self.trackRecord)

    def getTodayTotal(self, name):
        if name in self.trackRecord:
            return sum([i[2] for i in self.trackRecord[name]])
        else:
            return 0

    def hasProject(self, name):
        return name in self.projectNames

    def tryAddProject(self, name):
        if name in self.projectNames:
            return False
        else:
            self.projectNames.add(name)
            with open('OTT_projects.txt','a') as f:
                f.write(name+"\n")
            return True

    def startWorking(self, name):
        self.workingProject = name

    def stopWorking(self, startTime, endTime):
        if self.workingProject in self.trackRecord:
            self.trackRecord[self.workingProject].append((str(startTime), str(endTime), (endTime-startTime).seconds))
        else:
            self.trackRecord[self.workingProject] = [(str(startTime), str(endTime), (endTime-startTime).seconds)]
        log_file = '{}-{}.log'.format(startTime.year, startTime.month)
        with open(log_file, 'a') as f:
            f.write(self.workingProject + ", "+ str(startTime) + ", " + str(endTime) + ", " + str((endTime-startTime).seconds)+"\n")

    def archiveProject(self, name):
        pass




class MainWindow():
    def __init__(self):
        # ******** window **********
        self.m = tk.Tk()
        self.m.title('Time Tracker')
        self.m.bind('<Button-1>', self.click)
        self.m.bind('<B1-Motion>', self.drag)

        # ******** data **********
        self.data = DataControl()
        self.projectButtons = []
        self.projectLabels = []

        # ******** Frames **********
        self.projectArea = Frame()
        self.projectArea.pack(side = TOP)
        self.controlArea = Frame()
        self.controlArea.pack(side = BOTTOM)
        # self.settingArea = Frame()
        # self.settingArea.pack(side = TOP)
        # self.settingArea.pack_forget()

        # ******** buttons **********
        for name in self.data.projectNames:
            self.addNewProjectButton(name)

        self.newItemButton = tk.Button(self.controlArea, text='New')
        self.newItemButton.grid(column=0, row = 0)
        self.newItemButton.bind("<ButtonRelease>", lambda event: self.release(self.addNewItem))

        self.exitButton = tk.Button(self.controlArea, text='Exit')
        self.exitButton.grid(column=1, row = 0)
        self.exitButton.bind("<ButtonRelease>", lambda event: self.release(exit))

        self.settingButton = tk.Button(self.controlArea, text='Setting')
        self.settingButton.grid(column=0, row = 1)
        self.settingButton.bind("<ButtonRelease>", lambda event: self.release(self.openSetting))

        self.returnSettingButton = tk.Button(self.controlArea, text='Return')
        self.returnSettingButton.bind("<ButtonRelease>", lambda event: self.release(self.closeSetting))

        self.archiveButton = tk.Button(self.controlArea, text='Archive')
        self.archiveButton.grid(column=1, row = 1)
        self.archiveButton.bind("<ButtonRelease>", lambda event: self.release(self.archiveProject))

        self.photo = PhotoImage(file='stop.png').subsample(8,8)
        self.stopButton = tk.Button(self.controlArea, image = self.photo)
        self.stopButton.bind("<ButtonRelease>", lambda event: self.release(self.stopWorking))
        self.countingLabel = tk.Label(self.controlArea, text="")

        # ******** variables **********
        self.dragging = False
        self.startTime = 0
        self.tracking = False


    # ******** window behavior **********
    def drag(self, event):
        x = self.m.winfo_pointerx() - self.m.offsetx
        y = self.m.winfo_pointery() - self.m.offsety
        self.m.geometry('+{x}+{y}'.format(x=x,y=y))
        self.dragging = True

    def click(self, event):
        self.m.offsetx = self.m.winfo_pointerx() - self.m.winfo_rootx()
        self.m.offsety = self.m.winfo_pointery() - self.m.winfo_rooty()
        self.dragging = False

    def release(self, f = 0):
        if self.dragging:
            self.dragging = False
        elif f != 0:
            f()

    def openSetting(self):
        self.newItemButton.grid_remove()
        self.exitButton.grid_remove()
        for button in self.projectButtons:
            button.grid_remove()
        for label in self.projectLabels:
            label[1].grid_remove()
        self.projectArea.pack_forget()
        self.returnSettingButton.grid(column=0, row = 1)
        # self.controlArea.pack_forget()

    def closeSetting(self):
        self.projectArea.pack()
        self.newItemButton.grid()
        self.exitButton.grid()
        for button in self.projectButtons:
            button.grid()
        for label in self.projectLabels:
            label[1].grid()
        self.returnSettingButton.grid_remove()

    def archiveProject(self):
        pass



    # ******** add new project **********
    def addNewItem(self):
        l = tk.Label(self.controlArea, text="Item Name ")
        entry = tk.Entry(self.controlArea)
        entry.bind("<Return>", lambda event: self.confirmNewItem(entry, [l, entry, b]))
        b = tk.Button(self.controlArea, text='Confirm New Item', command=lambda: self.confirmNewItem(entry, [l, entry, b]))
        l.grid(row = len(self.projectButtons)*2)
        entry.grid(row = len(self.projectButtons)*2 + 1)
        b.grid(row = len(self.projectButtons)*2 + 2)

    def confirmNewItem(self, entry, destroyList: list):
        newItemName = entry.get()
        if newItemName != "":
            if self.data.tryAddProject(newItemName):
                self.addNewProjectButton(newItemName)

        for item in destroyList:
            item.destroy()

    def addNewProjectButton(self, name):
        total = self.data.getTodayTotal(name)
        new_button = tk.Button(self.projectArea, text=name, command= lambda: self.startWorking(new_button))
        new_button.grid(row = len(self.projectButtons)*2)
        l = tk.Label(self.projectArea, text="Today Total: {:02}:{:02}:{:02}".format(total//3600, total%3600//60, total%60))
        l.grid(row = len(self.projectButtons)*2 + 1)
        self.projectButtons.append(new_button)
        self.projectLabels.append((name, l))

    # ******** begin and stop **********
    def startWorking(self, button):
        self.data.startWorking(button['text'])
        self.startTime= datetime.now()
        self.tracking = True

        self.projectArea.pack_forget()
        self.newItemButton.grid_remove()
        self.exitButton.grid_remove()
        self.settingButton.grid_remove()
        self.archiveButton.grid_remove()
        # self.controlArea.pack_forget()
        for button in self.projectButtons:
            button.grid_remove()
        for label in self.projectLabels:
            label[1].grid_remove()

        self.stopButton.grid(row = 0)
        self.countingLabel.grid(row = 1)
        self.countingLabel.after(1000, self.updateWorkingTime)
        self.m.attributes("-alpha", 0.5)

    def stopWorking(self):
        endTime = datetime.now() 
        self.tracking = False

        self.data.stopWorking(self.startTime, endTime)

        self.projectArea.pack()
        self.stopButton.grid_remove()
        self.countingLabel.grid_remove()
        for index in range(len(self.projectButtons)):
            self.projectButtons[index].grid()
            self.projectLabels[index][1].grid()
        for p in self.projectLabels:
            if p[0] == self.data.workingProject:
                total = self.data.getTodayTotal(p[0])
                p[1].configure(text = "Today Total: {:02}:{:02}:{:02}".format(total//3600, total%3600//60, total%60))

        # self.controlArea.pack()
        self.newItemButton.grid()
        self.exitButton.grid()
        self.settingButton.grid()
        self.archiveButton.grid()
        self.m.attributes("-alpha", 1)

    # ******** update time label **********
    def updateWorkingTime(self):
        t = datetime.now()-self.startTime
        self.countingLabel.configure(text=self.data.workingProject+"\n{:02}:{:02}:{:02}".format(t.seconds//3600, t.seconds%3600//60, t.seconds%60))
        if self.tracking:
            self.countingLabel.after(1000, self.updateWorkingTime)



    # ******** main loop **********
    def mainloop(self):
        self.m.overrideredirect(True)
        self.m.wm_attributes("-topmost", 1)
        self.m.mainloop()


if __name__ == "__main__":
    m = MainWindow()
    m.mainloop()
