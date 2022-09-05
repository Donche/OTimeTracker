import tkinter as tk
from tkinter import *
import platform
from tkinter import ttk
if platform.system() == "Darwin":
    from tkmacosx import Button
    MID_BUTTON_HEIGHT = 70
    SMALL_BUTTON_HEIGHT = 50
    SMOL_BUTTON_WIDTH = 70
    BUTTON_WIDTH = 100
    WID_BUTTON_WIDTH = 200
else:
    from tkinter import Button
    MID_BUTTON_HEIGHT = 3
    SMALL_BUTTON_HEIGHT = 2
    SMOL_BUTTON_WIDTH = 5
    BUTTON_WIDTH = 7
    WID_BUTTON_WIDTH = 9

from tkinter import font as tkFont
from tkinter import simpledialog
from tkinter import messagebox
from DataControl import DataControl




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

        self.newItemButton= Button(self.controlArea, text='New', width = BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, fg='black', bg='lightblue')
        self.newItemButton.configure(command=lambda: self.release(self.addNewItem))
        self.newItemButton.grid(column=0, row = 0)

        self.statsButton = Button(self.controlArea, text='Stats', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.statsButton.configure(command=lambda: self.release(self.openSetting))
        self.statsButton.grid(column=1, row = 0)

        self.renameButton = Button(self.controlArea, text='Rename', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.renameButton.configure(command=lambda: self.release(self.renameProject))
        self.renameButton.grid(column=0, row = 1)

        self.returnRenameButton = Button(self.controlArea, text='Return', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.returnRenameButton.configure(command=lambda: self.release(self.__exitRename))

        self.archiveButton = Button(self.controlArea, text='Archive', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.archiveButton.configure(command=lambda: self.release(self.archiveProject))
        self.archiveButton.grid(column=1, row = 1)

        self.returnArchiveButton = Button(self.controlArea, text='Return', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.returnArchiveButton.configure(command=lambda: self.release(self.__exitArchive))

        self.settingButton = Button(self.controlArea, text='Setting', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.settingButton.configure(command=lambda: self.release(self.openSetting))
        self.settingButton.grid(column=0, row = 2)
        
        self.returnSettingButton = Button(self.controlArea, text='Return', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.returnSettingButton.configure(command=lambda: self.release(self.closeSetting))

        self.exitButton = Button(self.controlArea, text='Exit', width=BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, fg='black', bg='red')
        self.exitButton.configure(command=lambda: self.release(exit))
        self.exitButton.grid(column=1, row = 2)


        self.photo = PhotoImage(file='stop.png').subsample(8,8)
        self.stopButton = Button(self.controlArea, image = self.photo, command=lambda: self.release(self.stopWorking))
        self.countingLabel = Label(self.controlArea, text="")

        # ******** variables **********
        self.dragging = False
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

    def hideAllControlButtons(self):
        self.newItemButton.grid_remove()
        self.exitButton.grid_remove()
        self.settingButton.grid_remove()
        self.renameButton.grid_remove()
        self.archiveButton.grid_remove()
        self.statsButton.grid_remove()


    def showAllControlButtons(self):
        self.newItemButton.grid()
        self.renameButton.grid()
        self.exitButton.grid()
        self.settingButton.grid()
        self.archiveButton.grid()
        self.statsButton.grid()




    # ******** rename project **********
    def openSetting(self):
        self.hideAllControlButtons()
        for button in self.projectButtons:
            button.grid_remove()
        for label in self.projectLabels:
            label[1].grid_remove()
        self.projectArea.pack_forget()
        self.returnSettingButton.grid(column=0, row = 0)

    def closeSetting(self):
        self.projectArea.pack()
        self.showAllControlButtons()
        for button in self.projectButtons:
            button.grid()
        for label in self.projectLabels:
            label[1].grid()
        self.returnSettingButton.grid_remove()


    # ******** rename project **********
    def renameProject(self):
        for i in range(len(self.projectButtons)):
            self.addRenameProjectButton(self.projectButtons[i]['text'], i)
        self.hideAllControlButtons()
        self.returnRenameButton.grid(row = 0, column = 0)

    def addRenameProjectButton(self, name, i):
        b = Button(self.projectArea, text='Rename', height = MID_BUTTON_HEIGHT, width=BUTTON_WIDTH, font=tkFont.Font(size=20), fg = 'blue',  command=lambda: self.__renameProject(i))
        b.grid(row = i*2, column = 1)
        self.renameButtons.append(b)


    def __renameProject(self, i):
        newName = simpledialog.askstring(title="new Name",
                                  prompt="Please enter a new name for project "+ self.projectButtons[i]['text'])
        if newName == None or newName.strip() == "":
            self.__exitRename()
            return
        newName = newName.strip()

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
 
        self.returnRenameButton.grid_remove()
        self.showAllControlButtons()


    # ******** archive project **********
    def archiveProject(self):
        for i in range(len(self.projectButtons)):
            self.addArchiveProjectButton(self.projectButtons[i]['text'], i)
        self.hideAllControlButtons()
        self.returnArchiveButton.grid(row = 0, column = 0)

    def addArchiveProjectButton(self, name, i):
        b = Button(self.projectArea, text='Archive', height = MID_BUTTON_HEIGHT, width=BUTTON_WIDTH, font=tkFont.Font(size=20), fg = 'blue',  command=lambda: self.__archiveProject(i))
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
 
        self.returnArchiveButton.grid_remove()
        self.showAllControlButtons()


    # ******** add new project **********
    def addNewItem(self):

        newName = simpledialog.askstring(title="new Project",
                                  prompt="Please enter a name for the project ")
        if newName == None or newName == "":
            return
        newName = newName.strip()

        if self.data.tryAddProject(newName):
            self.addNewProjectButton(newName)

    def addNewProjectButton(self, name):
        total = self.data.getTodayTotal(name)
        new_button = Button(self.projectArea, text=name, height = MID_BUTTON_HEIGHT , width=WID_BUTTON_WIDTH, font=tkFont.Font(size=20), command= lambda: self.startWorking(new_button))
        new_button.grid(row = len(self.projectButtons)*2)
        l = Label(self.projectArea, text="Today Total: {:02}:{:02}:{:02}".format(total//3600, total%3600//60, total%60))
        l.grid(row = len(self.projectButtons)*2 + 1)
        self.projectButtons.append(new_button)
        self.projectLabels.append((name, l))

    # ******** begin and stop **********
    def startWorking(self, button):
        self.data.startWorking(button['text'])
        self.tracking = True

        self.hideAllControlButtons()
        self.projectArea.pack_forget()
        for button in self.projectButtons:
            button.grid_remove()
        for label in self.projectLabels:
            label[1].grid_remove()

        self.stopButton.grid(row = 0)
        self.countingLabel.grid(row = 1)
        self.updateWorkingTime()
        self.countingLabel.after(1000, self.updateWorkingTime)
        self.m.attributes("-alpha", 0.5)

    def stopWorking(self):
        self.tracking = False

        self.data.stopWorking()

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

        self.showAllControlButtons()
        self.m.attributes("-alpha", 1)

    # ******** update time label **********
    def updateWorkingTime(self):
        t = self.data.getWorkingTime()
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
