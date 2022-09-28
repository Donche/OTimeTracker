import tkinter as tk
from tkinter import filedialog
from tkinter import *
import platform
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

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
        sns.set_theme(palette="Set3")
        custom_style = {'axes.labelcolor': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white'}
        sns.set(rc={'axes.facecolor':'#333333', 'axes.labelcolor': 'lightgrey',
                'axes.edgecolor': '#888888',
                'xtick.color': 'lightgrey', 'grid.color': '#888888',
                'text.color': 'lightgrey', 'patch.edgecolor': '#666666',
                'ytick.color': 'lightgrey','figure.facecolor':'#222222'})
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
        self.project_area.grid(column=0, row = 0)
        self.control_area = Frame()
        self.control_area.grid(column=0, row = 1)
        self.stats_area = Frame()
        self.stats_area.grid(column=1, row = 0, rowspan=2)
        self.stats_area.grid_remove()

        # ******** Project Buttons **********
        for id in self.data.data.project_id_names:
            self.add_new_project_button(self.data.data.project_id_names[id])

        self.new_item_button = self._control_button()(text='New', command=self.add_new_item)
        self.new_item_button.grid(column=0, row = 0)

        # ******** Stats & Figure Buttons **********
        self.stats_button = self._control_button()(text='Stats', command=self.show_fig)
        self.stats_button.grid(column=1, row = 0)

        self.fig = plt.Figure(dpi=150)
        self.fig.set_tight_layout({"pad": 1.0})
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.stats_area)

        self.radio_button_choice = IntVar(value=0)
        self.Choices = [('HeatMap', 0), ('BarPlot', 1), ('PieChart', 2)]
        button_color = ('palegreen', 'mistyrose', 'lavender', 'plum1')
        total_width = 60
        for c, v in self.Choices:
            tk.Radiobutton(self.stats_area, text=c, padx = 20, indicatoron = 0,
            width = int(total_width/len(self.Choices)), height=3, anchor=CENTER, 
            fg='black', bg=button_color[v], font=tkFont.Font(size=20), 
            variable=self.radio_button_choice, command=self.update_fig, 
            value=v).grid(row = 0, column=v,sticky="ew")


        self.scale_frame = Frame(self.stats_area)
        self.scale_frame.grid(column=0, row = 2, columnspan=3)

        self.control_scale = [('<', -1), ('o', 0), ('>', 1)]
        self.control_scale_choice = IntVar(value=0)
        for c, v in self.control_scale:
            tk.Radiobutton(self.scale_frame, text=c, padx = 20, indicatoron = 0,
            width = int(total_width/len(self.control_scale)), height=2, 
            anchor=CENTER, fg='black', bg=button_color[v],
            font=tkFont.Font(size=10), variable=self.control_scale_choice, 
            command=self.update_range, value=v).grid(row = 0, column=(v+1)*4,columnspan=4,sticky="ew")

        self.time_scale = [('week', 0), ('month', 1), ('year', 2), ('all', 3)]
        self.time_scale_choice = IntVar(value=0)
        for c, v in self.time_scale:
            tk.Radiobutton(self.scale_frame, text=c, padx = 20, indicatoron = 0,
            width = int(total_width/len(self.time_scale)), height=2, 
            anchor=CENTER, fg='black', bg=button_color[v],
            font=tkFont.Font(size=20), variable=self.time_scale_choice, 
            command=self.update_fig, value=v).grid(row = 1, column=v*3,columnspan=3,sticky="ew")

        # ******** Control Buttons **********
        self.rename_button = self._control_button()(text='Rename', command=self.rename_project)
        self.rename_button.grid(column=0, row = 1)

        self.return_rename_button = self._control_button()(text='Return', command=self.__exit_rename)

        self.archive_button = self._control_button()(text='Archive', command=self.archive_project)
        self.archive_button.grid(column=1, row = 1)

        self.return_archive_button = self._control_button()(text='Return', command=self.__exit_archive)

        self.setting_button = self._control_button()(text='Setting', command=self.open_setting)
        self.setting_button.grid(column=0, row = 2)
        self.setting_buttons = []
        self.setting_buttons.append(self._control_button()(text='data path', command=self.change_data_path))

        
        self.return_setting_button = self._control_button()(text='Return', command=self.close_setting)

        self.exit_button = Button(self.control_area, width = BUTTON_WIDTH, command=exit,
                height=SMALL_BUTTON_HEIGHT, fg='black', bg='red', text='Exit')
        self.exit_button.grid(column=1, row = 2)


        self.photo = PhotoImage(file='stop.png').subsample(8,8)
        self.stop_button = Button(self.control_area, image = self.photo, command=self.stop_working)
        self.counting_label = Label(self.control_area, text="")

        # ******** variables **********
        self.dragging = False
        self.tracking = False

    def _control_button(self):
        def b(*args, **kwargs):
            return Button(self.control_area, width = BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, 
                fg='black', bg='lightblue', *args, **kwargs)
        return b

    def _decorator(foo):
        def magic( self ) :
            if self.dragging:
                self.dragging = False
            elif foo != 0:
                foo( self )
        return magic

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




    # ******** settting **********
    @_decorator
    def open_setting(self):
        self.hide_all_control_buttons()
        for button in self.project_buttons:
            button.grid_remove()
        for label in self.project_labels:
            label[1].grid_remove()
        self.project_area.grid_remove()
        for b in self.setting_buttons:
            b.grid()
        self.return_setting_button.grid()

    @_decorator
    def close_setting(self):
        self.project_area.grid()
        self.show_all_control_buttons()
        for button in self.project_buttons:
            button.grid()
        for label in self.project_labels:
            label[1].grid()
        self.return_setting_button.grid_remove()
        for b in self.setting_buttons:
            b.grid_remove()
    
    def change_data_path(self):
        folder_selected = filedialog.askdirectory()
        self.data.set_data_path(folder_selected+"/")
        print(folder_selected)


    # ******** rename project **********
    @_decorator
    def rename_project(self):
        for i in range(len(self.project_buttons)):
            self.addRenameProjectButton(self.project_buttons[i]['text'], i)
        self.hide_all_control_buttons()
        self.return_rename_button.grid(row = 0, column = 0)

    def addRenameProjectButton(self, name, i):
        b = Button(self.project_area, text='Rename', 
                height = MID_BUTTON_HEIGHT, width=BUTTON_WIDTH, 
                font=tkFont.Font(size=20), fg = 'blue', 
                command=lambda: self.__rename_project(i))
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

               
    @_decorator
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
    @_decorator
    def archive_project(self):
        for i in range(len(self.project_buttons)):
            self.add_archive_project_button(self.project_buttons[i]['text'], i)
        self.hide_all_control_buttons()
        self.return_archive_button.grid(row = 0, column = 0)

    def add_archive_project_button(self, name, i):
        b = Button(self.project_area, text='Archive', 
                height = MID_BUTTON_HEIGHT, width=BUTTON_WIDTH, 
                font=tkFont.Font(size=20), fg = 'blue', 
                command=lambda: self.__archive_project(i))
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

           
    @_decorator
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
    @_decorator
    def add_new_item(self):

        new_name = simpledialog.askstring(title="new Project",
                                  prompt="Please enter a name for the project ")
        if new_name == None or new_name == "":
            return
        new_name = new_name.strip()

        if self.data.try_add_project(new_name):
            self.add_new_project_button(new_name)

    def add_new_project_button(self, name):
        today_total = self.data.get_today_total(name)
        total = self.data.get_total(name)
        new_button = Button(self.project_area, text=name, 
                height = MID_BUTTON_HEIGHT , width=WID_BUTTON_WIDTH, 
                font=tkFont.Font(size=20), command= lambda: self.start_working(new_button))
        new_button.grid(row = len(self.project_buttons)*2, sticky="n")
        l = Label(self.project_area, text="Today Total: {:02}:{:02}:{:02}\n"\
                "Total: {:02}:{:02}:{:02}"
                .format(today_total//3600, today_total%3600//60, today_total%60, 
                total//3600, total%3600//60, total%60))
        l.grid(row = len(self.project_buttons)*2 + 1)
        self.project_buttons.append(new_button)
        self.project_labels.append((name, l))


    # ******** begin and stop **********
    def start_working(self, button):
        self.data.start_working(button['text'])
        self.tracking = True

        self.hide_all_control_buttons()
        self.project_area.grid_remove()
        for button in self.project_buttons:
            button.grid_remove()
        for label in self.project_labels:
            label[1].grid_remove()

        self.stop_button.grid(row = 0)
        self.counting_label.grid(row = 1)
        self.update_working_time()
        self.counting_label.after(1000, self.update_working_time)
        self.m.attributes("-alpha", 0.5)
        self.m.wm_attributes("-topmost", 1)

    @_decorator
    def stop_working(self):
        self.tracking = False

        self.data.stop_working()

        self.project_area.grid()
        self.stop_button.grid_remove()
        self.counting_label.grid_remove()
        for index in range(len(self.project_buttons)):
            self.project_buttons[index].grid()
            self.project_labels[index][1].grid()
        for p in self.project_labels:
            if p[0] == self.data.working_project:
                today_total = self.data.get_today_total(p[0])
                total = self.data.get_total(p[0])
                p[1].configure(text = "Today Total: {:02}:{:02}:{:02}\n"\
                    "Total: {:02}:{:02}:{:02}"
                    .format(today_total//3600, today_total%3600//60, today_total%60, 
                    total//3600, total%3600//60, total%60))

        self.show_all_control_buttons()
        self.m.attributes("-alpha", 1)
        self.m.wm_attributes("-topmost", 0)


    def update_working_time(self):
        t = self.data.get_working_time()
        self.counting_label.configure(text=self.data.working_project+
            "\n{:02}:{:02}:{:02}".format(t.seconds//3600, t.seconds%3600//60, t.seconds%60))
        if self.tracking:
            self.counting_label.after(1000, self.update_working_time)


    # ******** figures **********
    @_decorator
    def show_fig(self):
        if self.stats_button['text'] != 'Stats':
            self.stats_area.grid_remove()
            self.stats_button.configure(text="Stats", bg='lightblue')
            for ax in self.axes:
                ax.remove()
            return
        
        self.data.init_plot()
        self.scale_frame.grid_remove()
        self.axes = self.data.all_proj_heatmap(self.fig)
        self.stats_button.configure(text="hide stats", bg='pink')
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=len(self.Choices))
        self.stats_area.grid()

    def update_fig(self):
        for ax in self.axes:
            ax.remove()
        if self.radio_button_choice.get() == 0:
            self.axes = self.data.all_proj_heatmap(self.fig)
            self.scale_frame.grid_remove()
        elif self.radio_button_choice.get() == 1:
            self.scale_frame.grid()
            self.axes = self.data.bar_plot(self.fig, self.time_scale[self.time_scale_choice.get()][0])
        elif self.radio_button_choice.get() == 2:
            self.scale_frame.grid()
            self.axes = self.data.pie_chart(self.fig, self.time_scale[self.time_scale_choice.get()][0])
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=len(self.Choices))
    
    def update_range(self):
        self.data.update_range(self.time_scale[self.time_scale_choice.get()][0], int(self.control_scale_choice.get()))
        self.update_fig()


    # ******** main loop **********
    def mainloop(self):
        self.m.overrideredirect(True)
        self.m.wm_attributes("-topmost", 0)
        self.m.mainloop()


if __name__ == "__main__":
    m = MainWindow()
    m.mainloop()
