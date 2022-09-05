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
        self.project_buttons = []
        self.archive_buttons = []
        self.rename_buttons = []
        self.project_labels = []

        # ******** Frames **********
        self.project_area = Frame()
        self.project_area.pack(side = TOP)
        self.control_area = Frame()
        self.control_area.pack(side = BOTTOM)

        # ******** buttons **********
        for id in self.data.data.project_id_names:
            self.add_new_project_button(self.data.data.project_id_names[id])

        self.new_item_button= Button(self.control_area, text='New', width = BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, fg='black', bg='lightblue')
        self.new_item_button.configure(command=lambda: self.release(self.add_new_item))
        self.new_item_button.grid(column=0, row = 0)

        self.stats_button = Button(self.control_area, text='Stats', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.stats_button.configure(command=lambda: self.release(self.open_setting))
        self.stats_button.grid(column=1, row = 0)

        self.rename_button = Button(self.control_area, text='Rename', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.rename_button.configure(command=lambda: self.release(self.rename_project))
        self.rename_button.grid(column=0, row = 1)

        self.return_rename_button = Button(self.control_area, text='Return', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.return_rename_button.configure(command=lambda: self.release(self.__exit_rename))

        self.archive_button = Button(self.control_area, text='Archive', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.archive_button.configure(command=lambda: self.release(self.archive_project))
        self.archive_button.grid(column=1, row = 1)

        self.return_archive_button = Button(self.control_area, text='Return', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.return_archive_button.configure(command=lambda: self.release(self.__exit_archive))

        self.setting_button = Button(self.control_area, text='Setting', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.setting_button.configure(command=lambda: self.release(self.open_setting))
        self.setting_button.grid(column=0, row = 2)
        
        self.return_setting_button = Button(self.control_area, text='Return', height = SMALL_BUTTON_HEIGHT, width=BUTTON_WIDTH, fg='black', bg='lightblue')
        self.return_setting_button.configure(command=lambda: self.release(self.close_setting))

        self.exit_button = Button(self.control_area, text='Exit', width=BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, fg='black', bg='red')
        self.exit_button.configure(command=lambda: self.release(exit))
        self.exit_button.grid(column=1, row = 2)


        self.photo = PhotoImage(file='stop.png').subsample(8,8)
        self.stop_button = Button(self.control_area, image = self.photo, command=lambda: self.release(self.stop_working))
        self.counting_label = Label(self.control_area, text="")

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

    def hide_all_control_buttons(self):
        self.new_item_button.grid_remove()
        self.exit_button.grid_remove()
        self.setting_button.grid_remove()
        self.rename_button.grid_remove()
        self.archive_button.grid_remove()
        self.stats_button.grid_remove()


    def show_all_control_buttons(self):
        self.new_item_button.grid()
        self.rename_button.grid()
        self.exit_button.grid()
        self.setting_button.grid()
        self.archive_button.grid()
        self.stats_button.grid()




    # ******** rename project **********
    def open_setting(self):
        self.hide_all_control_buttons()
        for button in self.project_buttons:
            button.grid_remove()
        for label in self.project_labels:
            label[1].grid_remove()
        self.project_area.pack_forget()
        self.return_setting_button.grid(column=0, row = 0)

    def close_setting(self):
        self.project_area.pack()
        self.show_all_control_buttons()
        for button in self.project_buttons:
            button.grid()
        for label in self.project_labels:
            label[1].grid()
        self.return_setting_button.grid_remove()


    # ******** rename project **********
    def rename_project(self):
        for i in range(len(self.project_buttons)):
            self.addRenameProjectButton(self.project_buttons[i]['text'], i)
        self.hide_all_control_buttons()
        self.return_rename_button.grid(row = 0, column = 0)

    def addRenameProjectButton(self, name, i):
        b = Button(self.project_area, text='Rename', height = MID_BUTTON_HEIGHT, width=BUTTON_WIDTH, font=tkFont.Font(size=20), fg = 'blue',  command=lambda: self.__rename_project(i))
        b.grid(row = i*2, column = 1)
        self.rename_buttons.append(b)


    def __rename_project(self, i):
        new_name = simpledialog.askstring(title="new Name",
                                  prompt="Please enter a new name for project "+ self.project_buttons[i]['text'])
        if new_name == None or new_name.strip() == "":
            self.__exit_rename()
            return
        new_name = new_name.strip()

        for j in range(len(self.project_buttons)):
            if j == i:
                continue
            if self.project_labels[j][0] == new_name:
                messagebox.showwarning(title="Invalid Name", message="Name used by other project")
                return
            
        self.data.rename_project(self.project_buttons[i]['text'], new_name)
        self.project_buttons[i]['text'] = new_name
        self.project_labels[i] = (new_name, self.project_labels[i][1])
        self.__exit_rename()

               
    def __exit_rename(self):
        for i in range(len(self.project_buttons)):
            self.project_buttons[i].grid(row = i*2)
            self.project_labels[i][1].grid(row = i*2+1)
        for i in self.rename_buttons:
            i.destroy()
        self.rename_buttons= []
 
        self.return_rename_button.grid_remove()
        self.show_all_control_buttons()


    # ******** archive project **********
    def archive_project(self):
        for i in range(len(self.project_buttons)):
            self.add_archive_project_button(self.project_buttons[i]['text'], i)
        self.hide_all_control_buttons()
        self.return_archive_button.grid(row = 0, column = 0)

    def add_archive_project_button(self, name, i):
        b = Button(self.project_area, text='Archive', height = MID_BUTTON_HEIGHT, width=BUTTON_WIDTH, font=tkFont.Font(size=20), fg = 'blue',  command=lambda: self.__archive_project(i))
        b.grid(row = i*2, column = 1)
        self.archive_buttons.append(b)


    def __archive_project(self, i):
        name = self.project_buttons[i]['text']
        self.data.archive_project(name)
        self.project_buttons[i].destroy()
        del self.project_buttons[i]
        self.project_labels[i][1].destroy()
        del self.project_labels[i]
        self.__exit_archive()

           
    def __exit_archive(self):
        for i in range(len(self.project_buttons)):
            self.project_buttons[i].grid(row = i*2)
            self.project_labels[i][1].grid(row = i*2+1)
        for i in self.archive_buttons:
            i.destroy()
        self.archive_buttons = []
 
        self.return_archive_button.grid_remove()
        self.show_all_control_buttons()


    # ******** add new project **********
    def add_new_item(self):

        new_name = simpledialog.askstring(title="new Project",
                                  prompt="Please enter a name for the project ")
        if new_name == None or new_name == "":
            return
        new_name = new_name.strip()

        if self.data.try_add_project(new_name):
            self.add_new_project_button(new_name)

    def add_new_project_button(self, name):
        total = self.data.get_today_total(name)
        new_button = Button(self.project_area, text=name, height = MID_BUTTON_HEIGHT , width=WID_BUTTON_WIDTH, font=tkFont.Font(size=20), command= lambda: self.start_working(new_button))
        new_button.grid(row = len(self.project_buttons)*2)
        l = Label(self.project_area, text="Today Total: {:02}:{:02}:{:02}".format(total//3600, total%3600//60, total%60))
        l.grid(row = len(self.project_buttons)*2 + 1)
        self.project_buttons.append(new_button)
        self.project_labels.append((name, l))

    # ******** begin and stop **********
    def start_working(self, button):
        self.data.start_working(button['text'])
        self.tracking = True

        self.hide_all_control_buttons()
        self.project_area.pack_forget()
        for button in self.project_buttons:
            button.grid_remove()
        for label in self.project_labels:
            label[1].grid_remove()

        self.stop_button.grid(row = 0)
        self.counting_label.grid(row = 1)
        self.update_working_time()
        self.counting_label.after(1000, self.update_working_time)
        self.m.attributes("-alpha", 0.5)

    def stop_working(self):
        self.tracking = False

        self.data.stop_working()

        self.project_area.pack()
        self.stop_button.grid_remove()
        self.counting_label.grid_remove()
        for index in range(len(self.project_buttons)):
            self.project_buttons[index].grid()
            self.project_labels[index][1].grid()
        for p in self.project_labels:
            if p[0] == self.data.working_project:
                total = self.data.get_today_total(p[0])
                p[1].configure(text = "Today Total: {:02}:{:02}:{:02}".format(total//3600, total%3600//60, total%60))

        self.show_all_control_buttons()
        self.m.attributes("-alpha", 1)

    # ******** update time label **********
    def update_working_time(self):
        t = self.data.get_working_time()
        self.counting_label.configure(text=self.data.working_project+"\n{:02}:{:02}:{:02}".format(t.seconds//3600, t.seconds%3600//60, t.seconds%60))
        if self.tracking:
            self.counting_label.after(1000, self.update_working_time)



    # ******** main loop **********
    def mainloop(self):
        self.m.overrideredirect(True)
        self.m.wm_attributes("-topmost", 1)
        self.m.mainloop()


if __name__ == "__main__":
    m = MainWindow()
    m.mainloop()
