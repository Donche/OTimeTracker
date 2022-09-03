import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime
from os.path import exists
import csv
import uuid

MID_BUTTON_HEIGHT = 3
SMALL_BUTTON_HEIGHT = 2

class DataControl():
    def __init__(self):
        self.projectIdNames = {}
        self.archivedProjectIdNames = {}
        self.trackRecord = {}
        self.workingProject = ""
        self.workingId = 0

        if exists('OTT_projects.txt'):
            with open('OTT_projects.txt','r') as f:
                lines = [i.strip() for i in f.readlines()]
                for l in lines:
                    if l[:2] == "--":
                        name, id = l[2:].split(", ")
                        self.archivedProjectIdNames[uuid.UUID(id.strip())] = name
                    else:
                        name, id = l.split(", ")
                        self.projectIdNames[uuid.UUID(id.strip())] = name
            print("projects: ", self.projectIdNames)
            print("archived projects: ", self.archivedProjectIdNames)


        log_file = '{}-{}.log'.format(datetime.now().year, datetime.now().month)
        if exists(log_file):
            with open(log_file, 'r') as f:
                r = csv.reader(f, delimiter=',')
                for row in r:
                    id = uuid.UUID(row[0].strip())
                    try:
                        if id in self.projectIdNames:
                            name = self.projectIdNames[id]
                        else:
                            name = self.archivedProjectIdNames[id]
                    except:
                        print("project id ", id, " not recognized")
                        continue
                    if name in self.trackRecord:
                        self.trackRecord[name].append((row[1], row[2], int(row[3])))
                    else:
                        self.trackRecord[name] = [(row[1], row[2], int(row[3]))]

    def getTodayTotal(self, name):
        if name in self.trackRecord:
            return sum([i[2] for i in self.trackRecord[name]])
        else:
            return 0

    def hasProject(self, name):
        for id in self.projectIdNames:
            if name == self.projectIdNames[id]:
                return True
        return False

    def getIdWithName(self, name):
        for id in self.projectIdNames:
            if name == self.projectIdNames[id]:
                return id


    def tryAddProject(self, name):
        if self.hasProject(name):
            return False
        else:
            id = uuid.uuid1()
            self.projectIdNames[id] = name
            with open('OTT_projects.txt','a') as f:
                f.write(name+", "+str(id)+"\n")
            return True

    def startWorking(self, name):
        self.workingProject = name
        for id in self.projectIdNames:
            if self.workingProject == self.projectIdNames[id]:
                self.workingId = id
                break


    def stopWorking(self, startTime, endTime):
        if self.workingProject in self.trackRecord:
            self.trackRecord[self.workingProject].append((str(startTime), str(endTime), (endTime-startTime).seconds))
        else:
            self.trackRecord[self.workingProject] = [(str(startTime), str(endTime), (endTime-startTime).seconds)]
        log_file = '{}-{}.log'.format(startTime.year, startTime.month)
        with open(log_file, 'a') as f:
            f.write(str(self.workingId) + ", "+ str(startTime) + ", " + str(endTime) + ", " + str((endTime-startTime).seconds)+"\n")

    def archiveProject(self, name):
        print('archive ', name)
        id = self.getIdWithName(name)
        self.archivedProjectIdNames[id] = self.projectIdNames.pop(id, None)

        with open('OTT_projects.txt','w') as f:
            for id in self.projectIdNames:
                f.write(self.projectIdNames[id]+", "+str(id)+"\n")
            for id in self.archivedProjectIdNames:
                f.write("--"+self.archivedProjectIdNames[id]+", "+str(id)+"\n")

    def renameProject(self, oldName, newName):
        print('rename ', oldName, " to ", newName)
        id = self.getIdWithName(oldName)
        self.projectIdNames[id] = newName

        with open('OTT_projects.txt','w') as f:
            for id in self.projectIdNames:
                f.write(self.projectIdNames[id]+", "+str(id)+"\n")
            for id in self.archivedProjectIdNames:
                f.write("--"+self.archivedProjectIdNames[id]+", "+str(id)+"\n")






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
        self.archiveButtons = []
        self.renameButtons = []
        self.projectLabels = []

        # ******** Frames **********
        self.projectArea = Frame()
        self.projectArea.pack(side = TOP)
        self.controlArea = Frame()
        self.controlArea.pack(side = BOTTOM)

        # ******** buttons **********
        for id in self.data.projectIdNames:
            self.addNewProjectButton(self.data.projectIdNames[id])

        self.newItemButton = tk.Button(self.controlArea, text='New', height = SMALL_BUTTON_HEIGHT, width=7, fg='black', bg='lightblue', font=tkFont.Font(size=15))
        self.newItemButton.grid(column=0, row = 0)
        self.newItemButton.bind("<ButtonRelease>", lambda event: self.release(self.addNewItem))

        self.exitButton = tk.Button(self.controlArea, text='Exit', height = SMALL_BUTTON_HEIGHT, width=7, fg='red', bg='black', font=tkFont.Font(size=15))
        self.exitButton.grid(column=1, row = 0)
        self.exitButton.bind("<ButtonRelease>", lambda event: self.release(exit))

        self.settingButton = tk.Button(self.controlArea, text='Setting', height = SMALL_BUTTON_HEIGHT, width=7, fg='black', bg='lightblue', font=tkFont.Font(size=15))
        self.settingButton.grid(column=0, row = 1)
        self.settingButton.bind("<ButtonRelease>", lambda event: self.release(self.openSetting))

        self.returnSettingButton = tk.Button(self.controlArea, text='Return', height = SMALL_BUTTON_HEIGHT, width=7, fg='black', bg='lightblue', font=tkFont.Font(size=15))
        self.returnSettingButton.bind("<ButtonRelease>", lambda event: self.release(self.closeSetting))

        self.archiveButton = tk.Button(self.controlArea, text='Archive', height = SMALL_BUTTON_HEIGHT, width=7, fg='black', bg='lightblue', font=tkFont.Font(size=15))
        self.archiveButton.grid(column=1, row = 1)
        self.archiveButton.bind("<ButtonRelease>", lambda event: self.release(self.archiveProject))

        self.renameButton = tk.Button(self.controlArea, text='Rename', height = SMALL_BUTTON_HEIGHT, width=7, fg='black', bg='lightblue', font=tkFont.Font(size=15))
        self.renameButton.grid(column=0, row = 2)
        self.renameButton.bind("<ButtonRelease>", lambda event: self.release(self.renameProject))
        
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
        self.settingButton.grid_remove()
        self.archiveButton.grid_remove()
        for button in self.projectButtons:
            button.grid_remove()
        for label in self.projectLabels:
            label[1].grid_remove()
        self.projectArea.pack_forget()
        self.returnSettingButton.grid(column=0, row = 0)
        # self.controlArea.pack_forget()

    def closeSetting(self):
        self.projectArea.pack()
        self.newItemButton.grid()
        self.exitButton.grid()
        self.settingButton.grid()
        self.archiveButton.grid()
        for button in self.projectButtons:
            button.grid()
        for label in self.projectLabels:
            label[1].grid()
        self.returnSettingButton.grid_remove()


    # ******** rename project **********
    def renameProject(self):
        for i in range(len(self.projectButtons)):
            self.addRenameProjectButton(self.projectButtons[i]['text'], i)
        self.renameButton.configure(text="return")
        self.renameButton.bind("<ButtonRelease>", lambda event: self.release(self.__exitRename))

        self.newItemButton.grid_remove()
        self.exitButton.grid_remove()
        self.settingButton.grid_remove()
        self.archiveButton.grid_remove()

    def addRenameProjectButton(self, name, i):
        b = tk.Button(self.projectArea, text='Rename', height = MID_BUTTON_HEIGHT, width=5, font=tkFont.Font(size=20), fg = 'blue',  command=lambda: self.__renameProject(i))
        b.grid(row = i*2, column = 1)
        self.renameButtons.append(b)


    def __renameProject(self, i):
        newName = simpledialog.askstring(title="new Name",
                                  prompt="Please enter a new name for project "+ self.projectButtons[i]['text'])
        if newName == None:
            self.__exitRename()
            return

        for j in range(len(self.projectButtons)):
            if j == i:
                continue
            if self.projectLabels[j][0] == newName:
                messagebox.showwarning(title="Invalid Name", message="Name used by other project")
                return
            
        self.data.renameProject(self.projectButtons[i]['text'], newName)
        self.projectButtons[i]['text'] = newName
        self.projectLabels[i] = (newName, self.projectLabels[i][1])
        self.__exitRename()

               
    def __exitRename(self):
        for i in range(len(self.projectButtons)):
            self.projectButtons[i].grid(row = i*2)
            self.projectLabels[i][1].grid(row = i*2+1)
        for i in self.renameButtons:
            i.destroy()
        self.renameButtons= []
 
        self.renameButton.configure(text="Rename")
        self.renameButton.bind("<ButtonRelease>", lambda event: self.release(self.renameProject))

        self.newItemButton.grid()
        self.exitButton.grid()
        self.settingButton.grid()
        self.archiveButton.grid()



    # ******** archive project **********
    def archiveProject(self):
        for i in range(len(self.projectButtons)):
            self.addArchiveProjectButton(self.projectButtons[i]['text'], i)
        self.archiveButton.configure(text="return")
        self.archiveButton.bind("<ButtonRelease>", lambda event: self.release(self.__exitArchive))
        self.newItemButton.grid_remove()
        self.exitButton.grid_remove()
        self.settingButton.grid_remove()
        self.renameButton.grid_remove()

    def addArchiveProjectButton(self, name, i):
        b = tk.Button(self.projectArea, text='Archive', height = MID_BUTTON_HEIGHT, width=5, font=tkFont.Font(size=20), fg = 'blue',  command=lambda: self.__archiveProject(i))
        b.grid(row = i*2, column = 1)
        self.archiveButtons.append(b)


    def __archiveProject(self, i):
        name = self.projectButtons[i]['text']
        self.data.archiveProject(name)
        self.projectButtons[i].destroy()
        del self.projectButtons[i]
        self.projectLabels[i][1].destroy()
        del self.projectLabels[i]
        self.__exitArchive()

           
    def __exitArchive(self):
        for i in range(len(self.projectButtons)):
            self.projectButtons[i].grid(row = i*2)
            self.projectLabels[i][1].grid(row = i*2+1)
        for i in self.archiveButtons:
            i.destroy()
        self.archiveButtons = []
 
        self.archiveButton.configure(text="Archive")
        self.archiveButton.bind("<ButtonRelease>", lambda event: self.release(self.archiveProject))

        self.newItemButton.grid()
        self.exitButton.grid()
        self.settingButton.grid()
        self.renameButton.grid()


    # ******** add new project **********
    def addNewItem(self):
        l = tk.Label(self.projectArea, text="Item Name ")
        entry = tk.Entry(self.projectArea)
        entry.bind("<Return>", lambda event: self.confirmNewItem(entry, [l, entry, b]))
        b = tk.Button(self.projectArea, text='Confirm New Item', command=lambda: self.confirmNewItem(entry, [l, entry, b]))
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
        new_button = tk.Button(self.projectArea, text=name, height = MID_BUTTON_HEIGHT , width=12, font=tkFont.Font(size=20), command= lambda: self.startWorking(new_button))
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
        self.renameButton.grid_remove()
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
        self.renameButton.grid()
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
